from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    abort
)

from database import (
	setup_admin,
	load_admin
)
from models.admin_model import Admin

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix = "/admin"
)


setup_admin()
# Unpacking load_admin row
try:
	admin_id, admin_name, admin_password = load_admin()
	admin = Admin(admin_id, admin_name, admin_password)
except ValueError:
	admin = None


@admin_bp.route("/" ,methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        name = request.form.get("admin-name")
        password = request.form.get("admin-password")
        if admin:
            if admin.check_name(name) and admin.check_password(password):
                session["admin_name"] = name
                return redirect(url_for("admin.admin_menu"))
            else:
                return render_template(
                    "admin/admin.html",
                    message = "Incorrect username or password."
                    )
        abort(500, description="Database integrity error encountered.")
    return render_template("admin/admin.html")


@admin_bp.route("/admin-menu")
def admin_menu():
    return render_template("admin/admin-menu.html")


@admin_bp.route("/logout")
def admin_logout():
    if session.get("admin_name"):
        session.pop("admin_name")
    return render_template(
        "admin/admin.html",
        message = "Logged out!"
        )