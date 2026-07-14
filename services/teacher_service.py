# imports

import json

from database import (
    load_teachers_from_database,
    load_teacher_by_id,
    get_last_teacher_id,
)

from models.teacher_model import Teacher

# Helper Functions


def teacher_id_generator() -> str:
	last_id = get_last_teacher_id()
	if last_id is None:
		return "T01"
	last_number = int(last_id[1:])
	new_number = last_number + 1
	return f"T{new_number:02}"


def password_generator() -> str:
	# College name = college
	college_abbreviation = "xyz"
	id = teacher_id_generator()[1:]
	password = f"{'PASS'}{id}{college_abbreviation}"
	return password


def find_teacher_by_id(teacher_id : str) -> Teacher | None:
	teacher = load_teacher_by_id(teacher_id)
	if teacher:
		return Teacher(
			name=teacher["name"],
			id=teacher["ID"],
			password=teacher["password"],
			subject=teacher["subject"],
			grades=json.loads(teacher["grades"])
		)
	return None


# Core Business logic

## Read

def load_teachers() -> list[Teacher]:
	teachers = []
	teacher_rows = load_teachers_from_database()
	for row in teacher_rows:
		teacher = Teacher(
			name=row["name"],
			id=row["ID"],
			password=row["password"],
			subject=row["subject"],
			grades=json.loads(row["grades"])
			)
		teachers.append(teacher)
	return teachers
