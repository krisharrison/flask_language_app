from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user



class Registration(FlaskForm):
    username = StringField('Username', 
                          validators= [DataRequired(), 
                           Length(min=3, max=30)])
    email = StringField('Email', 
                        validators=[DataRequired(),
                         Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Error: username already exist!') 
    

    def validate_email(self, email):
        user_email = User.query.filter_by(email = email.data).first()
        if user_email:
            raise ValidationError('Error: email already exist!')


class Login(FlaskForm):
    username = StringField('Username', 
                          validators= [DataRequired(), 
                           Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Account(FlaskForm):
    username = StringField('New Username', 
                          validators= [DataRequired(), 
                           Length(min=3, max=30)])
    email = StringField('New Email', 
                        validators=[DataRequired(),
                         Email()])
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Error: username already exist!') 
    

    def validate_email(self, email):
        if email.data != current_user.email:
            user_email = User.query.filter_by(email = email.data).first()
            if user_email:
                raise ValidationError('Error: email already exist!')