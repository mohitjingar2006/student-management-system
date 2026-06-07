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
    "Aeronautics"
]

import csv
import config
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


def save_all_students():
	with open("student.csv","w",newline = "") as file:
		writer = csv.writer(file)
		for student in config.students :
			writer.writerow(student.to_file_format())


def load_students():
	config.students.clear()
	try:
		with open("student.csv",newline = "") as file:
			reader = csv.reader(file)
			for row in reader:
				try:
					name,roll_number,grade,branch = row
					student = Student(name,roll_number,grade,branch)
					config.students.append(student)
				except ValueError:
					print("Invalid Student Data Format.")
		return config.students
	except FileNotFoundError:
		print("student.csv file not found.")
		return []

def students_exist():
	if not config.students :
		print("\nNo student exists.\n")
		return False
	return True


def avoid_duplicate_roll(roll_num):
	if not config.students :
		return False
	for current_student in config.students :
		if(current_student.roll_number == roll_num):
			return True
	return False


def input_valid_grade():
	grade = input("Enter Student Grade : ").strip()
	while grade not in VALID_GRADES:
		print("Invalid Grade.")
		grade = input("Enter Student Grade : ").strip()
	return grade


def get_valid_branch():
	print("\nAvailable Branches :\n")
	for i, branch in enumerate(VALID_BRANCHES, start=1):
		print(f"{(str(i)+'.'):<5} {branch}")
	while True:
		branch_choice = input("\nEnter choice : ").strip()
		print()
		if not branch_choice.isdigit():
			print("\nInvalid Input.\n")
			continue
		branch_choice = int(branch_choice)
		if 1 <= branch_choice <= len(VALID_BRANCHES):
			return VALID_BRANCHES[branch_choice - 1]
		else :
			print("\nInvalid Input.\n")


def count_students_by_grade(grade):
	count = 0
	for student in config.students :
		if(student.grade == grade):
			count += 1
	return count

def roll_num_generator(grade):
	grade_prefix = {
		"1st Yr." : "1",
		"2nd Yr." : "2",
		"3rd Yr." : "3",
		"4th Yr." : "4"
	}

	count = count_students_by_grade(grade)

	return f"{grade_prefix[grade]}{count+1:02}"


def add_student():
	name = input("Enter Student Name : ").strip()
	while name == "":
		name = input("Name cannot be empty : ").strip()

	#checking for valid grade.
	grade = input_valid_grade()

	#giving option for branches
	branch = get_valid_branch()

	#roll_number
	roll_num = roll_num_generator(grade)

	student = Student(name,roll_num,grade,branch)

	try:
		with open("student.csv","a",newline = "") as file:
			writer = csv.writer(file)
			writer.writerow(student.to_file_format())

		print("\nStudent Added.\n")
		config.students.append(student)
		print(student)
		print()
	except OSError as e:
		print(f"Unable to save student data: {e}")
		return


def find_student_by_roll(roll_num):
	for current_student in config.students:
		if(current_student.roll_number == roll_num):
			return current_student
	return None




def search_student():
	exist = students_exist()
	if not exist:
		return
	roll_num = input("Enter Student Roll number : ").strip()
	print("\n")
	current_student = find_student_by_roll(roll_num)
	if current_student:
		print(current_student)
	else:
		print("Student Not Found.\n")


def view_all_students():
	exist = students_exist()
	if not exist:
		return
	print("----------------------------------------------------------------------------------------------------------")
	print(f"{'S.no.' : <8}{'Name' : <25}{'Roll Number' : <15}{'Grade' : <10}Branch")
	print("----------------------------------------------------------------------------------------------------------")


	for i,data in enumerate(config.students,start = 1):

		print(f"{str(i)+'.' :<8}{data.name :<25}{data.roll_number : ^15}{data.grade : <10}{data.branch}")

	print("\n")

def update_student_branch():
	roll_num = input("Enter student roll_number : ").strip()
	print("\n")
	student = find_student_by_roll(roll_num)
	if student:
		branch = get_valid_branch()
		student.update_branch(branch)
		#later will keep branch change optioon only for students coming to 2nd yr. means for starting of 2nd yr. and will make separate classes for respective yrs.
		save_all_students()
		print("Student details updated.")
		print()
		print(student)
	else:
		print("\nStudent Not Found.\n")

def update_student_grade():
	roll_num = input("Enter student roll_number : ").strip()
	print("\n")
	student = find_student_by_roll(roll_num)
	if student:
		#checking for valid grades.
		grade = input_valid_grade()
		student.update_grade(grade)
		print()
		save_all_students()
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
		if(choice == "1"):
			update_student_branch()
		elif(choice == "2"):
			update_student_grade()
		elif(choice == "3"):
			print("\nExiting...\n")
			return
		else:
			print("\nInvalid Choice.\n")


def remove_student():
	exist = students_exist()
	if not exist:
		return
	roll_num = input("Enter Student Roll Number : ")
	print()
	student = find_student_by_roll(roll_num)
	if student:
		user_input = input(f"Are you sure you want to remove {student.name} (y/n) : ").strip().lower()
		if(user_input == "y"):
			config.students.remove(student)
			save_all_students()
			print("\nStudent removed.\n")
			print(student)
		elif(user_input == "n"):
			print("\nOperation Cancelled\n")
		else :
			print("\nInvalid Input\n")
	else:
		print("\nStudent Not Found\n")
