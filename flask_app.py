__author__ = 'Sourav Datta'

from flask import *
import tweepy
from config import CONFIG


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth = tweepy.OAuthHandler(CONFIG['tw']['consumer_key'],
                               CONFIG['tw']['consumer_secret'])

    if auth is None:
        return redirect('/')

    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepError as ex:
        print('Failed to get request token ', ex)
        return redirect('/')

if __name__ == '__main__':
    app.run()

