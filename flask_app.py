__author__ = 'Sourav Datta'

from flask import *
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from config import CONFIG


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html', user='Sourav')

if __name__ == '__main__':
    app.run()

