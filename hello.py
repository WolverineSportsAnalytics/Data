from flask import Flask, render_template, url_for
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class DataAccess(Form):
    password = StringField('password')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()