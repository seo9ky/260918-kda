import pandas as pd
import matplotlib.pyplot as plt

#테스트용
data = {
    'user_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'mbti': [
        'ISTJ', 'ENFP', 'INTJ', 'ISTJ', 'ENFP',
        'ISFJ', 'INTJ', 'ENTP', 'ISFJ', 'ENFP'
    ],
    'age_group': [
        '20대', '20대', '30대', '20대', '30대',
        '20대', '30대', '20대', '30대', '20대'
    ],
    'risk_score': [
        30, 65, 70, 40, 60,
        35, 75, 80, 40, 55
    ],
    'investment_type': [
        '안정형', '공격형', '공격형', '안정형', '균형형',
        '안정형', '공격형', '공격형', '균형형', '균형형'
    ],
    'investment_period': [
        '장기', '단기', '장기', '장기', '중기',
        '장기', '장기', '단기', '중기', '중기'
    ],
    'loss_tolerance': [
        '낮음', '높음', '높음', '낮음', '보통',
        '낮음', '높음', '높음', '보통', '보통'
    ],
    'target_return': [
        5, 15, 20, 6, 10,
        5, 20, 25, 10, 12
    ],

    'stock_ratio': [55, 40, 60, 30, 50, 35, 65, 70, 40, 50],

    'etf_ratio': [30, 30, 25, 30, 30, 30, 20, 20, 30, 30],

    'bond_ratio': [10, 20, 10, 30, 15, 25, 10, 5, 20, 15],

    'cash_ratio': [5, 10, 5, 10, 5, 10, 5, 5, 10, 5] 
}

df = pd.DataFrame(data)

print(df)


#mbti별 인원수
print("\n===MBTI별 인원수===")

mbti_count = df['mbti'].value_counts()

print(mbti_count)


#mbti별 평균 위험점수
print("\n===MBTI별 평균 위험점수 ===")

avg_risk = df.groupby('mbti')['risk_score'].mean()

print(avg_risk)


#mbti별 투자성향 인원수
print("\n===MBTI별 투자성향 인원수 ===")

investment_count = pd.crosstab(
    df['mbti'],
    df['investment_type']
)

print(investment_count)


#mbti별 투자성향 비율
print("\n===MBTI별 투자성향 비율 ===")

investment_ratio = pd.crosstab(
    df['mbti'],
    df['investment_type'],
    normalize='index'
) * 100

print(investment_ratio.round(2))


#mbti별 투자기간 인원수
print("\n===MBTI별 투자기간 인원수 ===")

period_count = pd.crosstab(
    df['mbti'],
    df['investment_period']
)

print(period_count)

123
# MBTI별 투자기간 비율
print("\n=== MBTI별 투자기간 비율 ===")

period_ratio = pd.crosstab(
    df['mbti'],
    df['investment_period'],
    normalize='index'
) * 100

print(period_ratio.round(2))


# MBTI별 손실 감내 수준 인원수
print("\n=== MBTI별 손실 감내 수준 ===")

loss_count = pd.crosstab(
    df['mbti'],
    df['loss_tolerance']
)

print(loss_count)


# MBTI별 손실 감내 수준 비율
print("\n=== MBTI별 손실 감내 수준 비율 ===")

loss_ratio = pd.crosstab(
    df['mbti'],
    df['loss_tolerance'],
    normalize='index'
) * 100

print(loss_ratio.round(2))


# MBTI별 평균 목표 수익률
print("\n=== MBTI별 평균 목표 수익률 ===")

avg_return = df.groupby('mbti')['target_return'].mean()

print(avg_return.round(2))


# MBTI별 평균 포트폴리오 비율
print("\n=== MBTI별 평균 포트폴리오 비율 ===")

portfolio_avg = df.groupby('mbti')[
    ['stock_ratio', 'etf_ratio', 'bond_ratio', 'cash_ratio']
].mean()

print(portfolio_avg.round(2))

#mbti별 투자성향 비율 그래프

investment_ratio.plot(
    kind='bar',
    figsize=(10,6)
)


plt.title('MBTI별 투자성향 비율')
plt.xlabel('MBTI')
plt.ylabel('비율 (%)')

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()