VALID_GRADES = ["1st Yr.","2nd Yr.","3rd Yr.","4th Yr."]
VALID_BRANCHES = [
	"Electrical",
	"Mechanical",
	"CSE",
	"AI/DS",
	"Chemical",
	"Materials",
	"Bioengineering",
	"ES",
	"Optics",
	"Aeronautics",
	"Mathematics",
	"Chemistry",
	"Physics"
]


from utils import require_non_empty
from database import load_students_from_database,save_student,load_student_by_roll_num,count_students_by_grade,update_student_branch_db,update_student_grade_db,delete_student,count_students,max_roll_num_grade


class Student:
	def __init__(self,name,roll_num,grade,branch):
		self.name = name
		self.roll_number = roll_num
		self.grade = grade
		self.branch = branch
	def __str__(self):
		return (
			f"{'Name' :<12}: {self.name}\n"
			f"{'Roll Number' :<12}: {self.roll_number}\n"
			f"{'Grade' :<12}: {self.grade}\n"
			f"{'Branch' :<12}: {self.branch}\n"
			)
	def update_branch(self,branch):
		self.branch = branch
	def update_grade(self,grade):
		self.grade = grade
	def to_file_format(self):
		return [self.name,self.roll_number,self.grade,self.branch]



def load_students():
	students = []
	rows = load_students_from_database()
	for row in rows:
		roll_num,name,branch,grade = row
		student = Student(name,roll_num,grade,branch)
		students.append(student)
	return students



def students_exist():
	count = count_students()
	if count == 0:
		print("\nNo student exists.\n")
		return False
	return True
	students = load_students()


def input_valid_grade():
	grade = input("Enter Student Grade : ").strip()
	while grade not in VALID_GRADES:
		print("Invalid Input.")
		grade = input("Enter Student Grade : ").strip()
	return grade


def get_valid_branch():
	print("\nAvailable Branches :\n")
	for i, branch in enumerate(VALID_BRANCHES, start=1):
		print(f"{(str(i)+'.'):<5} {branch}")
	while True:
		prompt = "Enter student choice : "
		branch_choice = require_non_empty(prompt)
		print()
		if not branch_choice.isdigit():
			print("\nInvalid Input.\n")
			continue
		branch_choice = int(branch_choice)
		if 1 <= branch_choice <= len(VALID_BRANCHES):
			return VALID_BRANCHES[branch_choice - 1]
		else :
			print("\nInvalid Input.\n")



def roll_num_generator(grade):
	grade_prefix = {
		"1st Yr." : "1",
		"2nd Yr." : "2",
		"3rd Yr." : "3",
		"4th Yr." : "4"
	}

	last_roll = max_roll_num_grade(grade)
	if last_roll is None:
		return f"{grade_prefix[grade]}01"
	last_roll = int(last_roll)
	new_roll = str(last_roll + 1)
	return new_roll


def add_student():
	prompt = "Enter Student Name : "
	name = require_non_empty(prompt)

	#checking for valid grade.
	grade = input_valid_grade()

	#giving option for branches
	branch = get_valid_branch()

	roll_num = roll_num_generator(grade)

	student = Student(name,roll_num,grade,branch)

	save_student(student)
	print("\nStudent Added.")
	print(student)
	print()


def find_student_by_roll(roll_num):
	student = load_student_by_roll_num(roll_num)
	if student:
		roll_num,name,branch,grade = student
		current_student = Student(name,roll_num,grade,branch)
		return current_student
	return None


def search_student():
	exist = students_exist()
	if not exist:
		return
	prompt = "Enter Student Roll Number : "
	roll_num = require_non_empty(prompt)
	print("\n")
	current_student = find_student_by_roll(roll_num)
	if current_student:
		print(current_student)
	else:
		print("Student Not Found.\n")


def view_all_students():
	students = load_students()
	if not students:
		print("No student exists.")
		return
	print("----------------------------------------------------------------------------------------------------------")
	print(f"{'S.no.' : <8}{'Name' : <25}{'Roll Number' : <15}{'Grade' : <10}Branch")
	print("----------------------------------------------------------------------------------------------------------")


	for i,data in enumerate(students,start = 1):

		print(f"{str(i)+'.' :<8}{data.name :<25}{data.roll_number : ^15}{data.grade : <10}{data.branch}")

	print("\n")
	print(f"Total students : {count_students()}\n")
	print()

def update_student_branch():
	prompt = "Enter Student Roll Number : "
	roll_num = require_non_empty(prompt)
	print("\n")
	student = find_student_by_roll(roll_num)
	if student:
		branch = get_valid_branch()
		student.update_branch(branch)
		update_student_branch_db(branch,roll_num)
		#later will keep branch change optioon only for students coming to 2nd yr. means for starting of 2nd yr. and will make separate classes for respective yrs.
		print("Student details updated.")
		print()
		print(student)
	else:
		print("\nStudent Not Found.\n")

def update_student_grade():
	prompt = "Enter Student Roll Number : "
	roll_num = require_non_empty(prompt)
	print("\n")
	student = find_student_by_roll(roll_num)
	if student:
		#checking for valid grades.
		grade = input_valid_grade()
		student.update_grade(grade)
		update_student_grade_db(grade,roll_num)
		print()
		print("\nStudent details updated.\n")
		print(student)
	else:
		print("\nStudent Not Found.\n")


def update_student_details():
	exist = students_exist()
	if not exist:
		return
	while True:
		print("Menu : \n")
		print("1. Update Branch")
		print("2. Update Grade")
		print("3. Exit")
		print("\n")
		choice = input("Enter your choice : ").strip()
		print("\n")
		if choice == "1":
			update_student_branch()
		elif choice == "2":
			update_student_grade()
		elif choice == "3":
			print("\nExiting...\n")
			return
		else:
			print("\nInvalid Choice.\n")


def remove_student():
	exist = students_exist()
	if not exist:
		return
	prompt = "Enter Student Roll Number : "
	roll_num = require_non_empty(prompt)
	print()
	student = find_student_by_roll(roll_num)
	if student:
		user_input = input(f"Are you sure you want to remove {student.name} (y/n) : ").strip().lower()
		if user_input == "y":
			delete_student(roll_num)
			print("\nStudent removed.\n")
			print(student)
		elif user_input == "n":
			print("\nOperation Cancelled\n")
		else :
			print("\nInvalid Input\n")
	else:
		print("\nStudent Not Found\n")
