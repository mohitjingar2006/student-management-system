import json

from utils import require_non_empty

from database import (
    load_teachers_from_database,
    load_teacher_by_id,
    count_teachers,
    max_id,
    update_teacher_grades_db,
    update_teacher_subject_db,
    save_teacher,
    delete_teacher,
)

from models.teacher_model import Teacher

from constants import VALID_SUBJECTS


# Helper Functions

def teacher_exist():
	count = count_teachers()
	if count == 0:
		print("No teacher exists.")
		print()
		return False
	return True


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


def get_valid_subject():
	while True:
		for key in VALID_SUBJECTS:
			print(f"{"'"+str(key)+"'" :<6}: {VALID_SUBJECTS[key]}")
		print()
		value = input("Enter your choice : ").strip()
		print()
		if value in VALID_SUBJECTS:
			return VALID_SUBJECTS[value]
		else :
			print("\nInvalid Input.\n")


def find_teacher_by_id(id):
	teacher = load_teacher_by_id(id)
	if teacher:
		id,name,password,subject,grades = teacher
		grades = json.loads(grades)
		current_teacher = Teacher(name,id,password,subject,grades)
		return current_teacher
	print("\nTeacher not found.\n")
	print()
	return None


# Core Business logic

## Create
def add_teacher():
	prompt = "Enter Name of the Teacher : "
	name = require_non_empty(prompt)
	password = password_generator()
	print( "Enter subject of teacher : ")
	subject = get_valid_subject()
	prompt = "Enter Grades separated by commas : "
	grades = require_non_empty(prompt)
	grades = [grade.strip() for grade in grades.split(",")]
	ID = teacher_id_generator()
	teacher = Teacher(name,ID,password,subject,grades)

	save_teacher(teacher)
	print()
	print("Teacher added.")
	print(teacher)
	print()

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


def search_teacher_by_id():
	if not(teacher_exist()):
		return
	prompt = "Enter Teacher ID : "
	id = require_non_empty(prompt)
	teacher = find_teacher_by_id(id)
	if teacher:
		print(teacher)
		print()
		return

## Update

def update_subject(teacher):
	print()
	print( "Enter subject to update : ")
	subject = get_valid_subject()
	teacher.update_subject(subject)
	update_teacher_subject_db(subject,teacher.id)
	print()
	print("Teacher details updated.")
	print(teacher)
	print()


def update_grades(teacher):
	print()
	prompt = "Enter Grades separated by commas."
	print()
	grades = require_non_empty(prompt)
	grades = [grade.strip() for grade in grades.split(",")]
	teacher.update_grades(grades)
	grades = json.dumps(grades)
	update_teacher_grades_db(grades,teacher.id)
	print("Teacher details updated.")
	print(teacher)
	print()


def update_teacher_details():
	if not(teacher_exist()):
		return
	prompt = "Enter teacher ID : "
	id = require_non_empty(prompt)
	teacher = find_teacher_by_id(id)
	print("1. Update subject")
	print("2. Update grades")
	print()
	update_choice = input("Enter your choice : ")
	if update_choice == "1":
		update_subject(teacher)
	elif update_choice == "2":
		update_grades(teacher)
	else:
		print()
		print("Invalid Input.")
		print()


## Delete
def remove_teacher():
	if teacher_exist():
		prompt = "Enter teacher ID : "
		id = require_non_empty(prompt)
		teacher = find_teacher_by_id(id)
		if teacher:
			value = input(f"Are you sure you want to remove {teacher.name}?  (y/n)  ").lower()
			print()
			if value == "y":
				delete_teacher(id)
				print("Teacher removed.")
				print(teacher)
				print()
			elif value == "n":
				print("Operation Cancelled.")
				print()
			else:
				print("Invalid Input.")
				print()


## Display
def view_all_teachers():
	teachers = load_teachers()
	if not teachers:
		print("\nNo teacher exists.\n")
		return
	print("----------------------------------------------------------------------------------------------------------")
	print(f"{'S.no.' : <8}{'ID' : ^8}{'Name' : <20}{'Subject' : <15}Grades")
	print("----------------------------------------------------------------------------------------------------------")
	for i,teacher in enumerate(teachers,start = 1):
		print(f"{(str(i)+'.'): <8}{teacher.id :^8}{teacher.name :<20}{teacher.subject:<15}{", ".join(teacher.grades)}")
