from app.forms import LoginForm, SignupForm
from app.models.user import User, Users
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template
from flask.ext.login import login_user, login_required,logout_user


   
#https://flask-login.readthedocs.org/en/latest/

def signup():
   form = SignupForm()
   if form.validate_on_submit():
      #Todo: form validation
      print form.password.data
      print form.gender.data
      new_user = {
         'user_name':   form.user_name.data,
         'first_name':  form.first_name.data,
         'last_name':   form.last_name.data,
         'gender':      form.gender.data,
         'email':       form.email.data,
         'password':    form.password.data
      }
      users = Users()
      
      #upon successful signup, redirect to community
      if users.add_user(new_user):
         return redirect(url_for('login'))
      
   print form.errors
   return render_template('signup.html', form=form)
   
def login():
   #if user is already logged in, take him somewhere else
   if g.user.is_authenticated():
      return redirect(url_for('community'))
   form = LoginForm()
   print dir(form.user_name)
   if form.validate_on_submit():
      users = Users()
      id = users.get_user_id(request.form['user_name'], request.form['password'])
      if id is not False:
         login_user(Users().get_user(id))   
         return redirect(request.args.get('next') or url_for('community'))
   
   return render_template('login.html', form=form)
   
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

@login_required
def profile():
   return render_template('profile.html')
