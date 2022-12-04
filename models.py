import uuid

class Page:
    def __init__(self, index,title, formula, questions = None):
        self.index = index
        self.title = title        
        self.formula = formula
        self.questions = questions if questions else []


class Question:
    def __init__(self,index,question,answer_type, weight_type, answers = None):
        self.index = index
        self.question = question
        self.answer_type = answer_type
        self.weight_type = weight_type
        self.answers = answers if answers else []
        

class Answer:
    def __init__(self,index,text,weight):
        self.index = index
        self.text = text
        self.weight = weight



