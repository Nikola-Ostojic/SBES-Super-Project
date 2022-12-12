from models import Page,Question,Answer
import json

def process(config_name):
    json_data = json.load(open(config_name, 'r'))    
    pages = parse_pages(json_data['pages'])
    return pages


def parse_pages(pages):
    result = []
    for page in pages:        
        pg = parse_page(page)
        for question in page['questions']:
            q = parse_question(question)  
            print(pg, flush=True)          
            print(pg.questions, flush=True)                      
            print(type(pg.questions), flush=True)                      
            print(q, flush=True)          
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
    return Question(id,index,q,answer_type)

def parse_page(page):
    id = page['id']
    index = page['index']
    title = page['title']        
    return Page(id,index,title)

def edit_page_json(config_name,id,index,title):
    try:        
        config_data = json.load(open(config_name,'r'))
        
        found_index, page_idx = get_id_json(config_data['pages'], id)        
        if found_index == False: raise Exception("Page id not found.")
        
        page = config_data['pages'][int(page_idx)]        
        page['index'] = int(index)
        page['title'] = str(title)

        
        json_data = json.dumps(config_data)

        with open(config_name, "w") as file:
            file.write(json_data)

        return True
    except Exception as e:
        print(str(e), flush=True)
        return False


def edit_question_json(config_name, page_identifier, question_identifier, question_index, question, answer_type):
    try:        
        config_data = json.load(open(config_name,'r'))
        
        found_index, page_idx = get_id_json(config_data['pages'], page_identifier)        
        if found_index == False: raise Exception("Page id not found.")
        
        found_index, question_idx = get_id_json(config_data['pages'][int(page_idx)]['questions'], question_identifier)
        if found_index == False: raise Exception("Question id not found.")

        quest = config_data['pages'][int(page_idx)]['questions'][int(question_idx)]        
        quest['index'] = int(question_index)
        quest['question'] = str(question)
        quest['answer_type'] = str(answer_type)
        
        json_data = json.dumps(config_data)

        with open(config_name, "w") as file:
            file.write(json_data)

        return True
    except Exception as e:
        print(str(e), flush=True)
        return False

def edit_answer_json(config_name, page_identifier, question_identifier, answer_identifier, answer_index, answer, weight):
    try:        
        config_data = json.load(open(config_name,'r'))
        
        found_index, page_idx = get_id_json(config_data['pages'], page_identifier)        
        if found_index == False: raise Exception("Page id not found.")
        
        found_index, question_idx = get_id_json(config_data['pages'][int(page_idx)]['questions'], question_identifier)
        if found_index == False: raise Exception("Question id not found.")
    

        found_index, answer_idx = get_id_json(config_data['pages'][int(page_idx)]['questions'][int(question_idx)]['answers'], answer_identifier)
   
        print(answer_idx, flush=True)

        answ = config_data['pages'][int(page_idx)]['questions'][int(question_idx)]['answers'][int(answer_idx)]
        
        answ['index'] = int(answer_index)
        answ['text'] = str(answer)
        answ['weight'] = str(weight)

        print("OVDE3", flush=True)
        
        json_data = json.dumps(config_data)

        with open(config_name, "w") as file:
            file.write(json_data)

        return True
    except Exception as e:
        print(str(e), flush=True)
        return False

# def add_page_to_json(config_name,index,title,formula):
#     try:
#         config_data = json.load(open(config_name, 'r'))
#         data = {"index":int(index),"title":str(title),"formula":str(formula),"questions":[]}
#         config_data['pages'].append(data)

#         json_data = json.dumps(config_data)
#         with open(config_name, "w") as file:
#             file.write(json_data)        
#         return True
#     except Exception as e:
#         print(str(e), flush=True)
#         return False

# def add_question_to_json(config_name,page_index,question_index,question,answer_type,weight_type):
#     try:
#         config_data = json.load(open(config_name,'r'))
#         data = {"index":int(question_index),"question":str(question),"answerType":str(answer_type),"weightType":str(weight_type),"answers":[]}

#         found_index, page_idx = get_page_json(config_data['pages'],page_index)
#         if found_index == False: raise Exception("Page index not found.")
     
#         config_data['pages'][int(page_idx)]['questions'].append(data)
        
#         json_data = json.dumps(config_data)

#         with open(config_name, "w") as file:
#             file.write(json_data)
#         return True
        
#     except Exception as e:
#         print(str(e), flush=True)
#         return False

def add_answer_to_json(config_name,page_identifier,question_identifier,answer_index,text,weight):
    try:
        config_data = json.load(open(config_name,'r'))        

        print(config_data, flush=True)

        found_id, page_id = get_id_json(config_data['pages'], page_identifier)
        if found_id == False: raise Exception("Page index not found.")

        found_id, question_id = get_id_json(config_data['pages'][page_id]['questions'],question_identifier)
        if found_id == False: raise Exception("Question index not found.")
        
        new_id = len(config_data['pages'][int(page_id)]['questions'][int(question_id)]['answers']) + 1
        print("OVDEEE 2", flush=True)
        print(new_id,flush=True)
        print(answer_index,flush=True)
        data = {"id":int(new_id),"index":int(answer_index),"text":str(text),"weight":float(weight)}
        
        print("OVDEEE 4", flush=True)
        config_data['pages'][int(page_id)]['questions'][int(question_id)]['answers'].append(data)
        print("OVDEEE 5", flush=True)
        json_data = json.dumps(config_data)

        print("OVDEEE 3", flush=True)

        with open(config_name, "w") as file:
            file.write(json_data)
        return True
        
    except Exception as e:
        print(str(e), flush=True)
        return False 


def get_id_json(items,id):    
    counter = 0
    for item in items:
        if int(item['id']) == int(id):
            return True,counter
        counter += 1
    
    return False,counter




    