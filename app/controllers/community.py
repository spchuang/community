
from flask import session, g, redirect, url_for, render_template
from flask.ext.login import login_user, login_required,logout_user
from app.forms import CreateCommunityForm
from app.models import Community

@login_required
def community():
   form = CreateCommunityForm()
   c = Community(name='test')
   #c = Community()
   #communities = c.get_user_communities(g.user.get_id())
#   communities = [
#      {'id': 0, 'name':'community 1', 'description': 'test1'},
#      {'id': 1, 'name':'community 2', 'description': 'test2'},
#      {'id': 2, 'name':'community 3', 'description': 'test3'},

#   ]
   return render_template('communiy_list.html', communities={}, form=form)
 
@login_required  
def create_community():
   form = CreateCommunityForm()
   if form.validate_on_submit():
      return jsonify(error="false")
      #create community
   
   return jsonify(error="true")