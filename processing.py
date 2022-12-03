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
    id = answer['id'] if 'id' in answer else None
    text = answer['text']
    weight = answer['weight']
    return Answer(text,weight, id)

def parse_question(question):
    id = question['id'] if 'id' in question else None
    q = question['question']
    answer_type = question['answerType']
    weight_type = question['weightType']
    return Question(q,answer_type,weight_type,id)

def parse_page(page):
    index = page['index']
    title = page['title']    
    formula = page['formula']
    return Page(index,title,formula)


def add_page_to_json(config_name,index,title,formula):
    try:
        config_data = json.load(open(config_name, 'r'))
        data = {"index":int(index),"title":str(title),"formula":str(formula)}
        config_data['pages'].append(data)

        json_data = json.dumps(config_data)
        with open(config_name, "w") as file:
            file.write(json_data)        
        return True
    except Exception as e:
        print(str(e), flush=True)
        return False