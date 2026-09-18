"""K-Means 기반 투자 성향 군집 분석.

scikit-learn을 사용하지 않고 Python 코드로 직접 K-Means를 구현한다.

전체 투자성향 검사 데이터를 3개 군집으로 묶은 뒤,
평균 위험점수에 따라 안정/균형/공격 군집으로 해석하고
이름으로 특정 사용자의 결과를 조회한다.
"""

import math
import random

import pandas as pd

from analysis import load_analysis_dataframe


PERIOD_MAP = {
    "6개월 미만": 1,
    "6개월~1년": 2,
    "1~3년": 3,
    "3~5년": 4,
    "5년 이상": 5,
}

LOSS_MAP = {
    "매우 낮음": 1,
    "낮음": 2,
    "보통": 3,
    "높음": 4,
    "매우 높음": 5,
}

FEATURE_COLUMNS = [
    "risk_score",
    "target_return",
    "period_value",
    "loss_value",
]


def preprocess_data(df):
    """K-Means 분석에 사용할 데이터를 숫자형으로 전처리한다."""

    data = df.copy()

    data["period_value"] = data["investment_period"].map(PERIOD_MAP)
    data["loss_value"] = data["loss_tolerance"].map(LOSS_MAP)

    data["risk_score"] = pd.to_numeric(
        data["risk_score"],
        errors="coerce",
    )

    data["target_return"] = pd.to_numeric(
        data["target_return"],
        errors="coerce",
    )

    missing_mask = data[FEATURE_COLUMNS].isna().any(axis=1)

    if missing_mask.any():
        check_columns = [
            column
            for column in [
                "name",
                "investment_period",
                "loss_tolerance",
            ]
            if column in data.columns
        ]

        invalid_rows = data.loc[
            missing_mask,
            check_columns,
        ]

        raise ValueError(
            "K-Means 전처리에 실패한 값이 있습니다. "
            "investment_period 또는 loss_tolerance 값을 확인하세요.\n\n"
            + invalid_rows.to_string(index=False)
        )

    return data


def standardize(features):
    """각 입력 변수를 평균 0, 표준편차 1 기준으로 표준화한다."""

    if not features:
        return []

    columns = list(zip(*features))
    means = []
    stds = []

    for column in columns:
        mean = sum(column) / len(column)

        variance = (
            sum(
                (value - mean) ** 2
                for value in column
            )
            / len(column)
        )

        std = math.sqrt(variance)

        if std == 0:
            std = 1

        means.append(mean)
        stds.append(std)

    scaled_data = []

    for row in features:
        scaled_row = []

        for index, value in enumerate(row):
            standardized_value = (
                (value - means[index])
                / stds[index]
            )
            scaled_row.append(standardized_value)

        scaled_data.append(scaled_row)

    return scaled_data


def calculate_distance(point1, point2):
    """두 데이터 사이의 유클리드 거리를 계산한다."""

    return math.sqrt(
        sum(
            (value1 - value2) ** 2
            for value1, value2 in zip(point1, point2)
        )
    )


def simple_kmeans(data, k=3, max_iterations=100):
    """Python으로 직접 구현한 간단한 K-Means 알고리즘."""

    if len(data) < k:
        raise ValueError(
            f"K-Means 분석에는 최소 {k}명의 데이터가 필요합니다."
        )

    random.seed(42)
    centers = random.sample(data, k)
    previous_clusters = None

    for _ in range(max_iterations):
        clusters = []

        for row in data:
            distances = [
                calculate_distance(row, center)
                for center in centers
            ]

            nearest_cluster = distances.index(min(distances))
            clusters.append(nearest_cluster)

        if clusters == previous_clusters:
            break

        previous_clusters = clusters.copy()
        new_centers = []

        for cluster_id in range(k):
            members = [
                data[index]
                for index in range(len(data))
                if clusters[index] == cluster_id
            ]

            if not members:
                new_centers.append(random.choice(data))
                continue

            center = []

            for column_index in range(len(data[0])):
                average = (
                    sum(
                        row[column_index]
                        for row in members
                    )
                    / len(members)
                )
                center.append(average)

            new_centers.append(center)

        centers = new_centers

    return clusters


def run_kmeans(df):
    """투자성향 데이터를 3개 군집으로 분류한다."""

    data = preprocess_data(df)

    if len(data) < 3:
        raise ValueError(
            "K-Means 분석에는 투자성향 검사를 완료한 "
            "사용자가 최소 3명 필요합니다."
        )

    features = data[FEATURE_COLUMNS].values.tolist()
    scaled_features = standardize(features)

    data["cluster"] = simple_kmeans(
        scaled_features,
        k=3,
    )

    return data


