import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "super-secret-key"
    SECURITY_PASSWORD_SALT = os.environ.get(
        "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509634"
    )

    # have session and remember cookie be samesite (flask/flask_login)
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"
    SECURITY_REGISTERABLE = True
    WTF_CSRF_CHECK_DEFAULT = False
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]

    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI") or "postgresql://ian@localhost:5432/gino"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_SEND_REGISTER_EMAIL = False

    SECURITY_OAUTH_ENABLE = True
    SECURITY_OAUTH_BUILTIN_PROVIDERS = ["google"]
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # DRAMATIQ_BROKER = "dramatiq_pg:PostgresBroker"
    DRAMATIQ_BROKER = "dramatiq.brokers.redis:RedisBroker"
    # DRAMATIQ_BROKER_URL = SQLALCHEMY_DATABASE_URI + "?minconn=8&maxconn=8"
    DRAMATIQ_BROKER_URL = "redis://localhost:6379/0"
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = "your_mail_server"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "your_username"
    MAIL_PASSWORD = "your_password"
    MAIL_DEFAULT_SENDER = "your_email@example.com"
