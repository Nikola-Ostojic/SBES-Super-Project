from models import Page,Question,Answer

def calculate_result(result):
    BP, F1 = calculate_first_page(result)
    F2 = calculate_second_page(result)
    F3 = calculate_third_page(result)
    F4 = calculate_fourth_page(result)
    F5, F6 = calculate_fifth_page(result)

    result = BP * F1 * F2 * F3 * F4 * F5 * F6
    result = "{:,.2f}".format(result)
    return  result

def calculate_first_page(result):
    temp = int(result['answer-1-4-1']) or 0
    if temp <= 4_000_000:
        BP = 800
    elif temp <= 8_000_000:
        BP = 1_300
    elif temp <= 20_000_000:
        BP = 2_500
    else:
        BP = 4_000

    factor = 0

    # Question 5
    factor += int(result['answer-1-5-1'] or 0) or 0
    factor += int(result['answer-1-5-2'] or 0) or 0
    factor += int(result['answer-1-5-3'] or 0) or 0
    factor += int(result['answer-1-5-4'] or 0) or 0
    factor += int(result['answer-1-5-5'] or 0) or 0
    factor += int(result['answer-1-5-6'] or 0) or 0

    # Question 6
    temp = int(result['answer-1-6-1']) or 0

    if temp <= 4:
        factor += 0
    elif temp <= 20:
        factor += 1
    elif temp <= 50:
        factor += 2
    elif temp <= 100:
        factor += 5
    elif temp > 100:
        factor += 10

    #Question 7 - 11
    for i in range(7, 12):
        factor += int(result['answer-1-' + str(i)] or 0) or 0

    #Question 12
    for i in range(1, 5):
        factor += int(result['answer-1-12-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return BP, final_factor

def calculate_second_page(result):
    factor = 0

    #Question 1
    factor += 15 if result['answer-2-1-1'] == None else 0
    factor += 15 if result['answer-2-1-2'] == None else 0

    #Question 2
    factor += int(result['answer-2-2'] or 0)

    #Question 3
    temp = int(result['answer-2-3-1'] or 0)
    if temp >= 2 and temp <= 5:
        factor += 5
    elif temp > 5:
        factor += 10

    #Question 4
    for i in range(1, 6):
        factor += 10 if result['answer-2-4-' + str(i)] == None else 0

    return get_factor_by_value(factor)


def calculate_third_page(result):
    factor = 0

    #Question 1-2
    factor += int(result['answer-3-1'] or 0)
    factor += int(result['answer-3-2'] or 0)

    #Question 3
    for i in range(1, 5):
        factor += 8 if result['answer-3-3-' + str(i)] == None else 0

    #Question 4-9
    for i in range(4, 10):
        factor += int(result['answer-3-' + str(i)] or 0)

    return get_factor_by_value(factor)


def calculate_fourth_page(result):
    factor = 1
    for i in range(1, 4):
        factor *= float(result['answer-4-' + str(i)] or 1)

    return factor


def calculate_fifth_page(result):
    #Question 1
    temp = int(result['answer-5-1-1'] or 0)
    if temp <= 500_000:
        F5 = 0.8
    elif temp <= 1_000_000:
        F5 = 1
    elif temp <= 2_000_000:
        F5 = 1.15
    elif temp <= 3_000_000:
        F5 = 1.25
    elif temp <= 4_000_000:
        F5 = 1.35
    else:
        F5 = 1.45

    temp = int(result['answer-5-2-1'] or 0)
    F6 = temp * 0.1 + 1

    return F5, F6

def get_factor_by_value(value):
    if value <= 10:
        return 0.8
    elif value <= 20:
        return 0.9
    elif value <= 50:
        return 1.0
    elif value <= 80:
        return 1.3
    elif value <= 100:
        return 1.5
    else:
        return -1



