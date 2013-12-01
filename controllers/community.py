from models.users import User, Users
from models.communities import Communities
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template
from flask.ext.login import login_user, login_required,logout_user

@login_required
def community():
   c = Communities()
   
   return render_template('communiy_list.html')