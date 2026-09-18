# MBTI × 투자성향 분석 프로그램

Supabase에 등록된 사용자가 투자 성향 검사를 수행하고, 검사 결과를 DB에 저장한 뒤 MBTI별 통계와 K-Means 기반 군집 분석을 수행하는 팀 프로젝트입니다.

## 주요 기능

1. **투자성향 검사**
   - `mbti_users`에 존재하는 이름을 입력
   - 20문항 투자 설문 진행
   - 위험점수, 투자유형, 투자기간, 손실감내도, 목표수익률 계산
   - 결과를 `investment_tests`에 저장

2. **MBTI별 투자 성향 통계**
   - MBTI별 평균 위험점수
   - MBTI별 평균 목표수익률
   - 투자유형 / 투자기간 / 손실감내도 분포

3. **K-Means AI 투자 성향 분석**
   - `risk_score`, `target_return`, `investment_period`, `loss_tolerance` 사용
   - 범주형 데이터 숫자 변환
   - `StandardScaler` 표준화
   - K-Means 3개 군집 생성
   - 평균 위험점수를 기준으로 안정/균형/공격 군집으로 해석
   - 사용자 이름을 입력하면 해당 사용자의 군집 결과 출력

## DB 테이블

### mbti_users
- user_id
- name
- mbti
- age_group

### investment_tests
- test_id
- user_id
- risk_score
- investment_type
- investment_period
- loss_tolerance
- target_return

## 실행 준비

```bash
pip install -r requirements.txt
```

`.env.example`을 참고해 프로젝트 루트에 `.env` 파일을 만들고 Supabase 정보를 입력합니다.

```text
SUPABASE_URL=...
SUPABASE_KEY=...
```

## 실행

```bash
python main.py
```

## K-Means 분석 주의사항

- 투자성향 검사를 완료한 사용자가 최소 3명 필요합니다.
- K-Means의 cluster 번호(0, 1, 2)는 자체 의미가 없으므로 평균 위험점수 순으로 안정/균형/공격 군집이라는 해석 이름을 붙입니다.
- MBTI는 K-Means 입력 특성으로 사용하지 않습니다. 군집 분석 이후 MBTI 분포를 비교하는 용도로 사용합니다.
- 군집 결과는 현재 수집된 표본의 패턴이며, MBTI가 투자 성향을 결정한다는 의미가 아닙니다.
