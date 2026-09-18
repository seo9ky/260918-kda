from investment import run_investment_test
from analysis import run_mbti_analysis
from ai_analysis import run_ai_analysis


def main():
    while True:
        print("\n================================")
        print("     MBTI × 투자성향 분석 프로그램")
        print("================================")
        print("1. 투자성향 검사")
        print("2. MBTI별 투자 성향 통계")
        print("3. K-Means AI 투자 성향 분석")
        print("0. 종료")
        print("================================")

        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "1":
            run_investment_test()

        elif choice == "2":
            run_mbti_analysis()

        elif choice == "3":
            run_ai_analysis()

        elif choice == "0":
            print("\n프로그램을 종료합니다.")
            break

        else:
            print("\n 잘못된 메뉴입니다. 0~3 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
