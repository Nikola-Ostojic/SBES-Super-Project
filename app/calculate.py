from models import Odgovor, Page,Question,Answer, SelectedAnswersSmall
from database import write_to_database
from mappings import KeyToColumnNameMappings
from logging import info
from db_models import Result, CheckedItem, Factor
import json
from processing import parse_answers, process
from typing import Tuple

CONFIG_NAME = "config.json"

def extract_all_answers(questionnaire) -> list[Answer]:
    answers = []
    res = process(CONFIG_NAME, questionnaire)

    for page in res:
        for question in page.questions:
            if question.answer_type == 'checkbox':
                for answer in question.answers:
                    answers.append(answer)

    return answers


#region Small

def calculate_result(engine, result):
    if engine:
        res_obj, selected_answers = retrieve_all_answers(result)

        BP, F1 = calculate_first_page(result)
        F2 = calculate_second_page(result)
        F3 = calculate_third_page(result)
        F4 = calculate_fourth_page(result)
        F5, F6 = calculate_fifth_page(result)

        res = BP * F1 * F2 * F3 * F4 * F5 * F6
        res = "{:,.2f}".format(res)

        ret_val = {
                "result": res,
                "BP": BP,
                "Factor1": F1,
                "Factor2": F2,
                "Factor3": F3,
                "Factor4": F4,
                "Factor5": F5,
                "Factor6": F6,
                }

        info(result)

        factor = Factor()
        factor.BaznaPremija = BP
        factor.Factor1 = F1
        factor.Factor2 = F2
        factor.Factor3 = F3
        factor.Factor4 = F4
        factor.Factor5 = F5
        factor.Factor6 = F6

        all_answers = extract_all_answers("small")

        write_to_database(engine, res_obj, factor, all_answers, selected_answers)

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

