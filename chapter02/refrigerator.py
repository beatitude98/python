# 식품을 저장할 배열(리스트)를 하나 선언
foods = []

while True:
    print('-' * 34)
    print('1.출력|2.추가|3.삭제|4.변경|5.종료')
    print('-' * 34)
    menu = int(input('메뉴를 선택 하시오: '))
    if menu == 1:
        print(foods)
    elif menu == 2:
        food = input('추가할 식재료를 입력하세요:')
        foods.append(food)
        print(f'{food}가 추가되었습니다.')
    elif menu == 3:
        delete_food = input('삭제할 식재료를 입력하시오: ')
        if delete_food in foods:
            # 삭제할 음식이 푸드 리스트에 있냐?
            foods.remove(delete_food)
        else:
            print('삭제할 식재료가 조재하지 않음')
    elif menu == 4:
        modify_food = input('교환할 식재료를 입력하시오: ')
        if modify_food in foods:
            index = foods.index(modify_food)
            new_food = input('새로운 식재료를 입력히오: ')
            foods[index] = new_food
        else:
            print('교환할 식재료가 존재하지 않음')
    elif menu == 5:
        break