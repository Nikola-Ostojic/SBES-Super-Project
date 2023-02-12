from flask import Flask, render_template, url_for,request, session, redirect
from flask_session import Session
from calculate import calculate_result
from processing import process, edit_page_json,edit_question_json, edit_answer_json, add_answer_to_json
from models import Page
from database import get_database_instance, init_database

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 1800
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CONFIG_NAME = "config.json"

database = get_database_instance()
init_database(database)


@app.route('/')
@app.route('/home')
def home():        
    pages = None
    if not session.get("pages"):
        pages = process(CONFIG_NAME)            
        session['pages'] = pages
    else:  
        pages = session.get('pages')        
    
    app.logger.info(pages)
    app.logger.info(type(pages))

    html = render_template("questionnaire.html", pages=pages)
    return html


@app.route('/admin')
def admin():    
    pages = process(CONFIG_NAME)
    return render_template("admin.html", pages=pages)

@app.route('/editPage', methods=["POST"])
def edit_page():
    page_id = request.form.get('pageId')
    index = request.form.get('index')
    title = request.form.get('title')

    success = edit_page_json(CONFIG_NAME, page_id, index, title)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response    

@app.route('/editQuestion', methods=["POST"])
def edit_question():
    page_id = request.form.get('pageId')
    question_id = request.form.get('questionId')
    question_index = request.form.get('index')
    question = request.form.get('question')
    answer_type = request.form.get('answerType')

    success = edit_question_json(CONFIG_NAME, page_id, question_id,question_index,question,answer_type)
    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response    

@app.route('/editAnswer', methods=['POST'])
def edit_answer():
    page_id = request.form.get('pageId')
    question_id = request.form.get('questionId')
    answer_id = request.form.get('answerId')
    answer_index = request.form.get('index')
    text = request.form.get('answer')
    weight = request.form.get('weight')
 

    success = edit_answer_json(CONFIG_NAME, page_id,question_id, answer_id,answer_index,text,weight)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response       


# @app.route('/addPage', methods=["POST"])
# def add_page():
#     index = request.form.get('pageIndex')
#     title = request.form.get('title')
#     formula = request.form.get('formula')

#     success = add_page_to_json(CONFIG_NAME,index,title,formula)

#     response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
#     return response

# @app.route('/addQuestion', methods=["POST"])
# def add_question():
#     page_index = request.form.get('pageIndex')
#     question_index = request.form.get('questionIndex')
#     question = request.form.get('question')
#     answer_type = request.form.get('answerType')
#     weight_type = request.form.get('weightType')

#     app.logger.info(page_index)    

#     success = add_question_to_json(CONFIG_NAME,page_index,question_index,question,answer_type,weight_type)

#     response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
#     return response

@app.route('/addAnswer', methods=["POST"])
def add_answer():
    page_id = request.form.get('pageId')
    question_id = request.form.get('questionId')
    answer_index = request.form.get('index')
    text = request.form.get('answer')
    weight = request.form.get('weight')

    success = add_answer_to_json(CONFIG_NAME, page_id,question_id,answer_index,text,weight)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response


@app.route('/result', methods=["POST", "GET"])
def result():

    if request.method == 'GET':
        if session.get('result'):
            return render_template('result.html', result=session['result'], company=session['company'])
        else:
            return redirect('home.html', pages=pages)    
        
    if not session.get("pages"):
        return "Session expired, please fill out the form again. Sorry for the inconvenience."

    pages = session.get("pages") 

    res = {}
    for page in pages:
        for question in page.questions:
            for answer in question.answers:                
                name = 'answer-' + str(page.id) + '-' + str(question.id)
                if question.answer_type != 'radio':
                    name += '-' + str(answer.id)
                res[name] = request.form.get(name)

    result = calculate_result(database,res)
    company = res['answer-1-1-1']

    session['result'] = result
    session['company'] = company
    response = app.response_class(response="OK" if result else "ERR",status=200 if res else 400)
    return response


if __name__ == '__main__':    
    app.run(debug=True, port=5000, host='0.0.0.0')
