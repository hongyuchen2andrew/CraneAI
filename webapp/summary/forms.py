import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp import db
from webapp.models import User

class SmartSummaryForm(FlaskForm):
    user_input = StringField('Enter your text')
    length = RadioField('Length', choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')], validators=[DataRequired()])
    style = RadioField('Style', choices=[('paragraph', 'Paragraph'), ('bullet', 'Bullet Points')], validators=[DataRequired()])
    time_range = SelectField('Time Range', choices=[('24h', 'Last 24 hours'), ('3d', 'Last 3 days'), ('1w', 'Last 1 week')], validators=[DataRequired()])
    submit = SubmitField('Submit')

