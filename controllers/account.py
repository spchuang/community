from flask.views import View
from models.users import User, Users
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template
from flask.ext.login import login_user

   
#https://flask-login.readthedocs.org/en/latest/
#TODO: finish singup with bycrpt, signin with session control (save to db)?
def signup():
   print "TEST"
#return redirect(url_for('/home'))
   return render_template('signup.html')
   
def login():
   
   if request.method == 'POST':
      if request.form['username'] != "test":
         error = 'Invalid username'
      elif request.form['password'] != "test":
         error = 'Invalid password'
      else:
         user = User(nickname = 'test')
         login_user(user)
      return redirect(url_for('community'))
   	
   return render_template('login.html')
   
def logout():
   session.pop('logged_in', None)
   return redirect(url_for('login'))


def profile():
   return render_template('profile.html')