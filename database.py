"""Supabase 데이터 조회/저장 함수 모음."""

from supabase_client import supabase


USER_TABLE = "users"
TEST_TABLE = "investment_tests"


def find_user_id(name):
    """이름으로 사용자 ID를 조회한다. 없으면 None을 반환한다."""
    result = (
        supabase
        .table(USER_TABLE)
        .select("user_id, name")
        .eq("name", name)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]["user_id"]


def get_user_by_name(name):
    """이름으로 사용자 기본 정보를 조회한다."""
    result = (
        supabase
        .table(USER_TABLE)
        .select("user_id, name, mbti, age_group")
        .eq("name", name)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def get_all_users():
    """MBTI 사용자 전체를 조회한다."""
    result = (
        supabase
        .table(USER_TABLE)
        .select("user_id, name, mbti, age_group")
        .order("user_id")
        .execute()
    )
    return result.data or []


def check_investment_test(user_id):
    """해당 사용자가 이미 투자성향 검사를 완료했는지 확인한다."""
    result = (
        supabase
        .table(TEST_TABLE)
        .select("test_id")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    return len(result.data or []) > 0


def save_investment_test(
    user_id,
    risk_score,
    investment_type,
    investment_period,
    loss_tolerance,
    target_return,
):
    """투자성향 검사 결과를 investment_tests에 저장한다."""
    data = {
        "user_id": user_id,
        "risk_score": risk_score,
        "investment_type": investment_type,
        "investment_period": investment_period,
        "loss_tolerance": loss_tolerance,
        "target_return": target_return,
    }

    result = (
        supabase
        .table(TEST_TABLE)
        .insert(data)
        .execute()
    )
    return result.data


def get_all_investment_tests():
    """투자성향 검사 결과 전체를 조회한다."""
    result = (
        supabase
        .table(TEST_TABLE)
        .select(
            "test_id, user_id, risk_score, investment_type, "
            "investment_period, loss_tolerance, target_return"
        )
        .order("test_id")
        .execute()
    )
    return result.data or []


def get_investment_test_by_user_id(user_id):
    """특정 사용자의 투자성향 검사 결과를 조회한다."""
    result = (
        supabase
        .table(TEST_TABLE)
        .select(
            "test_id, user_id, risk_score, investment_type, "
            "investment_period, loss_tolerance, target_return"
        )
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]
