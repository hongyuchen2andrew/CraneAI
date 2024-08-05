from flask import Blueprint

bp = Blueprint("capture", __name__)

from webapp.capture import routes
