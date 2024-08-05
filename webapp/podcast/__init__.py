from flask import Blueprint

bp = Blueprint("podcast", __name__)

from webapp.podcast import routes
