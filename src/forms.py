from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, DateTimeField, validators
from wtforms.validators import DataRequired

class LoginForm(Form):
    user_name = TextField('user_name', [validators.Required()])
    password  = TextField('password',  [validators.Required()])
    remember_me = BooleanField('remember_me', default = False)
    
class SignupForm(Form):
   user_name   = TextField('user_name',    [validators.Length(min=4, max=30)])
   first_name  = TextField('first_name',   [validators.Required()])
   last_name   = TextField('last_name',    [validators.Required()])
   email       = TextField('email',        [validators.Required()])
   gender      = BooleanField('user_name', [validators.Required()], default = 0)
   password    = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
   confirm     = PasswordField('Repeat Password')
   

class CreateCommunityForm(Form):
   name         = TextField('name',          [validators.Required()])
   description  = TextField('description')

class CreateWallPostForm(Form):
   body   = TextField('body',  [validators.Required(),validators.Length(max=1000)])

class WallPostCommentForm(Form):
   body   = TextField('body',  [validators.Required(),validators.Length(max=1000)])

class CreateEventForm(Form):
   name        = TextField('name', [validators.Required()]) 
   start       = DateTimeField('start', [validators.Required()])
   end         = DateTimeField('end', [validators.Required()])
   description = TextField('description')
   
class TaskForm(Form):
   name     = TextField('name', [validators.Required()]) 
   summary  = TextField('summary')
   description = TextField('description')
   
