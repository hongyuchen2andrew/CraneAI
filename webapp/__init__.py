from flask import Flask
import flask_wtf

from webapp.extensions import db, migrate, dramatiq, mail, security
from webapp.models import user_datastore


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    flask_wtf.CSRFProtect(app)
    db.init_app(app)
    migrate.init_app(app, db)
    dramatiq.init_app(app)
    mail.init_app(app)
    security.init_app(app, user_datastore)

    from webapp.main import bp as main_bp

    app.register_blueprint(main_bp)

    from webapp.summary import bp as summary_bp

    app.register_blueprint(summary_bp, url_prefix="/summary")

    from webapp.capture import bp as capture_bp

    app.register_blueprint(capture_bp, url_prefix="/captures")

    from webapp.podcast import bp as podcast_bp

    app.register_blueprint(podcast_bp, url_prefix="/podcasts")

    # from webapp.auth import bp as auth_bp

    # app.register_blueprint(auth_bp, url_prefix="/auth")

    from webapp.askme import bp as askme_bp
    app.register_blueprint(askme_bp, url_prefix="/askme")


    return app
