import MySQLdb

class DB:
   #should eventually use a mysql user and some kind of db
   db_map = {
      'community': '127.0.0.1',
   }
   
   username = 'test'
   password = 'test'
   
   @classmethod
   def get_cursor(self, db_name):
      conn = MySQLdb.connect(self.db_map[db_name], self.username, self.password, db_name, use_unicode=True, charset='utf8')
      cursor = conn.cursor(MySQLdb.cursors.DictCursor)
      return (conn, cursor)
