# all the imports
from models.users import Users
from controllers import account
import os
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template, flash
from flask.ext.login import LoginManager




#----------------------------------------
# initialization
#----------------------------------------
DATABASE = 'community.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

#Todo: model abstraction for database access s
def connect_db():	
   return sqlite3.connect(app.config['DATABASE'])
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	

#----------------------------------------
# controllers
#----------------------------------------
@app.route('/')
def show_entries():
   cur = g.db.execute('select title, text from entries order by id desc')
   entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
   return render_template('show_entries.html', entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
   if not session.get('logged_in'):
      abort(401)
   g.db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
   g.db.commit()
   flash('New entry was successfully posted')
   return redirect(url_for('show_entries'))

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
      if request.form['username'] != app.config['USERNAME']:
         error = 'Invalid username'
      elif request.form['password'] != app.config['PASSWORD']:
         error = 'Invalid password'
      else:
         session['logged_in'] = True
         flash('You were logged in')
      return redirect(url_for('login'))
   	
   if session.get('logged_in'):
      return redirect(url_for('community'))
   return render_template('login.html', error=error)

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   flash('You were logged out')
   return redirect(url_for('login'))
	
	
@app.route('/signup', methods=['GET','POST'])
def signup():
   if request.method == 'POST':
      #Todo: form validation
      g.db.execute('insert into user (first_name, last_name, user_name, password, gender, email) values (?, ?, ?, ?, ?, ?)',
               [request.form['first_name'], request.form['last_name'], request.form['user_name'], request.form['password'], request.form['gender'], request.form['email']])
      g.db.commit()
      cur = g.db.execute('select user_name from user order by id desc')
      #Todo: Error handling
      print cur.fetchall()
      
   #return redirect(url_for('/home'))
   return render_template('signup.html')
'''

@login_manager.user_loader
def load_user(id):
   users = Users()
   return users.get_user(int(id))

@app.route('/home')
def home():
   return render_template('home.html')

	
@app.route('/community')
def community():
   return render_template('communiy_list.html')
 
#bind URL
app.add_url_rule('/login',    methods=['GET', 'POST'],   view_func=account.login)
app.add_url_rule('/logout',   methods=['GET'],           view_func=account.logout)
app.add_url_rule('/signup',   methods=['GET', 'POST'],   view_func=account.signup)
app.add_url_rule('/profile',  methods=['GET'],           view_func=account.profile)


#----------------------------------------
# launch
#----------------------------------------   


if __name__ == '__main__':
   #u = Users()
   #u.add_user()
   #users = u.get_users()
   #print users
   port = int(os.environ.get("PORT", 5000))
   app.run(host='0.0.0.0', port=port)