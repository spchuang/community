from src.forms import LoginForm, SignupForm
from flask import Blueprint, session, g, redirect, url_for, render_template, request
from flask.ext.login import login_user, login_required,logout_user
import bcrypt
from db.models import User
from src import db, facebook


#https://flask-login.readthedocs.org/en/latest/
mod = Blueprint('account', __name__, url_prefix='/account')

@mod.route('/signup', methods=['GET', 'POST'])
def signup():
   form = SignupForm()
   
   if form.validate_on_submit():
      hashed_password = bcrypt.hashpw(form.password.data,bcrypt.gensalt())

      new_user = User(user_name   = form.user_name.data,
                  first_name  = form.first_name.data,
                  last_name   = form.last_name.data,
                  gender      = form.gender.data,
                  email       = form.email.data,
                  password    = hashed_password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('account.login'))
   return render_template('account/signup.html', form=form)

@mod.route('/fb_signup', methods=['GET','POST'])
def fb_signup():
   '''
   return redirect(url_for('account.fb_login'), code=307)
   print session
   me = facebook.get('/me')
   form = SignupForm()
   print me
   '''
   return render_template('account/signup.html', form=form)



#this function is strictly for displaying the login page where the user can decide whether to use the default login fr the facebook login
@mod.route('/login', methods=['GET'])
def login():
   
   #if user is already logged in, take him somewhere else
   if g.user.is_authenticated():
      return redirect(request.args.get('next') or url_for('community_page.list'))
   
   form = LoginForm()
   return render_template('account/login.html', form=form)
  

@mod.route('/logout', methods=['GET'])
@login_required
def logout():
   pop_login_session()
   logout_user()
   return redirect(request.referrer or url_for('account.login'))

@mod.route('/profile', methods=['GET'])
@login_required
def profile():
   return render_template('account/profile.html')

#login callback methods
@mod.route('/facebook_login', methods=['POST'])
def fb_login():
   #check if user is logged in with fb
   return facebook.authorize(callback=url_for('account.facebook_authorized',
      next=request.args.get('next') or None, _external=True))

@mod.route('/default_login', methods=['POST'])
def default_login():
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(user_name = form.user_name.data).first()
      if user is not None and user.password == bcrypt.hashpw(form.password.data, user.password):
         login_user(user, remember = form.remember_me.data)   
         return redirect(request.args.get('next') or url_for('community_page.list'))
         
   return redirect(url_for('account.login'))


#facebook authorization
@mod.route('/login/facebook_authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
   next_url = request.args.get('next') or url_for('community_page.list')

   #TODO: not facebook logged in, return to somewhere
   if resp is None:
      return "You're not logged in with fb"
   
   #fb is logged in, see if this fb user is in the db
   session['facebook_token'] = (resp['access_token'], '')
   me = facebook.get('/me')

   #query the user based on fb id
   this_user = User.query.filter_by(fb_id = me.data['id']).first()

   if this_user is None:
      return redirect(url_for('account.signup'))
   else:
      login_user(this_user)
   
   return redirect(next_url)
      
@facebook.tokengetter
def get_facebook_token():
   return session.get('facebook_token')

def pop_login_session():
   session.pop('login', None)
   session.pop('facebook_token', None)