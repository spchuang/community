from db_util import DB

class Model: 
   def __init__(self, db_name=None, name=None):
      self.db_name         = db_name
      self.name            = name
      (self.conn, self.cursor) = DB.get_cursor('community')
      

   
   def __del__ (self):
      self.conn.close()

   