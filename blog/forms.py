"""
    use flask_wtf part of WTForms : pip install Flask-WTF
    in the new version of these packages were separated from each other
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from blog.models import User


class RegistrationForm(FlaskForm):
    """
        Build user registration form
        :param = for email validation you need to install email_validator lib
    """
    username = StringField('Username', validators=(DataRequired(), Length(min=4, max=25)))
    email = StringField('Email', validators=(DataRequired(), Email()))
    password = PasswordField('Password', validators=(DataRequired(),))
    confirm_password = PasswordField('Confirm Password',
                                     validators=(DataRequired(), EqualTo('password', message='passwords must match')))
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists')


class LoginForm(FlaskForm):
    """
        Build user Login Form
    """
    email = StringField('Email', validators=(DataRequired(), Email()))
    password = PasswordField('Password', validators=(DataRequired(),))
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    """
        Build profile form edit
    """
    username = StringField('Username', validators=(DataRequired(), Length(min=4, max=25)))
    email = StringField('Email', validators=(DataRequired(), Email()))

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])