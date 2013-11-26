from model import Model

class Users(Model):
   def __init__(self):
      Model.__init__(self, db_name='community', name='users')
      
   def get_user_list(self):
      print "."
   
   def add_user(self):
      try:
         self.cursor.execute("""INSERT INTO users \
                              (first_name,last_name,user_name,password,email,gender) \
                              VALUES \
                              (%s,%s,%s,%s,%s,%s)""", 
                              ("test","test","test","test","test",0))
         self.conn.commit()
      except Exception, e:
         print repr(e)
         return False
      
   def test(self):
      print "."
      
   def get_users(self):
      try:
         self.cursor.execute("""SELECT * FROM users""")
         result = self.cursor.fetchall()
         return result
      except Exception, e:
         print repr(e)
         return False
         
   
        

