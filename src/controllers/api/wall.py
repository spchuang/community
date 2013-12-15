from flask import Blueprint,jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateWallPostForm, WallPostCommentForm
from db.models import Community, User,Post, get_wall_posts
from src import db

api = Blueprint('wall', __name__, url_prefix='/api/wall')

def merge_comments(p):
   post = p.serialize
   post['user'] = {
      "first_name" : p.user.first_name.capitalize(),
      "last_name"  : p.user.last_name.capitalize(),
      "user_id"    : p.user.id,
   }
   return post


@api.route('/posts')
@login_required
def posts():
   c_id = request.args.get('c_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")

   posts = get_wall_posts(c_id).all()

   def merge_posts(p):
      post = p.serialize
      post['user'] = {
         "first_name" : p.user.first_name.capitalize(),
         "last_name"  : p.user.last_name.capitalize(),
         "user_id"    : p.user.id,
      }
      post['action'] = {
         'comment' :url_for('wall.comment_post', c_id=c_id, p_id=p.id)
      }
      post['comments'] = map(merge_comments, p.comments)

      return post

   #return map(merge_result, posts)

   return jsonify(success = True, data= map(merge_posts, posts))



@api.route('/new_post', methods=['POST'])
@login_required
def new_post():
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


@api.route('/comment_post', methods=['POST'])
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
      new_post = Post(body = commentForm.body.data, user_id=g.user.id)
      p = Post().query.filter_by(id=p_id).first()
      p.comment(new_post)
      db.session.add(p)
      db.session.commit()
      return jsonify(success = True)
   return jsonify(success = False, errors = commentForm.errors)