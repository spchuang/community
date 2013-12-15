from flask import Blueprint, jsonify, g, url_for, render_template, abort,request
from flask.ext.login import login_required
from src.forms import CreateCommunityForm
from db.models import Community, User, get_community_list
from src import db

api = Blueprint('communities', __name__, url_prefix='/api/communities')

@api.route('/list', methods=['GET'])
@login_required
def list():
   #TODO: show status of user to community (joined? join?)
   type = request.args.get('get') or 'public'
   if type == 'public':
      com = get_community_list(g.user).filter(Community.is_private ==0).all()
   elif type == g.user.user_name:
      com = get_community_list(g.user, is_user_filter=True).filter(Community.is_private ==0).all()

   else:
      #if looking at other users, must need to be related somehow first.. (belong to the same group?)
      user = User().query.filter_by(user_name=type).first()
      if user is not None:
         com = get_community_list(user, is_user_filter=True).filter(Community.is_private ==0).all()
      else:
         return jsonify(success=False, error="user not found")

   return jsonify(success = True, data= [
               {'id':c.Community.id, 'name': c.Community.name, 'num_members': c.num_members, 'is_member': c.is_member}
               for c in com
          ])

@api.route('/create',methods=['POST'])
@login_required
def create():
   form = CreateCommunityForm()
   if form.validate_on_submit():
      new_community = Community(name   = form.name.data,
                                description  = form.description.data)
      db.session.add(new_community)
      db.session.commit()
      g.user.join(new_community)
      db.session.add(g.user)
      db.session.commit()
      return jsonify(success = True)
   return jsonify(success = False, errors = form.errors)

@api.route('/join', methods=['POST'])
@login_required
def join():
   id =  request.form["id"]

   join_community = Community().query.filter_by(id=id).first()
   try:
      g.user.join(join_community)
   except Exception as e:
      return jsonify(success = False, errors = str(e))

   db.session.add(g.user)
   db.session.commit()
   return jsonify(success = True)