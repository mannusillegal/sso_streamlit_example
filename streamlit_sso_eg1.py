
from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)

# SSO Configuration
sso = oauth.remote_app(
    'sso',
    consumer_key='your_client_id',
    consumer_secret='your_client_secret',
    request_token_params={'scope': 'email'},
    base_url='https://sso.example.com/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://sso.example.com/oauth/token',
    authorize_url='https://sso.example.com/oauth/authorize'
)


@app.route('/')
def index():
    if 'sso_token' in session:
        sso_token = session['sso_token']
        # Use sso_token to access SSO API
        # and retrieve user information
        # Store the information in database
        return 'Hello User'
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return sso.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('sso_token', None)
    return redirect(url_for('index'))


@app.route('/authorized')
def authorized():
    resp = sso.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['sso_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))


# Streamlit App


@st.cache
def get_user_info():
    sso_token = session.get('sso_token')
    if sso_token is None:
        return None
    access_token, _ = sso_token
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    resp = sso.get('user', headers=headers)
    if resp.status != 200:
        return None
    return resp

# Flask App


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)


sso = oauth.remote_app('sso', consumer_key='your_client_id', consumer_secret='your_client_secret',    request_token_params={
                       'scope': 'email'},    base_url='https://sso.example.com/api/',    request_token_url=None,    access_token_method='POST',    access_token_url='https://sso.example.com/oauth/token',    authorize_url='https://sso.example.com/oauth/authorize')


@app.route('/')
def index():
    if 'sso_token' in session:
        sso_token = session['sso_token']
        return 'Hello User'
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return sso.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('sso_token', None)
    return redirect(url_for('index'))


@app.route('/authorized')
def authorized():
    resp = sso.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (request.args['error_reason'], request.args['error_description'])
        session['sso_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))
# Streamlit App
