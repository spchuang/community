from models.users import User, Users
from models.community import Community
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template
from flask.ext.login import login_user, login_required,logout_user
from forms import CreateCommunityForm

@login_required
def community():
   form = CreateCommunityForm()
   c = Community()
   communities = c.get_user_communities(g.user.get_id())
#   communities = [
#      {'id': 0, 'name':'community 1', 'description': 'test1'},
#      {'id': 1, 'name':'community 2', 'description': 'test2'},
#      {'id': 2, 'name':'community 3', 'description': 'test3'},

#   ]
   return render_template('communiy_list.html', communities=communities, form=form)
 
@login_required  
def create_community():
   print "OK"