import json
from flask import (
    Blueprint,
    render_template,
    request,redirect,
    url_for,
    flash
)

from database import save_teacher
from models.teacher_model import Teacher
from services.teacher_service import (
    load_teachers,
    teacher_id_generator,
    password_generator,
    find_teacher_by_id,
    update_teacher_grades_db,
    update_teacher_subject_db
)

teachers_bp = Blueprint(
    "teachers",
    __name__,
    url_prefix="/teacher"
)

## Admin part

# Helper function

@teachers_bp.route("/view-teacher/<id>")
def view_teacher(id):
    teacher = find_teacher_by_id(id)
    if teacher:
        id, name, password, subject, grades = teacher
        grades = json.loads(grades)
        teacher = Teacher(name,id,password,subject,grades)
        return render_template(
            "teachers/view-teacher.html",
            teacher = teacher
        )
    flash("Teacher not found","error")
    return redirect(url_for("teachers.teacher_admin_menu"))


# Core Business logic

@teachers_bp.route("/admin-menu")
def teachers_admin_menu():
    return render_template("teachers/admin-menu.html")


# View
@teachers_bp.route("/view")
def view_all_teachers():
    teachers = load_teachers()
    if teachers:
        return render_template(
            "teachers/view-teachers.html",
            teachers = teachers
        )
    flash("No teachers exist!","error")


# Add

@teachers_bp.route("/add-teacher", methods=["GET","POST"])
def add_teacher():
    if request.method == "POST":
        name = request.form.get("teacher-name")
        subject = request.form.get("teacher-subject")
        password = password_generator()
        grades = request.form.getlist("grades")
        id = teacher_id_generator()
        new_teacher = Teacher(name,id,password,subject,grades)
        save_teacher(new_teacher)
        flash("Teacher added successfully...","success")
       return redirect(
        url_for("teachers.view_teacher"),
        roll_num = roll_num
        )
    return render_template("teachers/add-teachers.html")


# Read
@teachers_bp.route("/search-teacher",methods=["GET","POST"])
def search_teacher():
    if request.method == "POST":
        id = request.form.get("id")
        return redirect(
            url_for("teachers.view_teacher"),
            id = id
            )
    return render_template("teachers/search-teacher.html")


# Update

@teachers_bp.route("/update-teacher-details")
def update_teacher_details():
    return render_template("update-teacher-details.html")


@students_bp.route("/update-branch",methods=["GET","POST"])
def update_teacher_subject():
    if request.method == "POST":
        id = request.form.get("id")
        subject = request.form.get("teacher-subject")
        teacher = find_teacher_by_id(id)
        if teacher:
            update_teacher_subject_db(subject,id)
            flash("Teacher subject changed successfully.","success")
            return redirect(
                url_for("teachers.view_teacher"),
                id = id
            )
        flash("Teacher not found!","error")
    return render_template("teachers/update-subject.html")


@students_bp.route("/update-grades",methods=["GET","POST"])
def update_teacher_grades():
    if request.method == "POST":
        id = request.form.get("id")
        grades = request.form.getlist("grades")
        grades = json.dumps(grades)
        teacher = find_teacher_by_id(id)
        if teacher:
            update_teacher_grades_db(grades,id)
            flash("Teachers grades changed successfully.","success")
            return redirect(
                url_for("teachers.view_teacher"),
                id = id
            )
        flash("Teacher not found!","error")
    return render_template("teachers/update-grades.html")


# Delete

@teachers_bp.route("/remove-teacher",methods=["GET","POST"])
def remove_teacher():
    if request.method == "POST":
        id = request.form.get("id")
        teacher = find_teacher_by_id(id)
        if teacher:
            return render_template(
                "teachers/confirm-delete.html",
                id = id
            )
        flash("Teacher not found!","error")
    return render_template("teachers/remove-teacher.html")


@teachers_bp.route("/delete/<id>",methods=["POST"])
def confirm_delete(id):
    button_clicked = request.form.get("action")
    if button_clicked == "submit":
        delete_teacher(id)
        flash("Teacher deleted successfully.","success")
        return redirect(url_for("teachers.remove_teacher"))
    flash("Operation Cancelled!","error")
    return redirect(url_for("teachers.remove_teacher"))


## Teacher part

@teachers_bp.route("/" ,methods=["GET","POST"])
def teacher_login():
    if request.method == "POST":
        id = request.form.get("teacher-id")
        password = request.form.get("teacher-password")
        teacher = find_teacher_by_id(id)
        if teacher.check_id(id) and teacher.check_password(password):
            session["teacher_name"] = teacher.name
            return redirect(url_for("teachers.teacher_menu"))
        else:
            return render_template(
                "teacher/teacher.html",
                message = "Incorrect username or password."
                )
    return render_template("teacher/teacher.html")


@teachers_bp.route("/teacher-menu")
def teacher_menu():
    return render_template("students/teacher-menu.html")


@teachers_bp.route("/logout")
def teacher_logout():
    if session.get("teacher_name"):
        session.pop("teacher_name")
    return render_template(
        "teachers/teacher.html",
        message = "Logged out!"
        )

