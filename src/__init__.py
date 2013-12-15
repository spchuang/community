from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, current_user
from flask_wtf.csrf import CsrfProtect



#----------------------------------------
# initialization
#----------------------------------------
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#flask-wtf
CsrfProtect(app)

from src import main
