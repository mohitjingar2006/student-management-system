import json
VALID_GRADES = {
		"1" : "1st Yr.",
		"2" : "2nd Yr.",
		"3" : "3rd Yr.",
		"4" : "4th Yr."
		}
VALID_SUBJECTS = {
	"1" : "Electrical",
	"2" : "Mechanical",
	"3" : "CSE",
	"4" : "AI/DS",
	"5" : "Chemical",
	"6" : "Materials",
	"7" : "Bioengineering",
	"8" : "ES",
	"9" : "Optics",
	"10": "Aeronautics",
	"11": "Mathematics",
	"12": "Chemistry",
	"13": "Physics"
}



from student import view_all_students,search_student
from utils import require_non_empty
from mask_input import get_masked_input
from database import load_teachers_from_database, save_teacher, delete_teacher ,count_teachers, load_teacher_by_id, max_id, update_teacher_grades_db, update_teacher_subject_db


class Teacher:
	def __init__(self,name,ID,password,subject,grades):
		self.name = name
		self.id = ID
		self.password = password
		self.subject = subject
		self.grades = grades
	def check_password(self,password):
		return (self.password == password)
	def check_name(self,name):
		return self.name == name
	def check_id(self,id):
		return self.id == id
	def update_grades(self,grades):
			self.grades = grades
	def update_subject(self,subject):
			self.subject = subject
	def __str__(self):
		return (
			f"{'Name' :<12}: {self.name}\n"
			f"{'ID' :<12}: {self.id}\n"
			f"{'Subject' :<12}: {self.subject}\n"
			f"{'Grades' :<12}: {self.grades}\n"
			)
	def to_file_format(self):
		return [
			self.name,
			self.id,
			self.password,
			self.subject,
			",".join(self.grades)
			]


def load_teachers():
	teachers = []
	rows = load_teachers_from_database()
	for row in rows:
		id,name,password,subject,grades = row
		grades = json.loads(grades)
		teacher = Teacher(name,id,password,subject,grades)
		teachers.append(teacher)
	return teachers


def teacher_exist():
	count = count_teachers()
	if count == 0:
		print("No teacher exists.")
		print()
		return False
	return True


def find_teacher_by_id(id):
	teacher = load_teacher_by_id(id)
	if teacher:
		id,name,password,subject,grades = teacher
		current_teacher = Teacher(name,id,password,subject,grades)
		return current_teacher
	print("\nTeacher not found.\n")
	print()
	return None



def teacher_menu():
	if not(teacher_exist()):
		return
	while True:
		print("Teacher menu :")
		print("\n\n")
		print("1. Login")
		print("2. Back to main menu")
		print("\n\n")
		choice = input("Enter your choice : ")
		print()
		if choice == "1":
			prompt = "Please Enter Your ID : "
			id = require_non_empty(prompt)
			exist = False
			teacher = find_teacher_by_id(id)
			if teacher:
				print("Enter your password : ",end = '',flush = True)
				password = get_masked_input()
				if teacher.check_password(password):
					print()
					print("Login Successful.")
					print()
					print(f"Welcome {teacher.name}")
					while True:
						print("\n\nMenu :\n\n")
						print("1. View All Students")
						print("2. Search Student")
						print("3. Logout")
						print()

						teacher_choice = input("Enter your choice : ").strip()
						print()
						if teacher_choice == "1":
							view_all_students()
						elif teacher_choice == "2":
							search_student()
						elif teacher_choice == "3":
							print()
							print("Logging out...")
							print()
							break
				else:
					print("\nInvalid Password\n")
		elif choice == "2":
			print("Back to main menu...")
			print()
			break
		else:
			print("Invalid Input.")
			print()



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
