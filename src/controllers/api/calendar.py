from flask import Blueprint, jsonify, g, url_for, render_template, request, abort
from flask.ext.login import login_required
from src.forms import CreateEventForm
from db.models import Event, Community, User, get_event_list
from src import db

api = Blueprint('calendar', __name__, url_prefix='/api/calendar')

@api.route('/list', methods=['GET'])
@login_required
def list():
   type = request.args.get('get') or 'community'

   if type == 'community':
      c_id = request.args.get('c_id')
      events = Event().query.filter_by(community_id= c_id).all()
      return jsonify(success = True, data= [
               {'id': e.id, 'name': e.name, 'date': e.date, 'description': e.description}
               for e in events
          ])
   elif type == g.user.user_name:
      events = get_event_list(g.user)
      return jsonify(success = True, data= [
               {'id': e.Event.id, 'name': e.Event.name, 'date': e.Event.date, 'description': e.Event.description}
               for e in events
          ])


@api.route('/create',methods=['POST'])
@login_required
def create_event():
   c_id = request.args.get('c_id')
   if c_id is None:
      return jsonify(success = False, errors = "What community?")

   form = CreateEventForm()
   if form.validate_on_submit():
      new_event = Event(name   = form.name.data, 
      							date = form.date.data,
                                description  = form.description.data)
      c = Community().query.filter_by(id=c_id).first()
      c.create_event(new_event)
      db.session.add(c)
      db.session.commit()
      return jsonify(success = True)
   return jsonify(success = False, errors = form.errors)