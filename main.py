from flask import Flask, render_template, url_for
from processing import process
from models import Page

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CONFIG_NAME = "config.json"
formula, pages = process(CONFIG_NAME)

@app.route('/home')
def home():        
    process(CONFIG_NAME)
    html = render_template("questionnaire.html", pages=pages)
    return html


@app.route('/admin')
def admin():
    app.logger.info("Admin")

    return render_template("admin.html")

if __name__ == '__main__':    
    app.run(debug=True, port=5000, host='0.0.0.0')