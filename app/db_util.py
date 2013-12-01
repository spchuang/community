import MySQLdb

class DB:
   #should eventually use a mysql user and some kind of db
   db_map = {
#      'community': '127.0.0.1',
   }
   
#   //username = 'test'
#   //password = 'test'
   
   host = "sql3.freesqldatabase.com"
   username = "sql322886"
   db   = "sql322886"
   password = "wD5*sF5%"
   

   @classmethod
   def get_cursor(self, db_name):
      #conn = MySQLdb.connect(self.db_map[db_name], self.username, self.password, db_name, use_unicode=True, charset='utf8')
      conn = MySQLdb.connect(self.host, self.username, self.password, self.db, use_unicode=True, charset='utf8')
      cursor = conn.cursor(MySQLdb.cursors.DictCursor)
      return (conn, cursor)
