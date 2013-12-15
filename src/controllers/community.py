from flask import Blueprint, jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_user, login_required,logout_user
from src.forms import CreateCommunityForm,CreateWallPostForm, WallPostCommentForm
from db.models import Community
from src import db

mod = Blueprint('community_page', __name__, url_prefix='/community')


@mod.route('/', methods=['GET'])
@login_required
def index():
   c_id = request.args.get('c_id') or abort(404)
   return redirect(url_for('community_page.wall', c_id=c_id))

@mod.route('/wall', methods=['GET'])
@login_required
def wall():
   c_id = request.args.get('c_id') or abort(404)
   c = Community().query.filter_by(id=c_id).first()
   c.num_members = c.members.count()
   postForm = CreateWallPostForm()
   commentForm = WallPostCommentForm()
   return render_template('community/community.html', community=c, postForm=postForm, commentForm=commentForm)


@mod.route('/list', methods=['GET'])
@login_required
def list():
   form = CreateCommunityForm()
   type = request.args.get('get') or 'public'
   return render_template('community/communiy_list.html', communities={}, form=form, type=type)

