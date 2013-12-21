from flask import Blueprint,jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateWallPostForm, WallPostCommentForm
from db.models import Community, User,Post, get_wall_posts
from src import db

api = Blueprint('wall', __name__, url_prefix='/api')

#currying to use community_id
def construct_post(c_id):
   def serialize(p):
      post = p.serialize
      post['action'] = {
         'comment' :url_for('wall.new_post_comment', c_id=c_id, p_id=p.id)
      }
      post['comments'] = [comment.serialize for comment in p.comments]
      return post
   return serialize
   


@api.route('/community/<int:c_id>/wall/posts')
@login_required
def get_posts(c_id):
   posts = get_wall_posts(c_id).all()
   return jsonify(success = True, data= map(construct_post(c_id), posts))


@api.route('/community/<int:c_id>/wall/posts', methods=['POST'])
@login_required
def new_post(c_id):
   postForm = CreateWallPostForm()
   if postForm.validate_on_submit():
      p = Post(body = postForm.body.data, user_id=g.user.id)
      c = Community().query.filter_by(id=c_id).first()
      c.create_post(p)
      db.session.add(c)
      db.session.commit()
      
      #return new model
      new_post = construct_post(c_id)(p)
      return jsonify(success = True, data=new_post)
   return jsonify(success = False, errors = postForm.errors)
   
   
@api.route('/community/<int:c_id>/wall/posts/<int:p_id>/comments', methods=['GET'])
@login_required
def get_post_comments(c_id, p_id):
   comments = Post().query.filter_by(id=p_id).first().comments
   return jsonify(success = False, data = [comment.serialize for comment in comments])


@api.route('/community/<int:c_id>/wall/posts/<int:p_id>/comments', methods=['POST'])
@login_required
def new_post_comment(c_id, p_id):
   commentForm = WallPostCommentForm()
   if commentForm.validate_on_submit():
      new_comment = Post(body = commentForm.body.data, user_id=g.user.id)
      p = Post().query.filter_by(id=p_id).first()
      p.comment(new_comment)
      db.session.add(p)
      db.session.commit()
      return jsonify(success = True, data=new_comment.serialize)
   return jsonify(success = False, errors = commentForm.errors)