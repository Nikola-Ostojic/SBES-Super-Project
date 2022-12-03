import uuid

class Page:
    def __init__(self, index,title, formula, questions = None):
        self.index = index
        self.title = title        
        self.formula = formula
        self.questions = questions if questions else []


class Question:
    def __init__(self,question,answer_type, weight_type, answers = None, id = None):
        self.id = id if id else str(uuid.uuid4())
        self.question = question
        self.answer_type = answer_type
        self.weight_type = weight_type
        self.answers = answers if answers else []
        

class Answer:
    def __init__(self,text,weight,id = None):
        self.id = id if id else str(uuid.uuid4())
        self.text = text
        self.weight = weight



