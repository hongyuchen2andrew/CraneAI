from flask import flash, redirect, render_template, url_for
from flask_security import current_user, auth_required

from webapp.main import bp


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("capture.captures_new"))
    return redirect(url_for("security.login"))


@bp.route("/extension-login")
@auth_required()
def extension_login():
    extension_app_id = "jcpdiieajepeecbpcfkheoffpegffdke"
    return redirect(
        f"https://{extension_app_id}.chromiumapp.org?token={current_user.get_auth_token()}"
    )
