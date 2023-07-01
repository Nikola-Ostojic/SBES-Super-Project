from flask import request
from models import Odgovor, Page,Question,Answer, SelectedAnswersSmall
from database import write_to_database
from logging import info
from db_models import Result, CheckedItem, Factor
import json
from processing import parse_answers, process
from typing import Tuple
from typing import Dict, List, Tuple


# def extract_answers(answers):
#     extracted_answers = []

#     for answer in answers:
#         question_id = answer.id
#         answer_type = answer.answerType

#         if answer_type == 'radio':
#             selected = bool(answer.id == 1)  # True if answer with ID 1 is selected, False otherwise
#             if selected:
#                 extracted_answers.append({'id': question_id, 'text': answer.text})
#         elif answer_type == 'checkbox':
#             selected_answers = []
#             for option in answer.answers:
#                 option_id = option.id
#                 option_text = option.text
#                 selected = bool(option_id == 1)  # True if option with ID 1 is selected, False otherwise
#                 if selected:
#                     selected_answers.append({'id': option_id, 'text': option_text})
#             if selected_answers:
#                 extracted_answers.append({'id': question_id, 'answers': selected_answers})
#         elif answer_type == 'text':
#             answer_text = answer.text
#             if answer_text:
#                 extracted_answers.append({'id': question_id, 'text': answer_text})

#     return extracted_answers



CONFIG_NAME = "config2.json"

def calculate_result2(answers):
    # Load questionnaire from file
    #questionnaire = load_questionnaire_from_file(CONFIG_NAME)
    #print(questionnaire)

    # Extract all answers
    #answers = extract_all_answers(questionnaire)
    # extracted_answers = extract_answers(answers) #DODATO

    # print(extracted_answers)

    # Process answers

    risks = count_possible_risks(answers)
    retval = determine_insurance_coverage(risks)
    return retval


def load_questionnaire_from_file(config_name):
    with open(config_name, "r") as file:
        questionnaire = json.load(file)
    return questionnaire



# def extract_answers(answers):
#     extracted_answers = []

#     for answer in answers:
#         question_id = answer['id']
#         answer_type = answer.get('answerType')

#         if answer_type == 'radio':
#             selected = bool(answer['id'] == 1)
#             if selected:
#                 extracted_answers.append({'id': question_id, 'text': answer['text']})
#         elif answer_type == 'checkbox':
#             selected_answers = []
#             for option in answer['answers']:
#                 option_id = option['id']
#                 option_text = option['text']
#                 selected = bool(option_id == 1)
#                 if selected:
#                     selected_answers.append({'id': option_id, 'text': option_text})
#             if selected_answers:
#                 extracted_answers.append({'id': question_id, 'answers': selected_answers})
#         elif answer_type == 'text':
#             answer_text = answer.get('text')
#             if answer_text:
#                 extracted_answers.append({'id': question_id, 'text': answer_text})
#     print(extracted_answers)
#     return extracted_answers


def determine_insurance_coverage(risks_possible):

    if risks_possible >= 12 and risks_possible <= 16:
        return "Insurance C"
    elif risks_possible >= 6 and risks_possible <= 11:
        return "Insurance B"
    elif risks_possible >= 0 and risks_possible <= 5:
        return "Insurance A"


def count_possible_risks(answers):
    possible_risks = 0

    second_question_occurrence = 0
    third_question_occurrence = 0
    fifth_question_occurrence = 0
    twelfth_question_occurrence = 0
    thirteenth_question_occurrence = 0

    # Checking each question's answers to determine the number of possible risks
    for answer, ids in answers.items():


            separeted_answer = answer.split('-')
            last_part = separeted_answer[2]  # Extract the last part of the answer

            # question_id = question['id']
            # answer_type = question.get('answerType')
            # if answer_type == 'radio':
            #     answer = question.get('text')
            if last_part in ['1', '6', '7', '10'] and ids == '1':
                possible_risks += 1
            elif last_part in ['4', '8', '9', '11', '14', '15', '16'] and ids == '2':
                possible_risks += 1
            elif last_part == '2':
                second_question_occurrence += 1
            elif last_part == '3':
                third_question_occurrence += 1
            elif last_part == '5':
                fifth_question_occurrence += 1
            elif last_part == '12':
                twelfth_question_occurrence += 1
            elif last_part == '13':
                thirteenth_question_occurrence += 1
                # for answer in selected_answers:
                #     if answer['text'] == 'Da':
                #         possible_risks += 1
            # elif answer_type == 'checkbox':
            #     selected_answers = question.get('answers', [])
            

    if second_question_occurrence >= 1:
        possible_risks += 1
    if third_question_occurrence == 1:
        possible_risks += 1
    if fifth_question_occurrence == 1:
        possible_risks += 1
    if twelfth_question_occurrence == 1:
        possible_risks += 1
    if thirteenth_question_occurrence == 1:
        possible_risks += 1


    return possible_risks














