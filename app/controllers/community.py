from flask import jsonify,session, g, redirect, url_for, render_template, request
from flask.ext.login import login_user, login_required,logout_user
from app.forms import CreateCommunityForm
from app.models import Community, User
from app import db

@login_required
def community():
   form = CreateCommunityForm()
   type = request.args['get']

   return render_template('communiy_list.html', communities={}, form=form, type=type)

@login_required
def community_list():
   #get public, current user, or other user
   #TODO: show status of user to community (joined? join?)
   type = request.args['get']
   if type == 'public':
      com = Community().query.filter_by(is_private = 0).all()
   elif type == g.user.user_name:
      com = g.user.joined_communities.all()
   else:
      #if looking at other users, must need to be related somehow first.. (belong to the same group?)
      user = User().query.filter_by(user_name=type).first()
      if user is not None:
         com = user.joined_communities.all()
      else:
         return jsonify(success=False, error="user not found")

   return jsonify(success = True, data= [
               {'id':c.id, 'name': c.name}
               for c in com
          ])

@login_required  
def create_community():
   form = CreateCommunityForm()
   if form.validate_on_submit():
      #when user create a new community, he is automatically a member in it

      new_community = Community(name   = form.name.data,
                                description  = form.description.data)
      db.session.add(new_community)
      db.session.commit()
      g.user.join(new_community)
      db.session.add(g.user)
      db.session.commit()
      return jsonify(success = True)

   return jsonify(success = False, errors = form.errors)