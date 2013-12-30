from src import db
from datetime import datetime
import dateutil.parser as parser
import json

USER  = 0
ADMIN = 1
NO    = 0
YES   = 1
NOT_COMMENT = -1

#see http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
def dump_datetime(value):
   if value is None:
      return None
   return value.strftime("%Y-%m-%d") +"T"+ value.strftime("%H:%M:%S")+"Z"

user_community = db.Table('user_community',
   db.Column('user_id',      db.Integer, db.ForeignKey('user.id')),
   db.Column('community_id', db.Integer, db.ForeignKey('community.id')),
   db.UniqueConstraint('user_id', 'community_id')
)

class Event(db.Model):
   __tablename__ = "event"
   id            = db.Column(db.Integer, primary_key = True)
   community_id  = db.Column(db.Integer, db.ForeignKey('community.id'))
   name          = db.Column(db.String(60), nullable=False)
   start_on      = db.Column(db.DateTime, nullable=False)
   end_on        = db.Column(db.DateTime, nullable=False)
   created_by    = db.Column(db.Integer, db.ForeignKey('user.id'))
   created_on    = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
   modified_by   = db.Column(db.Integer, db.ForeignKey('user.id'))
   modified_on   = db.Column(db.DateTime, nullable=False, default = datetime.utcnow, onupdate=datetime.utcnow)
   description   = db.Column(db.Text)

   @property
   def serialize(self):
      """Return object data in easily serializeable format"""
      return {
         'id'           : self.id,
         #had to change to 'title' for full calendar, might change
         'title'        : self.name,
         'host'         : self.created_by,
         'start'        : self.start_on.isoformat(),
         'end'          : self.end_on.isoformat(),
         'description'  : self.description,
         'color'        : 'blue',
      }

   def __repr__(self):
      return '<Event %r %r>' % (self.id, self.name)


class User(db.Model):
   __tablename__ = "user"
   id            = db.Column(db.Integer, primary_key = True)
   first_name    = db.Column(db.String(30), nullable=False)
   last_name     = db.Column(db.String(30), nullable=False)
   user_name     = db.Column(db.String(30),  index = True, unique = True, nullable=False)
   password      = db.Column(db.CHAR(60), nullable=False)
   email         = db.Column(db.String(120), index = True, unique = True, nullable=False)
   gender        = db.Column(db.SmallInteger, nullable=False)
   permission    = db.Column(db.SmallInteger, nullable=False, default=USER)
   fb_id         = db.Column(db.BigInteger(unsigned=True), default=None)

   @property
   def serialize(self):
      """Return object data in easily serializeable format"""
      return {
         "first_name" : self.first_name.capitalize(),
         "last_name"  : self.last_name.capitalize(),
         "name"       : self.first_name.capitalize() + ' ' + self.last_name.capitalize(),
         "user_id"    : self.id,
      }

   def __repr__(self):
      return '<User %r>' % (self.user_name)
   
   def is_authenticated(self):
      return True
   
   def is_active(self):
      return True
   
   def is_anonymous(self):
      return False
   
   def get_id(self):
      return unicode(self.id)

   def is_member(self, community):
      return self.joined_communities.filter(user_community.c.community_id == community.id).count() > 0

   def join(self, community):
      if self.is_member(community):
         raise Exception("Already a member of '%s'" %community.name)
      self.joined_communities.append(community)
      return self

   def leave(self, community):
      if not self.is_member(community):
         raise Exception("Not a member of '%s'" %community.name)
      self.joined_communities.remove(community)
      return self



class Community(db.Model):
   __tablename__ = "community"
   id            = db.Column(db.Integer, primary_key = True)
   name          = db.Column(db.String(60), nullable=False)
   description   = db.Column(db.Text)
   is_private    = db.Column(db.SmallInteger, nullable=False, default = NO)
   created_on    = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

   members = db.relationship('User',
      secondary = user_community,
      primaryjoin = "user_community.c.community_id == Community.id",
      secondaryjoin = "user_community.c.user_id == User.id",
      backref = db.backref('joined_communities', lazy = 'dynamic'),
      lazy = 'dynamic')

   
   events = db.relationship('Event', lazy = 'dynamic')
   posts = db.relationship('Post', lazy='dynamic')

   @property
   def serialize(self):
      """Return object data in easily serializeable format"""
      return {
         'id'           : self.id,
         'name'         : self.name,
         'description'  : self.description,
         'is_private'   : self.is_private,
      }

   def __repr__(self):
      return '<Community %r: %r>' % (self.id, self.name)


   def create_post(self, post):
      if post.user_id is None:
         raise Exception("Who created this post?")
      post.community_id = self.id
      post.parent_id    = None
      self.posts.append(post)
      return self

   #prob add in user_id check later, event creator
   def create_event(self, event):
      event.community_id = self.id
      self.events.append(event)
      return self

   def __repr__(self):
      return '<Community %r: %r>' % (self.id, self.name)

'''
#do we need a table for wall? if there's only one wall per community
class Wall(db.Model):
   __tablename__ = "wall"
   id            = db.Column(db.Integer, primary_key = True)
   community_id  = db.Column(db.Integer, db.ForeignKey('community.id'), nullabe=False)
   name          = db.Column(db.String(60), nullable = False)
   posts = db.relationship('Post', lazy='dynamic')

   def create(self, post):
      if post.user_id is None:
         raise Exception("Who created this post?")
      post.community_id = self.community_id
      self.posts.append(post)
      return self

   def __repr__(self):
      return '<Wall %r: %r>' % (self.id, self.name)
'''

