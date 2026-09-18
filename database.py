import os

from dotenv import load_dotenv
from supabase import create_client


# ======================================
# Supabase 연결
# ======================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ======================================
# 사용자 ID 조회
# ======================================

def find_user_id(name):

    result = (
        supabase
        .table("users")
        .select("user_id, name")
        .eq("name", name)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]["user_id"]


# ======================================
# 투자성향 검사 여부 확인
# ======================================

def check_investment_test(user_id):

    result = (
        supabase
        .table("investment_tests")
        .select("test_id")
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


# ======================================
# 투자성향 결과 저장
# ======================================

def save_investment_test(
    user_id,
    risk_score,
    investment_type,
    investment_period,
    loss_tolerance,
    target_return
):

    data = {
        "user_id": user_id,
        "risk_score": risk_score,
        "investment_type": investment_type,
        "investment_period": investment_period,
        "loss_tolerance": loss_tolerance,
        "target_return": target_return
    }

    result = (
        supabase
        .table("investment_tests")
        .insert(data)
        .execute()
    )

    return result.data