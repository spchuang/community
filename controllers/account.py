from models.users import User, Users
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template
from flask.ext.login import login_user, login_required,logout_user
   
#https://flask-login.readthedocs.org/en/latest/

def signup():
   if request.method == 'POST':
      #Todo: form validation

      new_user = {
         'user_name':   request.form['user_name'],
         'first_name':  request.form['first_name'],
         'last_name':   request.form['last_name'],
         'gender':      request.form['gender'],
         'email':       request.form['email'],
         'password':    reeqest.form['password']
      }
      users = Users()
      
      #upon successful signup, redirect to community
      if users.add_user(new_user):
         return redirect(url_for('community'))
      #Todo: Error handling
      

   return render_template('signup.html')
   
def login():
   if request.method == 'POST':
      users = Users()

      id = users.get_user_id(request.form['username'], request.form['password'])
         
      #if user exists in db
      if id is not False:
         login_user(Users().get_user(id))   
         print request.args.get('next')   
         return redirect(request.args.get('next') or url_for('community'))
   
   return render_template('login.html')
   
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

@login_required
def profile():
   return render_template('profile.html')