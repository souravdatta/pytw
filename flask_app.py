__author__ = 'Sourav Datta'

from flask import *
import tweepy
from config import CONFIG


app = Flask(__name__)
app.debug = False

api = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    args = request.args
    if ('denied' in args) or ('request_token' not in session):
        flash('Could not login, access denied!')
        return redirect('/')
    verifier = args.get('oauth_verifier', '')
    auth = tweepy.OAuthHandler(CONFIG['tw']['consumer_key'],
                               CONFIG['tw']['consumer_secret'])
    token = session['request_token']
    session.pop('request_token', None)
    auth.request_token = token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError as ex:
        print('Failed to get access token: ', ex)
        return redirect('/')
    try:
        global api
        api = tweepy.API(auth)
    except tweepy.TweepError as ex:
        print('Failed to create twitter api: ', ex)
        return redirect('/')
    try:
        api.update_status(status='Hello, tweepy!')
    except tweepy.TweepError as ex:
        print('Failed to update status: ', ex)
    return render_template('home.html')


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
        print('Failed to get request token: ', ex)
        return redirect('/')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTWoaWOA'

if __name__ == '__main__':
    app.run()

