from flask import Blueprint, jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_user, login_required,logout_user
from src.forms import CreateCommunityForm,CreateWallPostForm, WallPostCommentForm, CreateEventForm
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

@mod.route('/calendar', methods=['GET'])
@login_required
def calendar():
   c_id = request.args.get('c_id')
   form = CreateEventForm()
   if c_id == 'all':
      c = {'id': 'all'}
   else:
      c = Community().query.filter_by(id=c_id).first()
   return render_template('community/community_calendar.html', community=c, form=form)
   
@mod.route('/task', methods=['GET'])
@login_required
def task():
   c_id = request.args.get('c_id') or abort(404)
   form = CreateEventForm()

   c = Community().query.filter_by(id=c_id).first()
   return render_template('community/community_task.html', community=c)

@mod.route('/list', methods=['GET'])
@login_required
def list():
   form = CreateCommunityForm()
   type = request.args.get('get') or 'public'
   return render_template('community/communiy_list.html', communities={}, form=form, type=type)
