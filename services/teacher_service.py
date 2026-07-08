# imports

import json

from database import (
    load_teachers_from_database,
    load_teacher_by_id,
    max_id,
)

from models.teacher_model import Teacher

# Helper Functions


def teacher_id_generator():
	last_id = max_id()
	if last_id is None:
		return "T01"
	last_number = int(last_id[1:])
	new_number = last_number + 1
	return f"T{new_number:02}"


def password_generator():
	#College name = college
	college_abbreviation = "xyz"
	id = teacher_id_generator()[1:]
	password = f"{'PASS'}{id}{college_abbreviation}"
	return password


def find_teacher_by_id(id):
	teacher = load_teacher_by_id(id)
	if teacher:
		id,name,password,subject,grades = teacher
		grades = json.loads(grades)
		current_teacher = Teacher(name,id,password,subject,grades)
		return current_teacher
	return None


# Core Business logic

## Read

def load_teachers():
	teachers = []
	rows = load_teachers_from_database()
	for row in rows:
		id,name,password,subject,grades = row
		grades = json.loads(grades)
		teacher = Teacher(name,id,password,subject,grades)
		teachers.append(teacher)
	return teachers
