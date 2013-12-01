from app import db

USER  = 0
ADMIN = 1
YES   = 1
NO    = 0

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
   joined_communities = db.relationship('Community',
        secondary = user_community,
        primaryjoin = "user_community.c.user_id == User.id",
        secondaryjoin = "user_community.c.community_id == Community.id",
        backref = db.backref('members', lazy = 'dynamic'),
        lazy = 'dynamic')
   
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
      #return self.joined_communities.filter(user_community.c.community_id == community.id).count() > 0
      return False

   def join(self, community):
      if not self.is_member(community):
         self.joined_communities.append(community)
         return self

   def leave(self, community):
        if self.is_member(community):
            self.joined_communities.remove(community)
            return self


class Community(db.Model):
   __tablename__ = "community"
   id            = db.Column(db.Integer, primary_key = True)
   name          = db.Column(db.String(60), nullable=False)
   description   = db.Column(db.String(300))
   is_private    = db.Column(db.SmallInteger, nullable=False, default = NO)


   def __repr__(self):
      return '<Community %r: %r>' % (self.id, self.name)


