import json

from flask import flash, redirect, render_template, url_for, request
from flask_security import auth_required, current_user
import requests
from readabilipy import simple_json_from_html_string
import html2text
from bs4 import BeautifulSoup
from sqlalchemy.sql import text

from webapp import db
from webapp.capture import bp
from webapp.capture.forms import CaptureForm
from webapp.models import Capture
from webapp.capture.utils import extract_opengraph_metadata
from webapp.capture.actors import cop


@bp.route("/new", methods=["GET"])
@auth_required()
def captures_new():
    form = CaptureForm()
    return render_template("capture/new.html", form=form)


@bp.route("/", methods=["GET", "POST"])
@auth_required()
def captures():
    form = CaptureForm()
    if form.validate_on_submit():
        res = requests.get(form.link.data)
        res.encoding = "utf-8"
        if res.status_code != 200:
            flash(f"Failed to capture link: {res.status_code}")
            return redirect(url_for("capture.captures_new"))
        title = BeautifulSoup(res.text, "html.parser").title.string
        meta = json.dumps(extract_opengraph_metadata(res.text), ensure_ascii=False)
        article = simple_json_from_html_string(res.text, use_readability=True)
        if title is None:
            title = article["title"]
        markdown_content = html2text.html2text(article["content"])
        flash("Link captured!")
        capture = Capture(
            link=form.link.data,
            title=title,
            user_id=current_user.id,
            meta=meta,
            markdown_content=markdown_content,
        )
        db.session.add(capture)
        db.session.commit()
        return redirect(url_for("capture.captures_new"))
    captures = (
        Capture.query.filter_by(user_id=current_user.id)
        .order_by(Capture.created_at.desc())
        .all()
    )
    return render_template("capture/index.html", captures=captures)


@bp.route("/<id>", methods=["GET", "DELETE"])
@auth_required()
def captures_show(id):
    if request.method == "DELETE":
        capture = Capture.query.get(id)
        db.session.delete(capture)
        db.session.commit()
        return "OK", 200
    # cop.send()
    capture = Capture.query.get(id)
    clean_content = capture.markdown_content.replace("`", "\`").replace("${", "\${")
    return render_template(
        "capture/show.html", capture=capture, clean_content=clean_content
    )


@bp.route("/search", methods=["GET"])
@auth_required()
def captures_search():
    q = request.args.get("q")
    print(q)
    captures = Capture.query.search(q).all()
    ids = ",".join([f"'{c.id}'" for c in captures])
    snips = db.session.execute(
        text(
            f"SELECT id, ts_headline(markdown_content, parse_websearch('{q}'), 'MaxFragments=1, MinWords=5, MaxWords=20, FragmentDelimiter=XXX.....XXX') as text FROM {Capture.__tablename__} WHERE id in ({ids})"
        )
    )
    snip_texts = {s.id: s.text.split("XXX.....XXX") for s in snips}
    print(captures)
    return render_template(
        "capture/search_index.html", captures=captures, q=q, snip_texts=snip_texts
    )


@bp.route("/extension", methods=["POST"])
@auth_required()
def extension():
    data = request.json
    print(request.headers)
    print(data)
    if data["isReadable"]:
        markdown_content = html2text.html2text(data["html"])
        title = data["title"]
        meta = json.dumps({})
        capture = Capture(
            link=data["url"],
            title=title,
            user_id=current_user.id,
            meta=meta,
            markdown_content=markdown_content,
        )
        db.session.add(capture)
        db.session.commit()
    return "OK", 200
