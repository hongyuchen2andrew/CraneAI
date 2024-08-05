import json
import uuid

from flask_security import (
    AsaList,
    RoleMixin,
    SQLAlchemyUserDatastore,
    UserMixin,
    naive_utcnow,
)
from flask_sqlalchemy.query import Query
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.dialects.postgresql import ARRAY

from webapp.extensions import db


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id"))
    role_id = db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)
    update_datetime = db.Column(
        type_=db.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=naive_utcnow,
    )


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())

    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)

    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    create_datetime = db.Column(
        type_=db.DateTime, nullable=False, server_default=func.now()
    )
    update_datetime = db.Column(
        type_=db.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=naive_utcnow,
    )

    roles = relationship(
        "Role", secondary="roles_users", backref=backref("users", lazy="dynamic")
    )


class CaptureQuery(Query, SearchQueryMixin):
    pass


class Capture(db.Model):
    query_class = CaptureQuery
    __tablename__ = "captures"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta = db.Column(db.Text)
    title = db.Column(db.Text)
    link = db.Column(db.Text, index=True)
    markdown_content = db.Column(db.Text)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    search_vector = db.Column(TSVectorType("title", "markdown_content"))

    def get_meta(self):
        if self.meta is None:
            return {}

        d = json.loads(self.meta)
        return {
            "title": d.get("og:title", ""),
            "description": d.get("og:description", ""),
            "image": d.get("og:image", ""),
        }

    def __repr__(self):
        return "<Capture {}>".format(self.link)

class Summary_v2(db.Model):
    __tablename__ = "summary_v2"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary_title = db.Column(db.Text)
    summary = db.Column(db.Text)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    embedding = db.Column(ARRAY(db.Float))

db.configure_mappers()  # very important!

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
