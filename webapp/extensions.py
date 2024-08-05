from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_dramatiq import Dramatiq
from flask_security import Security
from sqlalchemy_searchable import make_searchable


db = SQLAlchemy()
make_searchable(db.metadata)
migrate = Migrate()
dramatiq = Dramatiq()
mail = Mail()
security = Security()
