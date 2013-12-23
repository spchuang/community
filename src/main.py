# all the imports
import config
from flask import request, session, g, redirect, url_for, \
   abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from src import app, login_manager, db
from db.models import User

from controllers.account import mod as account
from controllers.community import mod as community
from controllers.api.communities import api as communities_api
from controllers.api.wall import api as wall_api
from controllers.api.calendar import api as calendar_api
from controllers.api.task import api as task_api

@app.before_request
def before_request():
    g.user = current_user
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('status/404.html'), 404
	
@app.errorhandler(500)
def internal_error(error):
   db.session.rollback()
   return render_template('status/404.html'), 500

@login_manager.user_loader
def load_user(id):
   return User.query.get(int(id))
   
#----------------------------------------
# controllers
#----------------------------------------
@app.route('/')
def show_entries():
   return redirect(url_for('home'))

@app.route('/home')
def home():
   return render_template('home/home.html')
 
#bind blueprint
app.register_blueprint(account)
app.register_blueprint(community)
app.register_blueprint(communities_api)
app.register_blueprint(wall_api)
app.register_blueprint(calendar_api)
app.register_blueprint(task_api)
