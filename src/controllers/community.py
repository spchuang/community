from flask import jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_user, login_required,logout_user
from src.forms import CreateCommunityForm,CreateWallPostForm, WallPostCommentForm
from db.models import Community, User,Post, get_community_list, get_wall_posts
from src import db

@login_required
def community():
   c_id = request.args.get('c_id') or abort(404)
   c = Community().query.filter_by(id=c_id).first()
   c.num_members = c.members.count()
   p = get_wall_posts(c).all()

   print p
   postForm = CreateWallPostForm()
   commentForm = WallPostCommentForm()
   return render_template('community.html', community=c, posts=p, postForm=postForm, commentForm=commentForm)

@login_required
def communities():
   form = CreateCommunityForm()
   type = request.args.get('get') or 'public'
   return render_template('communiy_list.html', communities={}, form=form, type=type)

@login_required
def create_post():
   c_id = request.args.get('c_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")

   postForm = CreateWallPostForm()
   if postForm.validate_on_submit():
      new_post = Post(body = postForm.body.data, user_id=g.user.id)
      c = Community().query.filter_by(id=c_id).first()
      c.create_post(new_post)
      db.session.add(c)
      db.session.commit()
      return jsonify(success = True)

   return jsonify(success = False, errors = postForm.errors)

@login_required
def comment_post():
   c_id = request.args.get('c_id')
   p_id = request.args.get('p_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")
   if p_id is None:
      return jsonify(success = False, errors = "What post?")

   commentForm = WallPostCommentForm()
   if commentForm.validate_on_submit():
      print "validated"
      new_post = Post(body = commentForm.body.data, user_id=g.user.id)
      p = Post().query.filter_by(id=p_id).first()
      p.comment(new_post)
      db.session.add(p)
      db.session.commit()
      return jsonify(success = True)
   print "not alidated"
   return jsonify(success = False, errors = commentForm.errors)


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