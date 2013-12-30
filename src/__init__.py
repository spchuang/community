from flask import Flask
import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, current_user
from flask_wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth




#----------------------------------------
# initialization
#----------------------------------------
app = Flask(__name__)
app.config.from_object('config')

#flask-sqlalchemy
db = SQLAlchemy(app)

#flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account.login'

#flask-oauth
oauth = OAuth(app)
facebook = oauth.remote_app(
    'facebook',
    consumer_key= config.FACEBOOK_APP_ID,
    consumer_secret= config.FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

#flask-wtf
CsrfProtect(app)

from src import main
