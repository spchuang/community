from model import Model


class Users(Model):
   def __init__(self):
      Model.__init__(self, db_name='community', name='users')
   
   def add_user(self, u):
      try:
         self.cursor.execute("""INSERT INTO users \
                              (first_name,last_name,user_name,password,email,gender) \
                              VALUES \
                              (%s,%s,%s,%s,%s,%s)""", 
                              (u.first_name,u.last_name, u.user_name,u.passowrd,u.email,u.gender))
         self.conn.commit()
      except Exception, e:
         print repr(e)
         return False
      
   def is_user(self, user_name, password):
      try:
        self.cursor.execute("SELECT * FROM users WHERE user_name=%s AND password=%s",(user_name, passowrd))
        result = self.cursor.fetchone()
        
      except Exception, e:
         print repr(e)
         return False
         
   def get_user(self, uid):
      try:
         self.cursor.execute("SELECT * FROM users WHERE id=%s",(uid))
         result = self.cursor.fetchone()
         u = User('test')
         return u
 
      except Exception, e:
         print repr(e)
         return None
           

   def get_users(self):
      try:
         self.cursor.execute("SELECT * FROM users")
         result = self.cursor.fetchall()
         return result
      except Exception, e:
         print repr(e)
         return None
  
class User(Model):
   def __init__(self, nickname = None):
      Model.__init__(self, db_name='community', name='users')
      self.nickname = nickname
      self.id       = 0 
      
   #flask-login required user methods
   def __repr__(self):
      return '<User %r>' % (self.nickname)
      
   

   def is_authenticated(self):
      return True
   
   def is_active(self):
      return True
   
   def is_anonymous(self):
      return False
      
   def get_id(self):
      return unicode(self.id)
   
   
   

   
        

