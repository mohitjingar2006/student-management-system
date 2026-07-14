# imports

from flask import (
    Blueprint,
    redirect,
    Response,
    render_template,
    url_for,
    flash,
    request
)

from database import (
    save_student,
    delete_student,
    update_student_branch_db,
    update_student_grade_db
)
from models.student import Student
from services.student_service import (
    load_students,
    roll_number_generator,
    find_student_by_roll_number
)
from utils.decorators import (
    admin_required,
    login_required
)

# blueprint

students_bp = Blueprint(
    "students",
    __name__,
    url_prefix = "/students"
)

## Routes

# Admin Part

# Helper function
@students_bp.route("/view-student/<roll_number>")
@login_required
def view_student(roll_number : str) -> Response:
    student = find_student_by_roll_number(roll_number)
    if student:
        return render_template(
            "students/view-student.html",
            student = student
        )
    flash("Student not found","error")
    return redirect(url_for("students.student_admin_menu"))


# Core Business logic

@students_bp.route("/admin-menu")
@admin_required
def student_admin_menu() -> Response:
    return render_template("students/admin-menu.html")


# View
@students_bp.route("/view")
@login_required
def view_all_students() -> Response:
    students = load_students()
    if students:
        return render_template(
            "students/view-students.html",
            students = students
        )
    flash("No student exists!","error")
    return redirect(url_for("students.student_admin_menu"))


# Add
@students_bp.route("/add-student", methods=["GET","POST"])
@admin_required
def add_student() -> Response:
    if request.method == "POST":
        name = request.form.get("student-name")
        grade = request.form.get("grade")
        branch = request.form.get("student-branch")
        roll_number = roll_number_generator(grade)
        new_student = Student(name,roll_number,grade,branch)
        save_student(new_student)
        flash("Student added successfully...","success")
        return redirect(
            url_for(
                "students.view_student",
                roll_number = roll_number
            )
        )
    return render_template("students/add-student.html")


# Read
@students_bp.route("/search-student",methods=["GET","POST"])
@login_required
def search_student() -> Response:
    if request.method == "POST":
        roll_number = request.form.get("roll-number")
        return redirect(
            url_for(
                "students.view_student",
                roll_number = roll_number
            )
        )
    return render_template("students/search-student.html")


# Update

@students_bp.route("/update-student-details")
@admin_required
def update_student_details() -> Response:
    return render_template("students/update-student-details.html")


@students_bp.route("/update-branch",methods=["GET","POST"])
@admin_required
def update_student_branch() -> Response:
    if request.method == "POST":
        roll_number = request.form.get("roll-number")
        branch = request.form.get("student-branch")
        student = find_student_by_roll_number(roll_number)
        if student:
            update_student_branch_db(branch,roll_number)
            flash("Student Branch changed successfully.","success")
            return redirect(
                url_for(
                  "students.view_student",
                  roll_number = roll_number
                )
            )
        else:
            flash("Student not found!","error")
            return redirect(url_for("students.update_student_branch"))
    return render_template("students/update-branch.html")


@students_bp.route("/update-grade",methods=["GET","POST"])
@admin_required
def update_student_grade() -> Response:
    if request.method == "POST":
        roll_number = request.form.get("roll-number")
        grade = request.form.get("grade")
        student = find_student_by_roll_number(roll_number)
        if student:
            update_student_grade_db(grade,roll_number)
            flash("Student Grade changed successfully.","success")
            return redirect(
                url_for("students.view_student",
                roll_number = roll_number
                )
            )
        else:
            flash("Student not found!","error")
            return redirect(url_for("students.update_student_grade"))
    return render_template("students/update-grade.html")


# Delete

@students_bp.route("/remove-student",methods=["GET","POST"])
@admin_required
def remove_student() -> Response:
    if request.method == "POST":
        roll_number = request.form.get("roll-number")
        student = find_student_by_roll_number(roll_number)
        if student:
            return redirect(
                url_for(
                    "students.confirm_delete",
                    roll_number = roll_number
                    )
            )
        else:
            flash("Student not found!","error")
            return redirect(url_for("students.remove_student"))
    return render_template("students/remove-student.html")
    

@students_bp.route("/delete/<roll_number>",methods=["GET","POST"])
@admin_required
def confirm_delete(roll_number : str) -> Response:
    student = find_student_by_roll_number(roll_number)
    if request.method == "POST":
        button_clicked = request.form.get("action")
        if button_clicked == "submit":    
            delete_student(roll_number)
            flash("Student deleted successfully.","success")
            return redirect(url_for("students.remove_student"))
        else:
            flash("Operation Cancelled!","cancel")
            return redirect(url_for("students.remove_student"))
    return render_template(
        "students/confirm-delete.html",
        student = student
        )
    