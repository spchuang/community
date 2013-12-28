from flask import Blueprint, jsonify, g, url_for, render_template, abort,request
from flask.ext.login import login_required
from src.forms import CreateCommunityForm
from db.models import Community, User, get_community_list
from src import db

api = Blueprint('communities', __name__, url_prefix='/api')

@api.route('/communities/list', methods=['GET'])
@login_required
def list():

   type = request.args.get('get') or 'public'
   if type == 'public':
      com_list = get_community_list(g.user).filter(Community.is_private ==0).all()
   elif type == g.user.user_name:
      com_list = get_community_list(g.user, is_user_filter=True).filter(Community.is_private ==0).all()

   else:
      #if looking at other users, must need to be related somehow first.. (belong to the same group?)
      user = User().query.filter_by(user_name=type).first()
      if user is not None:
         com = get_community_list(user, is_user_filter=True).filter(Community.is_private ==0).all()
      else:
         return jsonify(success=False, error="user not found")


   def merge_com(c):
      #TODO: show status of user to community (joined? join?)
      com = c.Community.serialize
      com['action'] = {
         'join' :url_for('communities.join', c_id=c.Community.id)
      }
      com['url']         = url_for('community_page.index', c_id=c.Community.id)
      com['is_member']   = c.is_member or 0
      com['members']     = {
         'total' : c.num_members,
         'list'      : []
      }
      return com

   return jsonify(success = True, data= map(merge_com, com_list))


@api.route('/communities/create',methods=['POST'])
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

@api.route('/communities/join', methods=['POST'])
@login_required
def join():
   c_id = request.args.get('c_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")
   join_community = Community().query.filter_by(id=c_id).first()

   try:
      g.user.join(join_community)
   except Exception as e:
      return jsonify(success = False, errors = str(e))

   db.session.add(g.user)
   db.session.commit()
   return jsonify(success = True)
   
   
@api.route('/community/<int:c_id>/members', methods=['GET'])
@login_required
def get_members(c_id):
   print c_id
   members = Community().query.get(c_id).members.all()
   print members
   return jsonify(success = True, data=[m.serialize for m in members] )