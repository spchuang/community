from flask.views import View
from models.users import User, Users
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template
from flask.ext.login import login_user, login_required,logout_user

   
#https://flask-login.readthedocs.org/en/latest/
#TODO: finish singup with bycrpt, signin with session control (save to db)?
def signup():
   print "TEST"
   return render_template('signup.html')
   
def login():
   if request.method == 'POST':
      users = Users()
      id = users.get_user_id(request.form['username'], request.form['password'])
         
      #if user exists in db
      if id is not False:
         login_user(Users().get_user(id))      
         return redirect(url_for('community'))
   	
   return render_template('login.html')
   
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

@login_required
def profile():
   return render_template('profile.html')