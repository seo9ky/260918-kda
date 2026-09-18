import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

####################################
def insert_user(name, mbti, age_group):
    result = supabase.table("users").insert({
        "name": name,
        "mbti": mbti,
        "age_group": age_group
    }).execute()
    return result.data[0]["user_id"]

def get_all_users():
    result = supabase.table("users").select("*").execute()
    return result.data



def insert_investment_test(user_id, risk_score, investment_type,
                             investment_period, loss_tolerance, target_return):
    result = supabase.table("investment_test").insert({
        "user_id": user_id,
        "risk_score": risk_score,
        "investment_type": investment_type,
        "investment_period": investment_period,
        "loss_tolerance": loss_tolerance,
        "target_return": target_return
    }).execute()
    return result.data



def insert_portfolio(user_id, stock_ratio, etf_ratio, bond_ratio, cash_ratio):
    result = supabase.table("portfolio").insert({
        "user_id": user_id,
        "stock_ratio": stock_ratio,
        "etf_ratio": etf_ratio,
        "bond_ratio": bond_ratio,
        "cash_ratio": cash_ratio
    }).execute()
    return result.data



def get_all_full_data():
    users = supabase.table("users").select("*").execute().data
    result = []
    for u in users:
        investment = supabase.table("investment_test").select("*").eq("user_id", u["user_id"]).execute().data
        portfolio = supabase.table("portfolio").select("*").eq("user_id", u["user_id"]).execute().data
        result.append({
            **u,
            **(investment[0] if investment else {}),
            **(portfolio[0] if portfolio else {})
        })
    return result
