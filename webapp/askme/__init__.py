from flask import Blueprint

bp = Blueprint('askme', __name__)

from webapp.askme import routes