def label_clusters(df):
    """평균 위험점수를 기준으로 군집에 이름을 부여한다."""

    data = df.copy()

    cluster_risk = (
        data.groupby("cluster")["risk_score"]
        .mean()
        .sort_values()
    )

    cluster_ids = list(cluster_risk.index)

    if len(cluster_ids) != 3:
        raise ValueError(
            "데이터가 충분히 구분되지 않아 "
            "3개의 유효한 군집을 만들지 못했습니다."
        )

    labels = {
        cluster_ids[0]: "안정 군집",
        cluster_ids[1]: "균형 군집",
        cluster_ids[2]: "공격 군집",
    }

    data["cluster_type"] = data["cluster"].map(labels)

    return data


def get_cluster_summary(df):
    """군집별 인원수, 평균 위험점수, 평균 목표수익률을 계산한다."""

    order = [
        "안정 군집",
        "균형 군집",
        "공격 군집",
    ]

    summary = (
        df.groupby("cluster_type")
        .agg(
            user_count=("user_id", "count"),
            avg_risk_score=("risk_score", "mean"),
            avg_target_return=("target_return", "mean"),
            avg_period_value=("period_value", "mean"),
            avg_loss_value=("loss_value", "mean"),
        )
        .round(2)
    )

    available_order = [
        cluster_type
        for cluster_type in order
        if cluster_type in summary.index
    ]

    return summary.reindex(available_order)


def get_mbti_cluster_distribution(df):
    """MBTI별 군집 분포를 계산한다."""

    return pd.crosstab(
        df["mbti"],
        df["cluster_type"],
    )


def explain_user_result(user_row, cluster_summary):
    """특정 사용자의 설문 결과와 K-Means 결과를 간단히 설명한다."""

    cluster_type = user_row["cluster_type"]
    cluster_info = cluster_summary.loc[cluster_type]
    investment_type = str(user_row["investment_type"])

    same_direction = False

    if (
        ("안정" in investment_type or "회피" in investment_type)
        and "안정" in cluster_type
    ):
        same_direction = True

    elif (
        ("중립" in investment_type or "균형" in investment_type)
        and "균형" in cluster_type
    ):
        same_direction = True

    elif (
        (
            "적극" in investment_type
            or "공격" in investment_type
            or "선호" in investment_type
        )
        and "공격" in cluster_type
    ):
        same_direction = True

    if same_direction:
        comparison_text = (
            "기존 설문 기반 투자유형과 "
            "K-Means 분석 결과가 유사한 방향을 보입니다."
        )
    else:
        comparison_text = (
            "기존 설문 기반 분류와 "
            "K-Means 군집 분석 결과에는 일부 차이가 있습니다."
        )

    return (
        f"{user_row['name']}님은 전체 투자성향 검사자 중 "
        f"'{cluster_type}'에 포함되었습니다. "
        f"이 군집의 평균 위험점수는 "
        f"{cluster_info['avg_risk_score']:.2f}점이며, "
        f"평균 목표수익률은 "
        f"{cluster_info['avg_target_return']:.2f}%입니다. "
        f"{comparison_text} "
        "K-Means 결과는 현재 수집된 사용자 데이터의 "
        "유사성을 기반으로 한 군집 분석 결과입니다."
    )


def run_ai_analysis(name=None):
    """전체 데이터를 K-Means로 분석하고 특정 사용자의 결과를 출력한다."""

    df = load_analysis_dataframe()

    if df.empty:
        print("\n분석할 투자성향 검사 데이터가 없습니다.")
        return None

    try:
        clustered = run_kmeans(df)
        clustered = label_clusters(clustered)

    except ValueError as error:
        print("\nAI 분석을 실행할 수 없습니다.")
        print(error)
        return None

    if name is None:
        name = input(
            "\nAI 분석할 사용자 이름을 입력하세요: "
        ).strip()

    matched = clustered[
        clustered["name"] == name
    ]

    if matched.empty:
        print(
            "\n투자성향 검사를 완료한 "
            "해당 사용자를 찾을 수 없습니다."
        )
        return None

    user_row = matched.iloc[0]
    cluster_summary = get_cluster_summary(clustered)

    print("\n================================")
    print("       K-Means AI 분석 결과")
    print("================================")
    print(f"이름          : {user_row['name']}")
    print(f"MBTI          : {user_row['mbti']}")
    print(f"연령대        : {user_row['age_group']}")
    print(f"위험 점수     : {user_row['risk_score']}")
    print(f"기존 투자 유형: {user_row['investment_type']}")
    print(f"K-Means 결과  : {user_row['cluster_type']}")
    print(f"투자 기간     : {user_row['investment_period']}")
    print(f"손실 감내도   : {user_row['loss_tolerance']}")
    print(f"목표 수익률   : {user_row['target_return']}%")

    print("\n[군집별 특징]")
    print(cluster_summary.to_string())

    print("\n[분석 해석]")
    print(
        explain_user_result(
            user_row,
            cluster_summary,
        )
    )

    mbti_distribution = get_mbti_cluster_distribution(clustered)

    return {
        "clustered_data": clustered,
        "cluster_summary": cluster_summary,
        "mbti_cluster_distribution": mbti_distribution,
        "user_result": user_row.to_dict(),
    }
