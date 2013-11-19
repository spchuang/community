# all the imports
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash

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



def connect_db():	
	return sqlite3.connect(app.config['DATABASE'])
	
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404
	
@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

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
	
	
@app.route('/signup')
def signup():
	return render_template('signup.html')
	
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')
	
@app.route('/community')
def community():
	return render_template('communiy_list.html')
 
#----------------------------------------
# launch
#----------------------------------------   
if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)