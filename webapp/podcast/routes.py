import json

from flask import flash, redirect, render_template, url_for, request
from flask_security import current_user, auth_required

from webapp import db
from webapp.podcast import bp


def render(html, *args, **kwargs):
    return render_template(f"podcast/{html}", *args, **kwargs)


@bp.route("/new", methods=["GET"])
@auth_required()
def new():
    return render("new.html")


@bp.route("/", methods=["GET", "POST"])
@auth_required()
def index():
    return render("index.html")


@bp.route("/<int:id>", methods=["GET", "DELETE"])
@auth_required()
def show(id):
    return render("show.html")
