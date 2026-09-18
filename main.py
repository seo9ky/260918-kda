from investment import run_investment_test


def main():

    while True:

        print("\n================================")
        print("       투자성향 분석 프로그램")
        print("================================")
        print("1. 투자성향 검사")
        print("2. 종료")
        print("================================")

        choice = input("메뉴를 선택하세요: ")

        # 투자성향 검사
        if choice == "1":

            run_investment_test()

        # 종료
        elif choice == "2":

            print("\n프로그램을 종료합니다.")
            break

        else:

            print("\n❌ 잘못된 메뉴입니다.")
            print("1~2 중에서 선택해주세요.")


if __name__ == "__main__":
    main()