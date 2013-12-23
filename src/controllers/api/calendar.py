from flask import Blueprint, jsonify, g, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateEventForm
from db.models import Event, Community, User, get_event_list
from src import db


api = Blueprint('calendar', __name__, url_prefix='/api')

def construct_event(c_id):
   def serialize(e):
      if c_id == 'all':
         event = e.Event.serialize
      else:
         event = e.serialize
         return event
   return serialize



#need the extra /events in case later on we use the calendar to display other things
@api.route('/community/<c_id>/calendar/events', methods=['GET'])
@login_required
def list(c_id):
   if c_id == 'all':
      event_list = get_event_list(g.user)
   else:
      event_list = Event().query.filter_by(community_id= c_id).all()

   return jsonify(success = True, data= map(construct_event(c_id), event_list))


@api.route('/community/<c_id>/calendar/events',methods=['POST'])
@login_required
def new_event(c_id):
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

@api.route('/community/<c_id>/calendar/events/<e_id>',methods=['PUT'])
@login_required
def update_event(c_id, e_id):
   form = CreateEventForm()
   if form.validate_on_submit():
      e = Event().query.filter_by(id=e_id).first() 
      e.name         = form.name.data
      e.start_on     = form.start.data
      e.end_on       = form.end.data
      e.modified_by  = g.user.id
      e.description  = form.description.data

      db.session.add(e)
      db.session.commit()
      updated_event = construct_event(e.community_id)(e)
      return jsonify(success = True, data=updated_event)  
      return jsonify(success = False, errors = form.errors)
		
@api.route('/community/<c_id>/calendar/events/<e_id>',methods=['DELETE'])
@login_required
def delete_event(c_id, e_id):
	  
   e = Event().query.filter_by(id=e_id).first()
   if e is None:
      return jsonify(success = False)
   db.session.delete(e)
   db.session.commit()
   return jsonify(success = True)

	

