from calculate import get_answer_ids, get_answers
from models import Odgovor, Page,Question,Answer, SelectedAnswersSmall
from database import write_to_database
from mappings import KeyToColumnNameMappings
from logging import info
from db_models import Result, CheckedItem, Factor, ResultCritical
import json
from processing import parse_answers, process
from typing import Tuple

CONFIG_NAME = "config.json"

#region Critical

def calculate_result_critical(engine, result):
    if engine:
        #res_obj = retrieve_all_answers(result)

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
        if result['answer-7-2-' + str(i)]:
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

def check_answer(answer):
    if answer == None:
        return False
    elif answer == 0 or answer == '0':
        return False

    return True

def retrieve_all_answers(q_result) -> Tuple[ResultCritical, list[Answer]]:
    info(str(q_result))
    result = ResultCritical()

    #PAGE 1
    result.Naziv = q_result.get('answer-1-1-1') if q_result.get('answer-1-1-1') else ''
    result.Adresa = q_result.get('answer-1-2-1') if q_result.get('answer-1-2-1') else ''
    result.Telefon = q_result.get('answer-1-3-1') if q_result.get('answer-1-3-1') else ''
    result.GodisnjiPrihodi = int(q_result.get('answer-1-4-1')) if check_answer(q_result.get('answer-1-4-1')) else 0
    result.BrojZaposlenih = int(q_result.get('answer-1-5-1')) if check_answer(q_result.get('answer-1-5-1')) else 0

    result.PristupPoUlogama = True if check_answer(q_result.get('answer-1-6')) else False
    result.PracenjeAktivZapos = True if check_answer(q_result.get('answer-1-7')) else False
    result.EdukacijaZapos = True if check_answer(q_result.get('answer-1-8')) else False
    result.NDAZakon = True if check_answer(q_result.get('answer-1-9')) else False
    result.ObukeZapos = True if check_answer(q_result.get('answer-1-10'))  else False

    #PAGE 2
    result.KlasifPodataka = True if check_answer(q_result.get('answer-2-1')) else False
    result.DozvoljeniNosaci = True if check_answer(q_result.get('answer-2-2')) else False
    result.PrivatniNosaci = True if check_answer(q_result.get('answer-2-3')) else False
    result.SifrovanjePodat = True if check_answer(q_result.get('answer-2-4')) else False
    result.EnkriptovanaBaza = True if check_answer(q_result.get('answer-2-5'))  else False
    result.EndToEndEnkrip = True if check_answer(q_result.get('answer-2-6'))  else False
    result.VPN = True if check_answer(q_result.get('answer-2-7'))  else False

    #PAGE 3
    result.KreiranjeIUkidanjeNaloga = True if check_answer(q_result.get('answer-3-1'))  else False
    result.LozinkaZaPristup = True if check_answer(q_result.get('answer-3-2'))  else False
    result.DvofaktorskaAutent = True if check_answer(q_result.get('answer-3-3'))  else False
    result.DigitalniSert = True if check_answer(q_result.get('answer-3-4'))  else False
    result.PravilaSifri = True if check_answer(q_result.get('answer-3-5'))  else False
    result.InicijalnaSifra = True if check_answer(q_result.get('answer-3-6'))  else False
    result.PromenaNalogaDS = True if check_answer(q_result.get('answer-3-7'))  else False
    result.PristupNaZahtev = True if check_answer(q_result.get('answer-3-8'))  else False
    result.NajnizePrivil = True if check_answer(q_result.get('answer-3-9'))  else False
    result.InstalacijaDodatnogSoft = True if check_answer(q_result.get('answer-3-10'))  else False

    #PAGE 4
    result.LokalizovaniServ = True if check_answer(q_result.get('answer-4-1'))  else False
    result.OgranicenPristupServ = True if check_answer(q_result.get('answer-4-2'))  else False
    result.ZasticeniServ = True if check_answer(q_result.get('answer-4-3'))  else False
    result.FizickoZasticeniServ = True if check_answer(q_result.get('answer-4-4'))  else False
    result.ElektromegnetnoZrac = True if check_answer(q_result.get('answer-4-5'))  else False
    result.UPS = True if check_answer(q_result.get('answer-4-6'))  else False

    #PAGE 5
    result.Sesija = True if check_answer(q_result.get('answer-5-1'))  else False
    result.AzuriranjeSoft = True if check_answer(q_result.get('answer-5-2'))  else False
    result.AntivirusFirewall = True if check_answer(q_result.get('answer-5-3'))  else False
    result.BlokiraniPortovi = True if check_answer(q_result.get('answer-5-4'))  else False
    result.DMZ = True if check_answer(q_result.get('answer-5-5'))  else False
    result.BastionServeri = True if check_answer(q_result.get('answer-5-6'))  else False
    result.IDSIPS = True if check_answer(q_result.get('answer-5-7'))  else False

    #PAGE 6
    result.RezervneKopije = True if check_answer(q_result.get('answer-6-1'))  else False
    result.DnevneKopije = True if check_answer(q_result.get('answer-6-2'))  else False
    result.SedmicneKopije = True if check_answer(q_result.get('answer-6-3'))  else False
    result.MesecneKopije = True if check_answer(q_result.get('answer-6-4'))  else False
    result.GodisnjeKopije = True if check_answer(q_result.get('answer-6-5'))  else False

    #PAGE 7
    result.LogAktivnostiKoris = True if check_answer(q_result.get('answer-7-1'))  else False
    answer_ids = get_answer_ids(q_result, 'answer-7-2', 1, 6)
    answers = get_answers("critical", 7, 2, answer_ids)
    result.CuvanjeLogova = True if check_answer(q_result.get('answer-7-3'))  else False
    result.PenetrationTesting = True if check_answer(q_result.get('answer-7-4'))  else False
    result.ProcUpravljanjemIncid = True if check_answer(q_result.get('answer-7-5'))  else False
    result.ProcTestiranja = True if check_answer(q_result.get('answer-7-6'))  else False
    result.AzuriranjeTestiranja = True if check_answer(q_result.get('answer-7-7'))  else False
    result.ProcZaOporavak = True if check_answer(q_result.get('answer-7-8'))  else False
    result.PrijavaCERTu = True if check_answer(q_result.get('answer-7-9'))  else False

    #PAGE 8
    result.ZeljeniIznosNaknade = int(q_result.get('answer-8-1-1')) if check_answer(q_result.get('answer-8-1-1')) else 0
    result.BrojIncidenata = int(q_result.get('answer-8-2-1')) if check_answer(q_result.get('answer-8-2-1')) else 0


    return result, answers
