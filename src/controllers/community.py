from flask import jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_user, login_required,logout_user
from src.forms import CreateCommunityForm,CreateWallPostForm, WallPostCommentForm
from db.models import Community, User, Wall,Post, get_community_list, get_wall_posts
from src import db

@login_required
def community():
   c_id = request.args.get('id') or abort(404)
   w_id = request.args.get('wall') or 'default'
   c = Community().query.filter_by(id=c_id).first()
   c.num_members = c.members.count()
   w = c.walls.all()
   p = get_wall_posts(c,w[0]).all()

   postForm = CreateWallPostForm()
   return render_template('community.html', community=c, walls=w, posts=p, postForm=postForm)

@login_required
def communities():
   form = CreateCommunityForm()
   type = request.args.get('get') or 'public'
   return render_template('communiy_list.html', communities={}, form=form, type=type)

@login_required
def create_post():
   c_id = request.args.get('id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")
   w_id = request.args.get('wall')
   if w_id is None:
      return jsonify(success = False, errors = "What wall?")
   postForm = CreateWallPostForm()
   if postForm.validate_on_submit():
      w = Wall().query.filter(Wall.id==w_id).first()
      new_post = Post(body = postForm.body.data, user_id=g.user.id)
      w.create(new_post)
      db.session.add(w)
      db.session.commit()
      return jsonify(success = True)

   return jsonify(success = False, errors = postForm.errors)

@login_required
def comment_post():
   
   form = WallPostCommentForm()

#todo
@login_required
def get_wall_posts():
   pass

#todo
@login_required
def get_post_comments():
   pass

@login_required
def community_list():
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

@login_required  
def create_community():
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

@login_required
def join_community():
   id =  request.form["id"]

   join_community = Community().query.filter_by(id=id).first()
   try:
      g.user.join(join_community)
   except Exception as e:
      return jsonify(success = False, errors = str(e))

   db.session.add(g.user)
   db.session.commit()
   return jsonify(success = True)