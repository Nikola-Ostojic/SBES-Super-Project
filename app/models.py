import uuid
from enum import Enum

class Page:
    def __init__(self, id, index,title, questions = None):
        self.id = id
        self.index = index
        self.title = title
        self.questions:list[Question] = questions if questions else []


class Question:
    def __init__(self, id, index, question, answer_type, answers = None):
        self.id = id
        self.index = index
        self.question = question
        self.answer_type = answer_type
        self.answers:list[Answer] = answers if answers else []


class Answer:
    def __init__(self, id, index, text, weight):
        self.id = id
        self.index = index
        self.text = text
        self.weight = weight

class Odgovor(Enum):
    Ne = 0
    Da = 1
    NijeRelevantno = 2

class TipDelatnosti(Enum):
    Zemljoradnja = 1
    Industrija = 2
    Obrazovanje = 3
    Trgovina = 4
    Zdravstvo = 5
    IKTSektor = 6

class EksterneUsluge(Enum):
    Internet = 1
    SkladistenjePodataka = 2
    Marketing = 3
    Ostalo = 4

class EnkripcijaPodataka(Enum):
    Uskladitenih = 1
    UPrenosu = 2

class TehnickeMere(Enum):
    AntivirusInstaliran = 1
    DetekcijaUpadaUSistem = 2
    Firewall = 3
    MultifaktorskaAutentifikacija = 4
    PristupaZasnovanPrivilegijama = 5

class PolitikaIB(Enum):
    Internet = 1
    DrustveneMreze = 2
    ElektronskePoste = 3
    RukovanjeLozinkama = 4


class SelectedAnswersSmall:
    def __init__(self,pg1_q5, pg1_q12, pg2_q1, pg2_q4, pg3_q3):
        self.pg1_q5 = pg1_q5
        self.pg1_q12 = pg1_q12
        self.pg2_q1 = pg2_q1
        self.pg2_q4 = pg2_q4
        self.pg3_q3 = pg3_q3


class QuestionareType(Enum):
    Small = 0
    Big = 1
    Critical = 2