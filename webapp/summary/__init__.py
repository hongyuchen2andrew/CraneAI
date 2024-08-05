from flask import Blueprint

bp = Blueprint('summary', __name__)

from webapp.summary import routes
