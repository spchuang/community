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
      
   def get_user_id(self, user_name, password):
      try:
         self.cursor.execute("SELECT id FROM users WHERE user_name=%s AND password=%s",(user_name, password))
         result = self.cursor.fetchone()
         if len(result) >0:
            return result['id']
      
         return False
         
      except Exception, e:
         print repr(e)
         return False
         
   
        
   #for flask-login
   def get_user(self, id):
      try:
          #get user info from db
         self.cursor.execute("SELECT user_name FROM users WHERE id=%s",(id))
         result = self.cursor.fetchone()
         
         print result
         if len(result) >0:
            return User(result['user_name'], id)
         return None
 
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

  
class User():
   def __init__(self, nickname, id):
      self.nickname = nickname
      self.id       = id
   
         
           
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
   
   
   

   
        

