from flask import render_template, Flask , redirect
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, RadioField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import login_user



app = Flask(__name__)

class AddMovie(FlaskForm):
    name = StringField("Movie Name", validators=[DataRequired()])
    description = StringField("Movie Description", validators=[DataRequired()])
    img = FileField("Movie Image", validators=[FileRequired()])
    watch = StringField("Movie Link", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Addseries(FlaskForm):
    name = StringField("Series Name", validators=[DataRequired()])
    description = StringField("Series Description", validators=[DataRequired()])
    img = FileField("Series Image", validators=[FileRequired()])
    watch = StringField("Series Link", validators=[DataRequired()])
    submit = SubmitField("Submit")





class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired(), Length(min=8, max=20, message="Password is incorrect")])
    repeat_password = PasswordField("Re-enter Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("register")

class LoginForm(FlaskForm):
    username = StringField("enter username", validators=[DataRequired()])
    password = PasswordField("enter password",validators=[DataRequired()])
    submit = SubmitField("authorize")
