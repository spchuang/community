from app import db

USER  = 0
ADMIN = 1

class User(db.Model):
    id            = db.Column(db.Integer, primary_key = True)
    first_name    = db.Column(db.String(50), nullable=False)
    last_name     = db.Column(db.String(50), nullable=False)
    user_name     = db.Column(db.String(50),  index = True, unique = True, nullable=False)
    email         = db.Column(db.String(120), index = True, unique = True, nullable=False)
    gender        = db.Column(db.SmallInteger, nullable=False)
    permission    = db.Column(db.SmallInteger, nullable=False, default=0)
    
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = USER)

    def __repr__(self):
        return '<User %r>' % (self.user_name)
        
        
'''
CREATE TABLE users(
   id INTEGER(11) NOT NULL AUTO_INCREMENT, 
   first_name VARCHAR(20)     NOT NULL,
   last_name  VARCHAR(20)     NOT NULL,
   user_name  VARCHAR(30)     NOT NULL, 
   password   CHAR(60) BINARY NOT NULL,
   email      VARCHAR(100)    NOT NULL,
   gender     TINYINT(2)      NOT NULL,
   permission TINYINT(3)      NOT NULL DEFAULT 0,
   PRIMARY KEY (id),
   Unique(email),
   Unique(user_name)
  /*
   TODO: add more fields for user profiles like about me, birthday, and other shit
  */
);

'''