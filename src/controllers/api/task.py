from flask import Blueprint,jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateTaskForm
from db.models import Community, Task, User
from src import db

api = Blueprint('task', __name__, url_prefix='/api')

def construct_task(c_id):
	def serialize(t):
		return t.serialize
	return serialize

@api.route('/community/<int:c_id>/tasks', methods=['GET'])
@login_required
def get_posts(c_id):
   tasks = Task().query.filter_by(community_id= c_id).all()
   return jsonify(success = True, data= map(construct_task(c_id), tasks))


@api.route('/community/<int:c_id>/tasks', methods=['POST'])
@login_required
def new_post(c_id):
   form = CreateTaskForm()

   if form.validate_on_submit():
      t = Task(name           = form.name.data, 
               summary        = form.summary.data,
               created_by     = g.user.id,
               community_id   = c_id,
               modified_by    = g.user.id,
               Description    = ""
               )
      
      db.session.add(t)
      db.session.commit()
      
      #return new model
      new_task = construct_task(c_id)(t)
      return jsonify(success = True, data=new_task)
   return jsonify(success = False, errors = form.errors)

   
   
   