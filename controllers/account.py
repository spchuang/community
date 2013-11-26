from flask.views import View
from models.users import Users
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template


def signup():

   print "TEST"
#return redirect(url_for('/home'))
   return render_template('signup.html')
   
def login():
   error = None
   print "TEST"
   return render_template('login.html', error=error)
   
def logout():
   session.pop('logged_in', None)
   return redirect(url_for('login'))
