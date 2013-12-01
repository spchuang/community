import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'development key'

#DB config
DB_CONFIG = {
   "HOST" : "sql3.freesqldatabase.com",
   "USER" : "sql322886",
   "PASS" : "wD5*sF5%",
   "DB"   : "sql322886"
}


SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s"%(DB_CONFIG['USER'], DB_CONFIG['PASS'],DB_CONFIG['HOST'])