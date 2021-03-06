__author__ = 'Sourav Datta'

from flask import *
import tweepy
from config import CONFIG
import json


app = Flask(__name__)
app.debug = False

api = None

@app.route('/')
def index():
    return render_template('index.html',
                           logo_message='PyTw - A simple Twitter client in Python',
                           logo_link='https://github.com/souravdatta/pytw')

@app.route('/post')
def post_tweet():
    tweet = request.args.get('tweet')
    if tweet is None or tweet == '':
        return
    if 'logged_in' not in session:
        return 'failed'
    global api
    if api is not None:
        api.update_status(status=tweet)
        return 'success'
    return 'failed'

@app.route('/timeline')
def timeline():
    if 'logged_in' not in session:
        return json.dumps([])
    tweets = []
    global api
    for status in tweepy.Cursor(api.user_timeline).items(10):
        tweets.append(status.text)
    return json.dumps(tweets)

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
        session['logged_in'] = True
    except tweepy.TweepError as ex:
        print('Failed to get access token: ', ex)
        return redirect('/')
    try:
        global api
        api = tweepy.API(auth)
    except tweepy.TweepError as ex:
        print('Failed to create twitter api: ', ex)
        return redirect('/')
    return redirect('/twitter')

@app.route('/twitter')
def twitter():
    if 'logged_in' not in session:
        return redirect('/')
    user = api.me()
    tweets = []
    for status in tweepy.Cursor(api.user_timeline).items(10):
        tweets.append(status.text)
    return render_template('home.html',
                           logo_link='https://twitter.com/{}'.format(user.screen_name),
                           logo_message='Hi {}'.format(user.screen_name),
                           tweets=tweets
                           )

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

app.secret_key = 'AzerBaizanA0Zr98j/3yX R~XHH!jmN]LWX/,?RTWoaWOA'

if __name__ == '__main__':
    app.run()

