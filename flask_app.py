__author__ = 'Sourav Datta'

from flask import *
import authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from config import CONFIG


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html', user='Hola')

@app.route('/login/<provider_name>', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = Authomatic(CONFIG, 'secret').login(WerkzeugAdapter(request, response), provider_name)
    if result:
        if result.user:
            result.user.update()
            return render_template('home.html', user=result.user)
    return redirect('/')

if __name__ == '__main__':
    app.run()

