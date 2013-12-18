from flask import Blueprint, jsonify, g, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateEventForm
from db.models import Event, Community, User, get_event_list
from src import db

api = Blueprint('calendar', __name__, url_prefix='/api/calendar')

@api.route('/list', methods=['GET'])
@login_required
def list():
   c_id = request.args.get('c_id')
   if(c_id == 'all'):
      events = get_event_list(g.user)
      return jsonify(success = True, data= [
               e.Event.serialize
               for e in events
          ])
   else:
      events = Event().query.filter_by(community_id= c_id).all()
      return jsonify(success = True, data= [
               e.serialize
               for e in events
          ])



@api.route('/new_event',methods=['POST'])
@login_required
def new_event():
   c_id = request.args.get('c_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")

   form = CreateEventForm()
   if form.validate_on_submit():
      new_event = Event(name   = form.name.data, 
      							    start_on = form.start.data,
                        end_on = form.end.data,
                        created_by = g.user.id,
                        description  = form.description.data)
      c = Community().query.filter_by(id=c_id).first()
      c.create_event(new_event)
      db.session.add(c)
      db.session.commit()
      return jsonify(success = True)
   return jsonify(success = False, errors = form.errors)

"""
@api.route('/update_event',methods=['POST'])
@login_required
def update_event():
"""


@api.route('/delete_event',methods=['POST'])
@login_required
def delete_event():
   print "yes"
   c_id = request.args.get('c_id')

