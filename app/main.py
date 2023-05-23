from flask import Flask, render_template, url_for,request, session, redirect
from flask_session import Session
from calculate import calculate_result
from processing import process, edit_page_json,edit_question_json, edit_answer_json, add_answer_to_json
from models import Page
from database import get_db_engine, init_tables, validate_user_credentials
import os
from db_models import User

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 1800
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv('SECRET_KEY')
Session(app)
CONFIG_NAME = "config.json"

engine = get_db_engine()
init_tables(engine)


@app.route('/')
@app.route('/home')
def home():
    html = render_template("landingPage.html")
    return html

@app.route('/smallBusiness')
def smallBusiness():
    pages = None
    if not session.get("pages"):
        pages = process(CONFIG_NAME, "small")
        session['pages'] = pages
    else:
        pages = session.get('pages')

    app.logger.info(pages)
    app.logger.info(type(pages))

    html = render_template("questionnaire.html", pages=pages)
    return html

@app.route('/criticalBusiness')
def mediumBusiness():
    pages = None
    if not session.get("criticalPages"):
        pages = process(CONFIG_NAME, "critical")
        session['criticalPages'] = pages
    else:
        pages = session.get('criticalPages')

    app.logger.info(pages)
    app.logger.info(type(pages))

    html = render_template("questionnaire.html", pages=pages)
    return html



@app.route('/admin')
def admin():
    if session.get('authenticated') != True:
        return redirect(url_for('login'))
    pages = process(CONFIG_NAME, "small")
    return render_template("admin.html", pages=pages)


@app.route('/editPage', methods=["POST"])
def edit_page():
    page_id = request.form.get('pageId')
    index = request.form.get('index')
    title = request.form.get('title')

    success = edit_page_json(CONFIG_NAME, 'small', page_id, index, title)

    response = app.response_class(response="OK" if success else "ERR", status=200 if success else 400)
    return response


@app.route('/editQuestion', methods=["POST"])
def edit_question():
    page_id = request.form.get('pageId')
    question_id = request.form.get('questionId')
    question_index = request.form.get('index')
    question = request.form.get('question')
    answer_type = request.form.get('answerType')

    success = edit_question_json(CONFIG_NAME, 'small', page_id, question_id, question_index, question,answer_type)
    response = app.response_class(response="OK" if success else "ERR", status=200 if success else 400)
    return response


@app.route('/editAnswer', methods=['POST'])
def edit_answer():
    page_id = request.form.get('pageId')
    question_id = request.form.get('questionId')
    answer_id = request.form.get('answerId')
    answer_index = request.form.get('index')
    text = request.form.get('answer')
    weight = request.form.get('weight')

    success = edit_answer_json(CONFIG_NAME, 'small', page_id,question_id, answer_id,answer_index,text,weight)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response


@app.route('/addAnswer', methods=["POST"])
def add_answer():
    page_id = request.form.get('pageId')
    question_id = request.form.get('questionId')
    answer_index = request.form.get('index')
    text = request.form.get('answer')
    weight = request.form.get('weight')

    success = add_answer_to_json(CONFIG_NAME, 'small', page_id, question_id, answer_index, text, weight)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response


@app.route('/result', methods=["POST", "GET"])
def result():

    if request.method == 'GET':
        if session.get('result'):
            return render_template('result.html', result=session['result'], company=session['company'])
        else:
            return redirect('home.html')

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

    result = calculate_result(engine, res)
    company = res['answer-1-1-1']

    session['result'] = result
    session['company'] = company
    response = app.response_class(response="OK" if result else "ERR", status=200 if res else 400)
    return response


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if session.get('authenticated') == True:
            return redirect(url_for('admin'))
        html = render_template("login.html")
        return html

    else:
        username = request.form.get('username')
        password =  request.form.get('password')

        is_valid = validate_user_credentials(engine, username, password)

        if is_valid:
            session['authenticated'] = True

        response = app.response_class(response="OK" if is_valid else "ERR", status=200 if is_valid else 400)

        return response

@app.route('/logout', methods=['POST'])
def logout():
    if session.get('authenticated'):
        del session['authenticated']

    response = app.response_class(response="OK", status=200)
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
