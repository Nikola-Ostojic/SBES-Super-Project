from models import Page,Question,Answer
import json

def process(config_name):
    json_data = json.load(open(config_name, 'r'))
    formula = json_data['formula']
    pages = parse_pages(json_data['pages'])
    return formula, pages


def parse_pages(pages):
    result = []
    for page in pages:        
        pg = parse_page(page)
        for question in page['questions']:
            q = parse_question(question)            
            pg.questions.append(q)
            for answer in question['answers']:                
                answ = parse_answer(answer)
                q.answers.append(answ)
        result.append(pg)
    return result

def parse_answer(answer):
    id = answer['id']
    index = answer['index']
    text = answer['text']
    weight = answer['weight']
    return Answer(id,index,text,weight)

def parse_question(question):
    id = question['id']
    index = question['index']
    q = question['question']
    answer_type = question['answerType']
    weight_type = question['weightType']
    return Question(id,index,q,answer_type,weight_type)

def parse_page(page):
    id = page['id']
    index = page['index']
    title = page['title']    
    formula = page['formula']
    return Page(id,index,title,formula)


def add_page_to_json(config_name,index,title,formula):
    try:
        config_data = json.load(open(config_name, 'r'))
        data = {"index":int(index),"title":str(title),"formula":str(formula),"questions":[]}
        config_data['pages'].append(data)

        json_data = json.dumps(config_data)
        with open(config_name, "w") as file:
            file.write(json_data)        
        return True
    except Exception as e:
        print(str(e), flush=True)
        return False

def add_question_to_json(config_name,page_index,question_index,question,answer_type,weight_type):
    try:
        config_data = json.load(open(config_name,'r'))
        data = {"index":int(question_index),"question":str(question),"answerType":str(answer_type),"weightType":str(weight_type),"answers":[]}

        found_index, page_idx = get_page_json(config_data['pages'],page_index)
        if found_index == False: raise Exception("Page index not found.")
     
        config_data['pages'][int(page_idx)]['questions'].append(data)
        
        json_data = json.dumps(config_data)

        with open(config_name, "w") as file:
            file.write(json_data)
        return True
        
    except Exception as e:
        print(str(e), flush=True)
        return False

def add_answer_to_json(config_name,page_index,question_index,answer_index,text,weight):
    try:
        config_data = json.load(open(config_name,'r'))
        data = {"index":int(answer_index),"text":str(text),"weight":float(weight)}

        found_index, page_idx = get_page_json(config_data['pages'], page_index)
        if found_index == False: raise Exception("Page index not found.")

        found_index, question_idx = get_page_json(config_data['pages'][page_idx]['questions'],question_index)
        if found_index == False: raise Exception("Question index not found.")
        
        config_data['pages'][int(page_idx)]['questions'][int(question_idx)]['answers'].append(data)
        json_data = json.dumps(config_data)

        with open(config_name, "w") as file:
            file.write(json_data)
        return True
        
    except Exception as e:
        print(str(e), flush=True)
        return False 


def get_page_json(items,index):    
    counter = 0
    for item in items:
        if int(item['index']) == int(index):
            return True,counter
        counter += 1
    
    return False,counter




    