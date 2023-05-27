from models import Odgovor, Page,Question,Answer, SelectedAnswersSmall
from database import write_to_database
from mappings import KeyToColumnNameMappings
from logging import info
from db_models import Result, CheckedItem, Factor
import json
from processing import parse_answers, process
from typing import Tuple

CONFIG_NAME = "config.json"

#region Critical

def calculate_result_critical(engine, result):
    if engine:
        BP, F1 = calculate_first_page_critical(result)
        F2 = calculate_second_page_critical(result)
        F3 = calculate_third_page_critical(result)
        F4 = calculate_fourth_page_critical(result)
        F5 = calculate_fifth_page_critical(result)
        F6 = calculate_sixth_page_critical(result)
        F7 = calculate_seventh_page_critical(result)
        F8, F9 = calculate_eighth_page_critical(result)
              
        res = BP * F1 * F2 * F3 * F4 * F5 * F6 * F7 * F8 * F9

        ret_val = {
                "result": round(res, 2),
                "BP": BP,
                "Factor1": F1,
                "Factor2": F2,
                "Factor3": F3,
                "Factor4": F4,
                "Factor5": F5,
                "Factor6": F6,
                "Factor7": F7,
                "Factor8": F8,
                "Factor9": F9,
                }
        
        return ret_val
        
    else:
        return None

def calculate_first_page_critical(result):
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

    temp = int(result['answer-1-5-1']) or 0

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

    for i in range(6, 11):
        factor += int(result['answer-1-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return BP, final_factor

def calculate_second_page_critical(result):
    factor = 0

    for i in range(1, 8):
        factor += int(result['answer-2-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return final_factor

def calculate_third_page_critical(result):
    factor = 0

    for i in range(1, 11):
        factor += int(result['answer-3-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return final_factor

def calculate_fourth_page_critical(result):
    factor = 0

    for i in range(1, 7):
        factor += int(result['answer-4-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return final_factor

def calculate_fifth_page_critical(result):
    factor = 0

    for i in range(1, 8):
        factor += int(result['answer-5-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return final_factor

def calculate_sixth_page_critical(result):
    factor = 0

    for i in range(1, 6):
        factor += int(result['answer-6-' + str(i)] or 0) or 0

    final_factor = get_factor_by_value(factor)

    return final_factor

def calculate_seventh_page_critical(result):
    factor = 0

    for i in range(1, 10):
        if i == 2:
            continue
        factor += int(result['answer-7-' + str(i)] or 0) or 0

    factor += 15
    for i in range(1, 5):
        print('ovde je for......', flush=True)
        if result['answer-7-2-' + str(i)]:
            print('ovde je uslo......', flush=True)
            factor -= int(result['answer-7-2-' + str(i)] or 0) or 0    
        

    final_factor = get_factor_by_value(factor)

    return final_factor

def calculate_eighth_page_critical(result):
    #Question 1
    temp = int(result['answer-8-1-1'] or 0)
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

    temp = int(result['answer-8-2-1'] or 0)
    F6 = temp * 0.1 + 1

    return F5, F6

#endregion

def get_factor_by_value(value):
    if value <= 10:
        return 0.9
    elif value <= 20:
        return 0.95
    elif value <= 50:
        return 1.0
    elif value <= 80:
        return 1.1
    elif value <= 100:
        return 1.2
    else:
        return -1