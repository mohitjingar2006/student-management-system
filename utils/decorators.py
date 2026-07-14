from functools import wraps
from flask import (
    session,
    flash,
    redirect,
    url_for
)

def admin_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "admin_name" not in session:
            flash("Admin login required!","error")
            return redirect(url_for("admin.admin_login"))
        return func(*args,**kwargs)
    return wrapper


def teacher_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "teacher_name" not in session:
            flash("Teacher login required!","error")
            return redirect(url_for("teachers.teacher_login"))
        return func(*args,**kwargs)
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "admin_name" not in session and "teacher_name" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper