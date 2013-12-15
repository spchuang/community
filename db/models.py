from src import db
from datetime import datetime
import json

USER  = 0
ADMIN = 1
NO    = 0
YES   = 1
NOT_COMMENT = -1

#see http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

user_community = db.Table('user_community',
   db.Column('user_id',      db.Integer, db.ForeignKey('user.id')),
   db.Column('community_id', db.Integer, db.ForeignKey('community.id')),
   db.UniqueConstraint('user_id', 'community_id')
)

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

   members = db.relationship('User',
      secondary = user_community,
      primaryjoin = "user_community.c.community_id == Community.id",
      secondaryjoin = "user_community.c.user_id == User.id",
      backref = db.backref('joined_communities', lazy = 'dynamic'),
      lazy = 'dynamic')

   posts = db.relationship('Post', lazy='dynamic')

   def create_post(self, post):
      if post.user_id is None:
         raise Exception("Who created this post?")
      post.community_id = self.id
      post.parent_id    = None
      self.posts.append(post)
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

class Post(db.Model):
   __tablename__ = 'post'
   id            = db.Column(db.Integer, primary_key = True)
   community_id  = db.Column(db.Integer, db.ForeignKey('community.id'))
   user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
   parent_id     = db.Column(db.Integer, db.ForeignKey('post.id'))
   created       = db.Column(db.DateTime, default = datetime.now)
   modified      = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)
   body          = db.Column(db.String(1000), nullable=False)

   comments = db.relationship('Post', lazy='dynamic')
   user     = db.relationship('User')


   @property
   def serialize(self):
      """Return object data in easily serializeable format"""
      return {
         'id'           : self.id,
         'community_id' : self.community_id,
         'body'         : self.body,
         'created'      : self.created,
         'modified'     : self.modified,
      }

   def __repr__(self):
      return '<Post %r>' % (self.id)

   def comment(self, post):
      #only allow comment on root post (parent)
      if self.parent_id is not None:
         raise Exception("You can't comment on a comments")
      if post.user_id is None:
         raise Exception("Who commented it?")

      print self
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
               Post,
               User.first_name,
               User.last_name,
               User.id
            )\
            .join(User)\
            .filter(Post.community_id== c_id, Post.parent_id==None)\
            .order_by(Post.created.desc())
   return query
