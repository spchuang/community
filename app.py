# all the imports
from models.users import Users, User
from controllers import account, community
import os
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template, flash
from flask.ext.login import LoginManager, login_required,current_user




#----------------------------------------
# initialization
#----------------------------------------
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_request
def before_request():
    g.user = current_user
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
@login_manager.user_loader
def load_user(id):
   return Users().get_user(int(id))
   
#----------------------------------------
# controllers
#----------------------------------------
@app.route('/')
def show_entries():
   return redirect(url_for('home'))

@app.route('/home')
def home():
   return render_template('home.html')

	

 
#bind URL
app.add_url_rule('/login',    methods=['GET', 'POST'],   view_func=account.login)
app.add_url_rule('/logout',   methods=['GET'],           view_func=account.logout)
app.add_url_rule('/signup',   methods=['GET', 'POST'],   view_func=account.signup)
app.add_url_rule('/profile',  methods=['GET'],           view_func=account.profile)
app.add_url_rule('/community',methods=['GET'],           view_func=community.community)




#----------------------------------------
# launch
#----------------------------------------   


if __name__ == '__main__':
   #u = Users()
   #u.add_user()
   #users = u.get_users()
   #print users
   port = int(os.environ.get("PORT", 5000))
   app.run(host='0.0.0.0', port=port)