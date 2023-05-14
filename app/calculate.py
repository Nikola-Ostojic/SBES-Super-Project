from models import Odgovor, Page,Question,Answer
from database import insert_row
from mappings import KeyToColumnNameMappings

def calculate_result(database,result):
    if database:
        row = retrieve_all_answers(result)
        insert_row(database, row)

        BP, F1 = calculate_first_page(result)
        F2 = calculate_second_page(result)
        F3 = calculate_third_page(result)
        F4 = calculate_fourth_page(result)
        F5, F6 = calculate_fifth_page(result)

        res = BP * F1 * F2 * F3 * F4 * F5 * F6
        res = "{:,.2f}".format(res)

        ret_val = {
            "result" : res,
            "BP" : BP,
            "Factor1" : F1,
            "Factor2" : F2,
            "Factor3" : F3,
            "Factor4" : F4,
            "Factor5" : F5,
            "Factor6" : F6,
        }

        return ret_val
    else:
        return None

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


def retrieve_all_answers(result):
    row = {}

    # Questions 1 - 3
    for i in range(1, 4):
        value = result['answer-1-' + str(i) + '-1']
        row['answer-1-' + str(i)] = value

    # Question 4
    value = int(result['answer-1-4-1'] or 0)
    row['answer-1-4'] = value

    #Question 5
    row['answer-1-5'] = multiple_choices_answers(result, 'answer-1-5', 1, 6)

    # Question 6
    row['answer-1-6'] = int(result['answer-1-6-1'] or 0)

    # Questions 7 - 11
    for i in range(7, 12):
        row['answer-1-' + str(i)] = yes_no_answers(result, 'answer-1-' + str(i))

    # Question 12
    row['answer-1-12'] = multiple_choices_answers(result, 'answer-1-12', 1, 4)

        # PAGE 2

    # Question 1
    row['answer-2-1'] = ''
    if result['answer-2-1-1'] == None:
        row['answer-2-1'] += '1,'
    if result['answer-2-1-1'] == None:
        row['answer-2-1'] += '2,'

    if row['answer-2-1'] != '':
        row['answer-2-1'] = row['answer-2-1'][:-1]

    # Question 2
    row['answer-2-2'] = yes_no_answers(result, 'answer-2-2')

    # Question 3
    row['answer-2-3'] = int(result['answer-2-3-1'] or 0)

    # Question 4
    row['answer-2-4'] = multiple_choices_answers(result, 'answer-2-4', 1, 5)

        # PAGE 3

    # Question 1 - 2
    for i in range(1, 3):
        if yes_no_answers(result, 'answer-3-' + str(i)) == Odgovor.Da:
            row['answer-3-' + str(i)] = Odgovor.Ne.value
        else:
            row['answer-3-' + str(i)] = Odgovor.Da.value

    # Question 3
    row['answer-3-3'] = multiple_choices_answers(result, 'answer-3-3', 1, 4)

    # Questions 4 - 9
    for i in range(4, 10):
        if yes_no_answers(result, 'answer-3-' + str(i)) == Odgovor.Da:
            row['answer-3-' + str(i)] = Odgovor.Ne.value
        else:
            row['answer-3-' + str(i)] = Odgovor.Da.value

        # PAGE 4

    # Qusetion 1
    if float(result['answer-4-1']) == 1:
        row['answer-4-1'] = Odgovor.Da.value
    else:
        row['answer-4-1'] = Odgovor.Ne.value

    # Qusetion 2
    if float(result['answer-4-2']) == 1.5:
        row['answer-4-2'] = Odgovor.Ne.value
    else:
        row['answer-4-2'] = Odgovor.Da.value

    # Qusetion 3
    if float(result['answer-4-3']) == 1:
        row['answer-4-3'] = Odgovor.Ne.value
    else:
        row['answer-4-3'] = Odgovor.Da.value


        # PAGE 5

    # Question 1
    row['answer-5-1'] = int(result['answer-5-1-1'] or 0)

    # Question 2
    row['answer-5-2'] = int(result['answer-5-2-1'] or 0)

    print(row, flush=True)

    return row



def set_calculative_values(row,BP,F1,F2,F3,F4,F5,F6):
    row['BaznaPremija'] = BP
    row['Faktor1'] = F1
    row['Faktor2'] = F2
    row['Faktor3'] = F3
    row['Faktor4'] = F4
    row['Faktor5'] = F5
    row['Faktor6'] = F6

def multiple_choices_answers(result, answer, from_idx, to_idx):
    res = ''
    for i in range(from_idx, to_idx + 1):
        if int(result[str(answer) + '-' + str(i)] or -1) != -1:
            res += str(i) + ','
    res = res[:-1]
    return res

def yes_no_answers(result, answer):
    print(answer, flush=True)
    if int(result[answer] or 0) == 0:
        value = Odgovor.Ne.value
    else:
        value = Odgovor.Da.value

    return value
