from flask import (
    Blueprint,
    session,
    flash,
    render_template,
    redirect,
    request,
    url_for,
    Response,
    abort
)

from utils.app_setup import get_admin
from utils.decorators import admin_required

# blueprint
admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix = "/admin"
)

@admin_bp.route("/" ,methods=["GET","POST"])
def admin_login() -> Response:
    admin = get_admin()
    if request.method == "POST":
        name = request.form.get("admin-name")
        password = request.form.get("admin-password")
        if admin is None:
            abort(500, description="Database integrity error encountered.")
        if admin.check_name(name) and admin.check_password(password):
            session["admin_name"] = name
            return redirect(url_for("admin.admin_menu"))
        else:
            flash("Incorrect username or password.","error")
            return redirect(url_for("admin.admin_login"))
    return render_template("admin/admin.html")


@admin_bp.route("/admin-menu")
@admin_required
def admin_menu() -> Response:
    return render_template("admin/admin-menu.html")


@admin_bp.route("/logout")
@admin_required
def admin_logout() -> Response:
    if "admin_name" in session:
        session.pop("admin_name")
        flash("Logged out!","success")
    return redirect(url_for("admin.admin_login"))