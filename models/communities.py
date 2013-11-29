from model import Model


class Communities(Model):
   def __init__(self):
      Model.__init__(self, db_name='community', name='communities')
   
   def add_community(self, c):
      try:
         self.cursor.execute("""INSERT INTO communities \
                              (name,description,is_public) \
                              VALUES \
                              (%s,%s,%s)""", 
                              (c['name'],c['description'], c['is_public']))
         self.conn.commit()
      except Exception, e:
         print repr(e)
         return False
      
  
