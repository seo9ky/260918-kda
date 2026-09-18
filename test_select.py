import pandas as pd
from supabase_client import supabase

result = (
    supabase
    .table("investment_tests")
    .select("*")
    .execute()
)

df = pd.DataFrame(result.data)

if df.empty:
    print("investment_tests에 데이터가 없습니다.")
else:
    print("\n===== 전체 데이터 =====")
    print(df.to_string(index=False))

    for column in [
        "investment_type",
        "investment_period",
        "loss_tolerance",
        "target_return",
    ]:
        print(f"\n===== {column} 종류 =====")
        print(df[column].dropna().unique())

    print("\n===== risk_score 범위 =====")
    print("최소:", df["risk_score"].min())
    print("최대:", df["risk_score"].max())
