from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class RegiterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')
    name = StringField('name', validators=[InputRequired()])
    phone_number = StringField('phone_number', validators=[InputRequired()])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])