def retrieve_all_answers(q_result) -> Tuple[Result, list[Answer]]:
    info(str(q_result))
    result = Result()

    result.Naziv = q_result.get('answer-1-1-1') if q_result.get('answer-1-1-1') else ''
    result.Adresa = q_result.get('answer-1-2-1') if q_result.get('answer-1-2-1') else ''
    result.Telefon = q_result.get('answer-1-3-1') if q_result.get('answer-1-3-1') else ''
    result.GodisnjiPrihodi = int(q_result.get('answer-1-4-1')) if check_answer(q_result.get('answer-1-4-1')) else 0

    # Question 5 TODO
    answer_ids = get_answer_ids(q_result, 'answer-1-5', 1, 6)
    pg1_q5_answers = get_answers("small", 1, 5, answer_ids)


    # Question 6
    result.BrojZaposlenih = int(q_result.get('answer-1-6-1')) if check_answer(q_result.get('answer-1-6-1')) else 0

    # Questions 7 - 11
    result.FinansijskiPZ = True if check_answer(q_result.get('answer-1-7')) else False
    result.FinansijskiPK = True if check_answer(q_result.get('answer-1-8')) else False
    result.LicniPK = True if check_answer(q_result.get('answer-1-9')) else False
    result.MedicinskiPK = True if check_answer(q_result.get('answer-1-10'))  else False
    result.DeljenjePK = True if check_answer(q_result.get('answer-1-11'))  else False


    # Question 12
    # row['answer-1-12'] = get_answer_ids(result, 'answer-1-12', 1, 4)
    # 1, 3 , 5
    answer_ids = get_answer_ids(q_result, 'answer-1-12', 1, 4)
    pg1_q12_answers = get_answers("small", 1, 12, answer_ids)


    # PAGE 2

    answer_ids = get_answer_ids(q_result, 'answer-2-1', 1, 3)
    pg2_q1_answers = get_answers("small", 1, 12, answer_ids)

    # Question 2
    result.Websajt = True if check_answer(q_result.get('answer-1-11')) else False

    # Question 3
    result.BrojJavnihURL = int(q_result.get('answer-2-3-1')) if check_answer(q_result.get('answer-2-3-1')) else 0

    # Question 4
    # row['answer-2-4'] = get_answer_ids(result, 'answer-2-4', 1, 5)
    answer_ids = get_answer_ids(q_result, 'answer-2-4', 1, 5)
    pg2_q4_answers = get_answers("small", 1, 12, answer_ids)

    # PAGE 3

    # Question 1 - 2
    result.PolitikaPrivatnosti = True if check_answer(q_result.get('answer-3-1')) else False
    result.PolitikaZadrzavanjaIBrisanja = True if check_answer(q_result.get('answer-3-2')) else False

    # Question 3
    # row['answer-3-3'] = get_answer_ids(result, 'answer-3-3', 1, 4)
    answer_ids = get_answer_ids(q_result, 'answer-2-4', 1, 4)
    pg3_q3_answers = get_answers("small", 1, 12, answer_ids)

    # Questions 4 - 9
    result.ObukaIB =  True if check_answer(q_result.get('answer-3-4')) else False
    result.BezbednosniTestovi = True if check_answer(q_result.get('answer-3-5')) else False
    result.PlanReagovanjaNaIncident = True if check_answer(q_result.get('answer-3-5')) else False
    result.PlanOporavka = True if check_answer(q_result.get('answer-3-6')) else False
    result.KreiranjeRezervnihKopija = True if check_answer(q_result.get('answer-3-7')) else False
    result.BezbednoSkladistenjePodataka = True if check_answer(q_result.get('answer-3-8')) else False

    # PAGE 4

    print("TEST", flush=True)
    print(str(q_result.get('answer-4-1')), flush=True)
    print(str(q_result.get('answer-4-2')), flush=True)
    print(str(q_result.get('answer-4-3')), flush=True)
    print("TEST", flush=True)

    result.ZakonPOLPP = True if check_answer(q_result.get('answer-4-1')) else False
    result.Pcidss = True if check_answer(q_result.get('answer-4-2')) else False
    result.Iso27001 = True if check_answer(q_result.get('answer-4-3')) else False


    # PAGE 5

    # Question 1
    result.ZeljeniIznosNaknade = int(q_result.get('answer-5-1-1')) if check_answer(q_result.get('answer-5-1-1')) else 0

        # Question 2
    result.BrojIncidenata = int(q_result.get('answer-5-2-1')) if check_answer(q_result.get('answer-5-2-1')) else 0

    answers = pg2_q1_answers + pg3_q3_answers + pg2_q4_answers + pg1_q5_answers + pg1_q12_answers

    return result, answers

def set_calculative_values(row,BP,F1,F2,F3,F4,F5,F6):
    row['BaznaPremija'] = BP
    row['Faktor1'] = F1
    row['Faktor2'] = F2
    row['Faktor3'] = F3
    row['Faktor4'] = F4
    row['Faktor5'] = F5
    row['Faktor6'] = F6

#endregion



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

def get_answer_ids(result, answer, from_idx, to_idx):
    res = []
    for i in range(from_idx, to_idx + 1):
        r = result.get(str(answer) + '-' + str(i))
        if r:
            res.append(int(i))
    return res

def yes_no_answers(result, answer):
    if int(result[answer] or 0) == 0:
        return False
    else:
        return True

#   print(answer, flush=True)
#   if int(result[answer] or 0) == 0:
#       value = Odgovor.Ne.value
#   else:
#       value = Odgovor.Da.value
#
#     return value


def check_answer(answer):
    if answer == None:
        return False
    elif answer == 0 or answer == '0':
        return False

    return True


def get_answers(questionnaire, page, question, indexes) -> list[Answer]:
    result = []
    page = page-1
    question = question-1
    # da bi u funkciji mogla da se koristi realna brojka pitanja
    res = process(CONFIG_NAME, questionnaire)
    question = res[page].questions[question]
    for index in indexes:
        for anw in question.answers:
            if anw.id == index:
                result.append(anw)
    return result


