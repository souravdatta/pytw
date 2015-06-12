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
    print('verifier={}'.format(verifier))
    auth = tweepy.OAuthHandler(CONFIG['tw']['consumer_key'],
                               CONFIG['tw']['consumer_secret'])
    token = session['request_token']
    print('token = {}'.format(token))
    del session['request_token']
    auth.request_token = token
    try:
        auth.get_access_token(verifier)
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
        api = tweepy.API(auth)
        api.update_status('Hello tweepy!')
    except tweepy.TweepError as ex:
        print('Error in access token ', ex)
        return redirect('/')
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
        print('Failed to get request token ', ex)
        return redirect('/')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTWoaWOA'

if __name__ == '__main__':
    app.run()

