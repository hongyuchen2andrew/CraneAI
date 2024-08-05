import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp import db
from webapp.models import User

class AskMeForm(FlaskForm):
    user_input = StringField('Enter your text', validators=[DataRequired()])
    submit = SubmitField('Submit')

