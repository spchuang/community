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
LOCAL_DB_CONFIG = {
   "HOST" : "127.0.0.1",
   "USER" : "root",
   "PASS" : "",
   "DB"   : "community"
}

SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s"%(DB_CONFIG['USER'], DB_CONFIG['PASS'],DB_CONFIG['HOST'],DB_CONFIG['DB'])
#SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s"%(LOCAL_DB_CONFIG['USER'], LOCAL_DB_CONFIG['PASS'],LOCAL_DB_CONFIG['HOST'],LOCAL_DB_CONFIG['DB'])


#oauth info
FACEBOOK_APP_ID = '499438820169724'
FACEBOOK_APP_SECRET = '485d362f9194ba2fe00d6db78b7460dc'