from src.forms import LoginForm, SignupForm
from flask import session, g, redirect, url_for, render_template, request
from flask.ext.login import login_user, login_required,logout_user
import bcrypt
from db.models import User
from src import db

#https://flask-login.readthedocs.org/en/latest/

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
      return redirect(url_for('login'))
   return render_template('account/signup.html', form=form)
   
def login():
   #if user is already logged in, take him somewhere else
   if g.user is not None and g.user.is_authenticated():
      return redirect(url_for('communities'))
         
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(user_name = form.user_name.data).first()
      if user is not None and user.password == bcrypt.hashpw(form.password.data, user.password):
         login_user(user, remember = form.remember_me.data)   
         return redirect(request.args.get('next') or url_for('communities'))
   
   return render_template('account/login.html', form=form)
   
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

@login_required
def profile():
   return render_template('account/profile.html')
