from flask import Flask, render_template, url_for,request
from processing import process,add_page_to_json
from models import Page

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CONFIG_NAME = "config.json"
formula, pages = process(CONFIG_NAME)

@app.route('/home')
def home():        
    formula, pages = process(CONFIG_NAME)
    html = render_template("questionnaire.html", pages=pages)
    return html


@app.route('/admin')
def admin():    
    app.logger.info(pages)
    return render_template("admin.html", pages=pages)

@app.route('/addPage', methods=["POST"])
def add_page():
    index = request.form.get('index')
    title = request.form.get('title')
    formula = request.form.get('formula')

    success = add_page_to_json(CONFIG_NAME,index,title,formula)

    if success:
        formula,pages = process(CONFIG_NAME)

    response = app.response_class(response="OK" if success else "ERR",status=200 if success else 400)
    return response

@app.route('/result', methods=["POST"])
def result():
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