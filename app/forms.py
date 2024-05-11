from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, FloatField, FileField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class AdForm(FlaskForm):
    titlerequest = StringField('Title of ad*', validators=[DataRequired(), Length(max=50)])
    games = SelectField('Game Selling?*', choices=[
        ('', 'Select an option'),
        ('CSGO', 'CSGO'),
        ('League', 'League of Legends'),
        ('Overwatch', 'Overwatch'),
        ('Valorant', 'Valorant')
    ], validators=[DataRequired()])
    rank = SelectField('Rank*', choices=[('', 'Select an option')], validators=[DataRequired()])
    price = FloatField('Price (AUD)*', validators=[DataRequired()])
    skin = SelectField('Skins*', choices=[
        ('', 'Select an option'),
        (True, 'Yes'),
        (False, 'No')
    ], validators=[DataRequired()])
    exclusive_skin = BooleanField('Exclusive Skins?', default=False)
    description = TextAreaField('Extra Description (specify your skins and exact elo)', validators=[Optional(), Length(max=500)])
    images = FileField('Upload images (max 4)', validators=[Optional()])
    submit =SubmitField('Create Ad')

class LoginForm(FlaskForm):
    log_username= StringField('Enter Username', validators=[DataRequired(), Length(max=50)])
    log_password= PasswordField('Enter password', validators=[DataRequired(), Length(max=50)])
    submit=SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField('Enter Username*', validators=[DataRequired(), Length(max=30)])
    display_name = StringField('Enter Display Name*', validators=[DataRequired(), Length(max=30)])
    password = PasswordField('Enter password*', validators=[DataRequired(), Length(max=20)])
    submit =SubmitField('Create Account')
