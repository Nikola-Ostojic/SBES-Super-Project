from flask import Flask, render_template, url_for
import json

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/home')
def home():
    app.logger.info("Home")

    pages = json.load(open('config.json', 'r'))

    

    return render_template("questionnaire.html", pages=pages)


@app.route('/admin')
def admin():
    app.logger.info("Admin")

    return render_template("admin.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')