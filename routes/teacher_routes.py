import json
from flask import (
    Blueprint,
    session,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    save_teacher,
    delete_teacher,
    update_teacher_grades_db,
    update_teacher_subject_db
)
from models.teacher_model import Teacher
from services.teacher_service import (
    load_teachers,
    teacher_id_generator,
    password_generator,
    find_teacher_by_id
)
from utils.decorators import (
    admin_required,
    teacher_required
)

# blueprint
teachers_bp = Blueprint(
    "teachers",
    __name__,
    url_prefix="/teacher"
)

## Admin part

# Helper function

@teachers_bp.route("/view-teacher/<teacher_id>")
@admin_required
def view_teacher(teacher_id : str) -> Response:
    teacher = find_teacher_by_id(teacher_id)
    if teacher:
        return render_template(
            "teachers/view-teacher.html",
            teacher = Teacher(
                name=teacher["name"],
                id=teacher["ID"],
                password=teacher["password"],
                subject=teacher["subject"],
                grades=json.loads(teacher["grades"])
            )
        )
    flash("Teacher not found","error")
    return redirect(url_for("teachers.teacher_admin_menu"))


# Core Business logic

@teachers_bp.route("/admin-menu")
@admin_required
def teachers_admin_menu() -> Response:
    return render_template("teachers/admin-menu.html")


# View
@teachers_bp.route("/view")
@admin_required
def view_all_teachers():
    teachers = load_teachers()
    if teachers:
        return render_template(
            "teachers/view-teachers.html",
            teachers = teachers
        )
    flash("No teachers exist!","error")
    return redirect(url_for("teachers.teachers_admin_menu"))


# Add

@teachers_bp.route("/add-teacher", methods=["GET","POST"])
@admin_required
def add_teacher() -> Response:
    if request.method == "POST":
        name = request.form.get("teacher-name")
        subject = request.form.get("teacher-subject")
        password = password_generator()
        grades = request.form.getlist("grades")
        teacher_id = teacher_id_generator()
        new_teacher = Teacher(name,teacher_id,password,subject,grades)
        save_teacher(new_teacher)
        flash("Teacher added successfully...","success")
        return redirect(
            url_for(
                "teachers.view_teacher",
                teacher_id = teacher_id
            )
        )
    return render_template("teachers/add-teachers.html")


# Read
@teachers_bp.route("/search-teacher",methods=["GET","POST"])
@admin_required
def search_teacher() -> Response:
    if request.method == "POST":
        teacher_id = request.form.get("id")
        return redirect(
            url_for(
                "teachers.view_teacher",
                teacher_id = teacher_id
                )
            )
    return render_template("teachers/search-teacher.html")


# Update

@teachers_bp.route("/update-teacher-details")
@admin_required
def update_teacher_details() -> Response:
    return render_template("teachers/update-teacher-details.html")


@teachers_bp.route("/update-subject",methods=["GET","POST"])
@admin_required
def update_teacher_subject() -> Response:
    if request.method == "POST":
        teacher_id = request.form.get("id")
        subject = request.form.get("teacher-subject")
        teacher = find_teacher_by_id(teacher_id)
        if teacher:
            update_teacher_subject_db(subject,teacher_id)
            flash("Teacher subject changed successfully.","success")
            return redirect(
                url_for(
                    "teachers.view_teacher",
                    teacher_id = teacher_id
                    )
            )
        else:
            flash("Teacher not found!","error")
            return redirect(url_for("teachers.update_teacher_subject"))
    return render_template("teachers/update-subject.html")


@teachers_bp.route("/update-grades",methods=["GET","POST"])
@admin_required
def update_teacher_grades() -> Response:
    if request.method == "POST":
        teacher_id = request.form.get("id")
        grades = request.form.getlist("grades")
        grades = json.dumps(grades)
        teacher = find_teacher_by_id(teacher_id)
        if teacher:
            update_teacher_grades_db(grades,teacher_id)
            flash("Teachers grades changed successfully.","success")
            return redirect(
                url_for(
                    "teachers.view_teacher",
                    teacher_id = teacher_id
                    )
            )
        else:
            flash("Teacher not found!","error")
            return redirect(url_for("teachers.update_teacher_grades"))
    return render_template("teachers/update-grades.html")


# Delete

@teachers_bp.route("/remove-teacher",methods=["GET","POST"])
@admin_required
def remove_teacher() -> Response:
    if request.method == "POST":
        teacher_id = request.form.get("id")
        teacher = find_teacher_by_id(teacher_id)
        if teacher:
            return render_template(
                "teachers/confirm-delete.html",
                teacher_id = teacher_id
            )
        else:
            flash("Teacher not found!","error")
            return redirect(url_for("teachers.remove_teacher"))
    return render_template("teachers/remove-teacher.html")


@teachers_bp.route("/delete/<teacher_id>",methods=["POST"])
@admin_required
def confirm_delete(teacher_id : str) -> Response:
    button_clicked = request.form.get("action")
    if button_clicked == "submit":
        delete_teacher(teacher_id)
        flash("Teacher deleted successfully.","success")
        return redirect(url_for("teachers.remove_teacher"))
    flash("Operation Cancelled!","cancel")
    return redirect(url_for("teachers.remove_teacher"))


## Teacher part

@teachers_bp.route("/" ,methods=["GET","POST"])
def teacher_login() -> Response:
    if request.method == "POST":
        teacher_id = request.form.get("teacher-id")
        password = request.form.get("teacher-password")
        teacher = find_teacher_by_id(teacher_id)
        if teacher and teacher.check_password(password):
            session["teacher_name"] = teacher.name
            return redirect(url_for("teachers.teacher_menu"))
        else:
            flash("Incorrect username or password.","error")
            return redirect(url_for("teachers.teacher_login"))
    return render_template("teachers/teacher.html")


@teachers_bp.route("/teacher-menu")
@teacher_required
def teacher_menu() -> Response:
    return render_template("teachers/teacher-menu.html")


@teachers_bp.route("/logout")
@teacher_required
def teacher_logout() -> Response:
    if "teacher_name" in session:
        session.pop("teacher_name")
        flash("Logged out!","success")
    return redirect(url_for("teachers.teacher_login"))