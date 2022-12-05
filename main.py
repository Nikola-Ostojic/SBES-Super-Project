from flask import Flask, render_template, url_for,request, session
from flask_session import Session
from processing import process,add_page_to_json,add_question_to_json, add_answer_to_json
from models import Page

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 30
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CONFIG_NAME = "config.json"

@app.route('/home')
def home():        
    pages = None
    if not session.get("pages"):
        _, pages = process(CONFIG_NAME)            
        session['pages'] = pages
    else:  
        pages = session.get('pages')
    
    
    app.logger.info(pages)
    app.logger.info(type(pages))

    html = render_template("questionnaire.html", pages=pages)
    return html


@app.route('/admin')
def admin():    
    _ , pages = process(CONFIG_NAME)
    return render_template("admin.html", pages=pages)

@app.route('/addPage', methods=["POST"])
def add_page():
    index = request.form.get('pageIndex')
    title = request.form.get('title')
    formula = request.form.get('formula')

    success = add_page_to_json(CONFIG_NAME,index,title,formula)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response

@app.route('/addQuestion', methods=["POST"])
def add_question():
    page_index = request.form.get('pageIndex')
    question_index = request.form.get('questionIndex')
    question = request.form.get('question')
    answer_type = request.form.get('answerType')
    weight_type = request.form.get('weightType')

    app.logger.info(page_index)    

    success = add_question_to_json(CONFIG_NAME,page_index,question_index,question,answer_type,weight_type)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response

@app.route('/addAnswer', methods=["POST"])
def add_answer():
    page_index = request.form.get('pageIndex')
    question_index = request.form.get('questionIndex')
    answer_index = request.form.get('answerIndex')
    text = request.form.get('text')
    weight = request.form.get('weight')

    success = add_answer_to_json(CONFIG_NAME, page_index,question_index,answer_index,text,weight)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response


@app.route('/result', methods=["POST"])
def result():
    if('pages' not in session):
        return "Session expired, please fill out the form again. Sorry for the inconvenience."
    
    pages = session['pages']
    res = []
    counter = 1
    for item in pages:
        for question in item.questions:
            counter += 1
            res.append(request.form['answer-' + question.id])

    response = app.response_class(response="OK" if res else "ERR",status=200 if res else 400)
    return render_template("questionnaire.html", pages=res)


if __name__ == '__main__':    
    app.run(debug=True, port=5000, host='0.0.0.0')