class Task(db.Model):
   __tablename__ = 'task'
   id            = db.Column(db.Integer, primary_key = True)
   name          = db.Column(db.String(60), nullable=False)
   assigned_to   = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
   assigned_by   = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
   summary       = db.Column(db.String(1000), nullable=False, default="")
   description   = db.Column(db.String(1000), nullable=False, default ="")
   created_by    = db.Column(db.Integer, db.ForeignKey('user.id'))
   created_on    = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
   modified_by   = db.Column(db.Integer, db.ForeignKey('user.id'))
   modified_on   = db.Column(db.DateTime, nullable=False, default = datetime.utcnow, onupdate=datetime.utcnow)
   community_id  = db.Column(db.Integer, db.ForeignKey('community.id'))
   parent_id     = db.Column(db.Integer, db.ForeignKey('task.id'), default=None)
   status        = db.Column(db.Integer, default = 0, nullable=False)

   assigned_to_user = db.relationship('User', primaryjoin = "User.id == Task.assigned_to")

   @property
   def serialize(self):
      """Return object data in easily serializeable format"""
      s = {
         'id'           : self.id,
         'community_id' : self.community_id,
         'name'         : self.name,
         'summary'      : self.summary,
         'description'  : self.description,
         
         'created_on'   : dump_datetime(self.created_on),
         'modified_on'  : dump_datetime(self.modified_on),
         'status'       : self.status
         #'assigned_to'  : self.assigned_to_user.serialize or None
      }
      if self.parent_id is not None:
         s['parent_id'] = self.parent_id
      return s


   def __repr__(self):
      return '<Task %r %s>' % (self.id, self.name)

class AcitivityFeed(db.Model):
   __tablename__ = 'activity_feed'
   id            = db.Column(db.Integer, primary_key = True)
   
class Notification(db.Model):
   __tablename__ = 'notification'
   id            = db.Column(db.Integer, primary_key = True)



class Post(db.Model):
   __tablename__ = 'post'
   id            = db.Column(db.Integer, primary_key = True)
   community_id  = db.Column(db.Integer, db.ForeignKey('community.id'))
   user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
   parent_id     = db.Column(db.Integer, db.ForeignKey('post.id'))
   created_on    = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
   modified_on   = db.Column(db.DateTime, nullable=False, default = datetime.utcnow, onupdate=datetime.utcnow)
   body          = db.Column(db.String(1000), nullable=False)

   #relationships
   comments = db.relationship('Post', lazy='joined')
   user     = db.relationship('User')

   @property
   def serialize(self):
      """Return object data in easily serializeable format"""
      s = {
         'id'           : self.id,
         'community_id' : self.community_id,
         'body'         : self.body,
         
         'created_on'   : dump_datetime(self.created_on),
         'modified_on'  : dump_datetime(self.modified_on),
         'user'         : self.user.serialize
      }
      if self.parent_id is not None:
         s['parent_id'] = self.parent_id
      return s

   def __repr__(self):
      return '<Post %r>' % (self.id)

   def comment(self, post):
      #only allow comment on root post (parent)
      if self.parent_id is not None:
         raise Exception("You can't comment on a comments")
      if post.user_id is None:
         raise Exception("Who commented it?")

      post.community_id = self.community_id
      post.parent_id    = self.id
      self.comments.append(post)
      return self


#DB query funtions
def get_community_list(user, is_user_filter=False):
   subq_members = db.session.query(
                        (user_community.c.community_id).label('id'),
                        db.func.count(user_community.c.user_id).label('num_members')
                     )\
                     .group_by(user_community.c.community_id)\
                     .subquery()

   subq_is_member = db.session.query(
                        (user_community.c.community_id).label('id'),
                        db.func.count(user_community.c.user_id).label('is_member')
                     )\
                     .filter(user_community.c.user_id==user.id)\
                     .group_by(user_community.c.community_id)\
                     .subquery()

   #return number of members in each group and whether the user is a member
   query = db.session.query(
               Community,
               subq_members.c.num_members,
               subq_is_member.c.is_member
            )
   if is_user_filter:
      query = query.join(user_community)\
         .filter(user_community.c.community_id == Community.id, user_community.c.user_id == user.id)

   query = query.outerjoin(subq_members, subq_members.c.id == Community.id)\
               .outerjoin(subq_is_member, subq_is_member.c.id == Community.id)

   return query

def get_wall_posts(c_id):
   query = db.session.query(
               Post
            )\
            .join(User)\
            .options(db.joinedload(Post.comments))\
            .filter(Post.community_id== c_id, Post.parent_id==None)\
            .order_by(Post.created_on.desc())

   return query

def get_post_comments(p_id):
   query = db.session.query(
               Post,
            )\
            .join(User)\
            .options(db.joinedload(Post.comments))\
            .filter(Post.community_id== c_id, Post.parent_id==None)\
            .order_by(Post.created_on.desc())

   return query

def get_event_list(user):
   subq_communities = db.session.query(
                       user_community,
                      )\
                      .filter(user_community.c.user_id==user.id)\
                      .subquery()
   
   query = db.session.query(
           Event,
           subq_communities
           )\
           .filter(Event.community_id==subq_communities.c.community_id)\
           .order_by(Event.start_on.asc())

   return query

