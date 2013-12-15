# all the imports
import config
from controllers import user, community

from flask import request, session, g, redirect, url_for, \
   abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from src import app, login_manager, db
from db.models import User

from controllers.api.communities import api as communities_api
from controllers.api.wall import api as wall_api

@app.before_request
def before_request():
    print current_user
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
 
#bind URL
app.add_url_rule('/login',    methods=['GET', 'POST'],   view_func=user.login)
app.add_url_rule('/logout',   methods=['GET'],           view_func=user.logout)
app.add_url_rule('/signup',   methods=['GET', 'POST'],   view_func=user.signup)
app.add_url_rule('/profile',  methods=['GET'],           view_func=user.profile)
app.add_url_rule('/list/community'     ,methods=['GET'],      view_func=community.communities)

app.add_url_rule('/community' ,methods=['GET'],      view_func=community.community)

app.register_blueprint(communities_api)
app.register_blueprint(wall_api)

#app.add_url_rule('/api/communities/create', methods=['POST'],    view_func=communities.create)
#app.add_url_rule('/api/communities/join' ,  methods=['POST'],    view_func=communities.join)
#app.add_url_rule('/api/communities',   methods=['GET'],     view_func=communities.list)
#app.add_url_rule('/api/community/create_post',  methods=['POST'],     view_func=community.create_post)
#app.add_url_rule('/api/community/comment_post',  methods=['POST'],     view_func=community.comment_post)
