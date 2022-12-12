import uuid

class Page:
    def __init__(self, id, index,title, questions = None):
        self.id = id
        self.index = index
        self.title = title                
        self.questions = questions if questions else []


class Question:
    def __init__(self, id, index, question, answer_type, answers = None):
        self.id = id
        self.index = index
        self.question = question
        self.answer_type = answer_type
        self.answers = answers if answers else []
        

class Answer:
    def __init__(self, id, index, text, weight):
        self.id = id
        self.index = index
        self.text = text
        self.weight = weight



