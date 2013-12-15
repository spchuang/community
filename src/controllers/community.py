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

   postForm = CreateWallPostForm()
   commentForm = WallPostCommentForm()
   return render_template('community/community.html', community=c, posts=p, postForm=postForm, commentForm=commentForm)

@login_required
def communities():
   form = CreateCommunityForm()
   type = request.args.get('get') or 'public'
   return render_template('community/communiy_list.html', communities={}, form=form, type=type)



