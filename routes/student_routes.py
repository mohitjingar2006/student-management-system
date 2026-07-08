# imports

from flask import (
    Blueprint,
    redirect,
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
    roll_num_generator,
    find_student_by_roll
)

# blueprint
students_bp = Blueprint(
    "students",
    __name__,
    url_prefix = "/students"
)

# routes

## Admin Part

# Helper function
@students_bp.route("/view-student/<roll_num>")
def view_student(roll_num):
    student = find_student_by_roll(roll_num)
    if student:
        return render_template(
            "view-student.html",
            student = student
        )
    flash("Student not found","error")
    return redirect(url_for("students.student_admin_menu"))

# Core Business logic

@students_bp.route("/admin-menu")
def student_admin_menu():
    return render_template("students/admin-menu.html")

# View
@students_bp.route("/view")
def view_all_students():
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
def add_student():
    if request.method == "POST":
        name = request.form.get("student-name")
        grade = request.form.get("grade")
        branch = request.form.get("student-branch")
        roll_num = roll_num_generator(grade)
        new_student = Student(name,roll_num,grade,branch)
        save_student(new_student)
        flash("Student added successfully...","success")
        return redirect(
            url_for(
                "students.view_student",
                roll_num = roll_num
            )
        )
    return render_template("students/add-students.html")

# Read
@students_bp.route("/search-student",methods=["GET","POST"])
def search_student():
    if request.method == "POST":
        roll_num = request.form.get("roll-number")
        return redirect(
            url_for(
                "students.view_student",
                roll_num = roll_num
            )
        )
    return render_template("students/search-student.html")

# Update

@students_bp.route("/update-student-details")
def update_student_details():
    return render_template("update-student-details.html")

@students_bp.route("/update-branch",methods=["GET","POST"])
def update_student_branch():
    if request.method == "POST":
        roll_num = request.form.get("roll-number")
        branch = request.form.get("student-branch")
        student = find_student_by_roll(roll_num)
        if student:
            update_student_branch_db(branch,roll_num)
            flash("Student Branch changed successfully.","success")
            return redirect(
                url_for(
                  "students.view_student",
                  roll_num = roll_num
                )
            )
        flash("Student not found!","error")
    return render_template("students/update-branch.html")


@students_bp.route("/update-grade",methods=["GET","POST"])
def update_student_grade():
    if request.method == "POST":
        roll_num = request.form.get("roll-number")
        grade = request.form.get("grade")
        student = find_student_by_roll(roll_num)
        if student:
            update_student_grade_db(grade,roll_num)
            flash("Student Grade changed successfully.","success")
            return redirect(
                url_for("students.view_student",
                roll_num = roll_num
                )
            )
        flash("Student not found!","error")
    return render_template("students/update-grade.html")

# Delete

@students_bp.route("/remove-student",methods=["GET","POST"])
def remove_student():
    if request.method == "POST":
        roll_num = request.form.get("roll-number")
        student = find_student_by_roll(roll_num)
        if student:
            return render_template(
                "confirm-delete.html",
                roll_num = roll_num
            )
        flash("Student not found!","error")
    return render_template("students/remove-student.html")
    
@students_bp.route("/delete/<roll_num>",methods=["POST"])
def confirm_delete(roll_num):
    button_clicked = request.form.get("action")
    if button_clicked == "submit":    
        delete_student(roll_num)
        flash("Student deleted successfully.","success")
    flash("Operation Cancelled!","error")
    return redirect(url_for("students.remove_student"))