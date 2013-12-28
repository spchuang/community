from flask import Blueprint,jsonify,session, g, redirect, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import TaskForm
from db.models import Community, Task, User
from src import db

api = Blueprint('task', __name__, url_prefix='/api')

def construct_task(c_id):
   def serialize(t):
      task = t.serialize
      task['action'] = {
         #'url': url_for('task.update_task', c_id=c_id, t_id=t.id)
      }
      return task
   return serialize

@api.route('/community/<int:c_id>/tasks', methods=['GET'])
@login_required
def get_tasks(c_id):
   tasks = Task().query.filter_by(community_id= c_id).all()
   return jsonify(success = True, data= map(construct_task(c_id), tasks))


@api.route('/community/<int:c_id>/tasks', methods=['POST'])
@login_required
def new_task(c_id):
   form = TaskForm()

   if form.validate_on_submit():
      t = Task(name           = form.name.data, 
               summary        = form.summary.data,
               created_by     = g.user.id,
               community_id   = c_id,
               modified_by    = g.user.id,
               description    = form.description.data or ""
               )
      
      db.session.add(t)
      db.session.commit()
      
      #return new model
      new_task = construct_task(c_id)(t)
      return jsonify(success = True, data=new_task)
   return jsonify(success = False, errors = form.errors)


@api.route('/community/<c_id>/tasks/<t_id>',methods=['PUT'])
@login_required
def update_task(c_id, t_id):
   form = TaskForm()
   if form.validate_on_submit():
      t = Task().query.get(t_id)
      t.name         = form.name.data
      t.summary      = form.summary.data
      t.description  = form.description.data
      t.status       = form.status.data
      db.session.commit()
      updated_task = construct_task(c_id)(t)
      return jsonify(success = True, data= updated_task)
      
   return jsonify(success = False, errors = form.errors)

@api.route('/community/<c_id>/tasks/<t_id>',methods=['DELETE'])
@login_required
def delete_task(c_id, t_id):
   t = Task().query.get(t_id)
   if t is None:
      return jsonify(success = False)
   db.session.delete(t)
   db.session.commit()
   return jsonify(success = True)

