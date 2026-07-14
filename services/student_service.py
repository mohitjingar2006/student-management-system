# imports

from models.student import Student

from database import (
    load_students_from_database,
	load_student_by_roll_number,
	max_roll_number_grade,
)

# Helper Functions

def roll_number_generator(grade : str) -> str:
	grade_prefix = {
		"1st Year" : "1",
		"2nd Year" : "2",
		"3rd Year" : "3",
		"4th Year" : "4"
	}
	last_roll = max_roll_number_grade(grade)
	if last_roll is None:
		return f"{grade_prefix[grade]}01"
	last_roll = int(last_roll)
	new_roll = str(last_roll + 1)
	return new_roll


def find_student_by_roll_number(roll_number : str) -> Student | None:
	student = load_student_by_roll_number(roll_number)
	if student:
		return Student(
			name=student["name"],
			roll_number=student["roll_number"],
			grade=student["grade"],
			branch=student["branch"]
		)
	return None


# Core Business logic

# Read

def load_students() -> list[Student]:
	students = []
	student_rows = load_students_from_database()
	for row in student_rows:
		student = Student(
			name=row["name"],
			roll_number=row["roll_number"],
			grade=row["grade"],
			branch=row["branch"]
			)
		students.append(student)
	return students

