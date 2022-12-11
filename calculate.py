from models import Page,Question,Answer

def calculate_result(result):
    BP, F1 = calculate_first_page(result)

    return BP * F1

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



