from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такая почта уже используется')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')


class ChangeUsernameForm(FlaskForm):
    old_username = StringField('Old Username', validators=[DataRequired()])
    new_username = StringField('New Username', validators=[DataRequired()])
    submit_username = SubmitField('Change Username')

    def validate_old_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('Неверное текущее имя.')

    def validate_new_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and field.data != current_user.username:
            raise ValidationError('Это имя уже занято.')

class ChangeEmailForm(FlaskForm):
    old_email = StringField('Old Email', validators=[DataRequired(), Email()])
    new_email = StringField('New Email', validators=[DataRequired(), Email()])
    submit_email = SubmitField('Change Email')

    def validate_old_email(self, field):
        if field.data != current_user.email:
            raise ValidationError('Неверный текущий email.')

    def validate_new_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and field.data != current_user.email:
            raise ValidationError('Этот email уже используется.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit_password = SubmitField('Change password')
