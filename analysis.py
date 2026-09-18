"""MBTI별 투자 성향 통계 분석."""

import pandas as pd

from database import get_all_users, get_all_investment_tests


def load_analysis_dataframe():
    """users와 investment_tests를 user_id 기준으로 결합한다."""
    users = get_all_users()
    tests = get_all_investment_tests()

    if not users or not tests:
        return pd.DataFrame()

    users_df = pd.DataFrame(users)
    tests_df = pd.DataFrame(tests)

    return users_df.merge(tests_df, on="user_id", how="inner")


def get_mbti_statistics(df):
    """MBTI별 핵심 수치 통계를 계산한다."""
    if df.empty:
        return pd.DataFrame()

    return (
        df.groupby("mbti")
        .agg(
            user_count=("user_id", "count"),
            avg_risk_score=("risk_score", "mean"),
            avg_target_return=("target_return", "mean"),
        )
        .round(2)
        .sort_index()
    )


def get_distribution(df, column):
    """MBTI별 범주형 변수 분포를 표 형태로 반환한다."""
    if df.empty:
        return pd.DataFrame()

    return pd.crosstab(df["mbti"], df[column])


def run_mbti_analysis():
    """콘솔에서 MBTI별 투자 성향 통계를 출력한다."""
    df = load_analysis_dataframe()

    if df.empty:
        print("\n 분석할 투자성향 검사 데이터가 없습니다.")
        return

    print("\n================================")
    print("      MBTI별 투자 성향 통계")
    print("================================")
    print(f"분석 대상: {len(df)}명")

    print("\n[1] MBTI별 평균 위험점수 / 목표수익률")
    print(get_mbti_statistics(df).to_string())

    print("\n[2] MBTI별 투자 유형 분포")
    print(get_distribution(df, "investment_type").to_string())

    print("\n[3] MBTI별 투자 기간 분포")
    print(get_distribution(df, "investment_period").to_string())

    print("\n[4] MBTI별 손실 감내도 분포")
    print(get_distribution(df, "loss_tolerance").to_string())
