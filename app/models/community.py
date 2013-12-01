from app.models.model import Model


class Community(Model):
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
         
   def get_user_communities(self, user_id):
      try:
         self.cursor.execute("""SELECT id, name, description FROM communities \
                                 JOIN user_in_community \
                                 WHERE communities.id = user_in_community.community_id AND user_id=%s""", (user_id))
         result = self.cursor.fetchall()
         return result
      except Exception, e:
         print repr(e)
         return False
   
   def get_public_communities(self):
      try:
         self.cursor.execute("""SELECT id, name, description FROM communities WHERE is_private=0""", )
         result = self.cursor.fetchall()
         return result
      except Exception, e:
         print repr(e)
         return False
  
   def user_join_community(self, user_id, community_id):
      try:
         self.cursor.execute("""INSERT INTO user_in_community \
                              (user_id,community_id) \
                              VALUES \
                              (%s,%s)""", 
                              (user_id, community_id))
         self.conn.commit()
      except Exception, e:
         print repr(e)
         return False
