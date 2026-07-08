# imports

from models.student import Student

from database import (
    load_students_from_database,
	load_student_by_roll_num,
	max_roll_num_grade,
)

# Helper Functions

def roll_num_generator(grade):
	grade_prefix = {
		"1st Year" : "1",
		"2nd Year" : "2",
		"3rd Year" : "3",
		"4th Year" : "4"
	}

	last_roll = max_roll_num_grade(grade)
	if last_roll is None:
		return f"{grade_prefix[grade]}01"
	last_roll = int(last_roll)
	new_roll = str(last_roll + 1)
	return new_roll


def find_student_by_roll(roll_num):
	student = load_student_by_roll_num(roll_num)
	if student:
		roll_num,name,grade,branch = student
		current_student = Student(name,roll_num,grade,branch)
		return current_student
	return None

# Core Business logic

# Read

def load_students():
	students = []
	rows = load_students_from_database()
	for row in rows:
		roll_num, name, grade, branch = row
		student = Student(name,roll_num,grade,branch)
		students.append(student)
	return students

