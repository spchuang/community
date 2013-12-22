from flask import Blueprint, jsonify, g, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateEventForm
from db.models import Event, Community, User, get_event_list
from src import db


api = Blueprint('calendar', __name__, url_prefix='/api/calendar')

def construct_event(c_id):
   def serialize(e):
      event = e.serialize
      return event
   return serialize

@api.route('/list', methods=['GET'])
@login_required
def list():
   c_id = request.args.get('c_id')
   if c_id == 'all':
      event_list = get_event_list(g.user)
   else:
      event_list = Event().query.filter_by(community_id= c_id).all()

   def merge_event(e):
      if c_id == 'all':
        event = e.Event.serialize
      else:
        event = e.serialize
        #need to include action in construct_event: bug with deleting new events w.o reloading page
      event['action'] = {
         'update' :url_for('calendar.update_event', e_id= event['id']),
         'delete' :url_for('calendar.delete_event', e_id= event['id'])
      }     
      return event

   return jsonify(success = True, data= map(merge_event, event_list))



@api.route('/new_event',methods=['POST'])
@login_required
def new_event():
   c_id = request.args.get('c_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")
   form = CreateEventForm()
   if form.validate_on_submit():
   	e = Event(name = form.name.data,
      			start_on = form.start.data,
               end_on = form.end.data,
               created_by = g.user.id,
               description  = form.description.data)
   	c = Community().query.filter_by(id=c_id).first()
   	c.create_event(e)
   	db.session.add(c)
   	db.session.commit()

   	new_event = construct_event(c_id)(e)
   	return jsonify(success = True, data=new_event)
   return jsonify(success = False, errors = form.errors)

@api.route('/update_event',methods=['PUT'])
@login_required
def update_event():
   e_id = request.args.get('e_id')
   if e_id is None:
      return jsonify(success = False, errors = "What event?")   
   
   form = CreateEventForm()
   if form.validate_on_submit():
      e = Event().query.filter_by(id=e_id).first() 
      e.name = form.name.data
      e.start_on = form.start.data
      e.end_on = form.end.data
      e.modified_by = g.user.id
      e.description = form.description.data
      db.session.add(e)
      db.session.commit()

      updated_event = construct_event(e_id)(e)
      return jsonify(success = True, data=updated_event)  
   return jsonify(success = False, errors = form.errors)

@api.route('/delete_event',methods=['DELETE'])
@login_required
def delete_event():
   e_id = request.args.get('e_id')
   if e_id is None:
      return jsonify(success = False, errors = "What event?")  

   e = Event().query.filter_by(id=e_id).first()
   db.session.delete(e)
   db.session.commit()
   return jsonify(success = True)

