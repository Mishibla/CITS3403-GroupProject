from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, FloatField, FileField, TextAreaField, SubmitField
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
        ('yes', 'Yes'),
        ('no', 'No')
    ], validators=[DataRequired()])
    exclusive_skin = BooleanField('Exclusive Skins?', default=False)
    description = TextAreaField('Extra Description (specify your skins and exact elo)', validators=[Optional(), Length(max=500)])
    images = FileField('Upload images (max 4)', validators=[Optional()])
    submit =SubmitField('Create Ad')




