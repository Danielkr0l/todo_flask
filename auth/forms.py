from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=4, max=150), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Length(min=4, max=150), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')