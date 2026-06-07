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
	def update_branch(self,Branch):
		self.branch = Branch
	def update_grade(self,Grade):
		self.grade = Grade
	def to_file_format(self):
		return [self.name,self.roll_number,self.grade,self.branch]


def save_all_students():
	with open("student.csv","w",newline = "") as file:
		writer = csv.writer(file)
		for Student in config.students :
			writer.writerow(Student.to_file_format())


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

def avoid_duplicate_roll(roll_num):
	if not config.students :
		return False
	for current_student in config.students :
		if(current_student.roll_number == roll_num):
			return True
	return False


def add_student():
	name = input("Enter Student Name : ").strip()
	while name == "":
		name = input("Name cannot be empty : ").strip()

	roll_num = input("Enter Student Roll number : ").strip()
	while (avoid_duplicate_roll(roll_num)):
		roll_num = input("This roll number exists . Enter different roll number : ").strip()
	grade = input("Enter Student Grade : ").strip()
	grades = ["1st Yr.","2nd Yr.","3rd Yr.","4th Yr."]
	while grade not in grades:
		print("Invalid Grade.")
		grade = input("Enter Student Grade : ").strip()
	branch = input("Enter Student Branch : ").strip()
	while branch == "" or branch.isdigit() :
		print("Invalid Input.")
		branch = input("Enter Student Branch : ").strip()

	student = Student(name,roll_num,grade,branch)

	try:
		with open("student.csv","a",newline = "") as file:
			writer = csv.writer(file)
			writer.writerow(student.to_file_format())

		print("\nStudent Added.\n")
		config.students.append(student)
		print(student)
		print()
	except Exception as e :
		print(e)


def find_student_by_roll(roll_num):
	for current_student in config.students:
		if(current_student.roll_number == roll_num):
			return current_student
	return None


def search_student():
	if not config.students:
		print("No Student Exists.")
		return
	roll_num = input("Enter Student Roll number : ").strip()
	print("\n")
	current_student = find_student_by_roll(roll_num)
	if current_student:
		print(current_student)
	else:
		print("Student Not Found.\n")


def view_all_students():
	if not config.students:
		print("\nNo Student Exists.\n")
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
		student.update_branch(input("Enter Branch of the Student : ").strip())
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
		grade = input("Enter grade of the student : ").strip()
		grades = ["1st Yr.","2nd Yr.","3rd Yr.","4th Yr."]
		while grade not in grades:
			print("Invalid grade.")
			grade = input("Enter grade of the student : ").strip()
		student.update_grade(grade)
		print()
		save_all_students()
		print("\nStudent details updated.\n")
		print(student)
	else:
		print("\nStudent Not Found.\n")


def update_student_details():
	if not config.students:
		print("\nNo Student Exists.\n")
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
	if not config.students:
		print("\nNo Student Exists.\n")
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
