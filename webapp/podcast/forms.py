import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp import db
from webapp.models import User


class CaptureForm(FlaskForm):
    link = StringField("Link", validators=[DataRequired()])
    submit = SubmitField("Submit")
