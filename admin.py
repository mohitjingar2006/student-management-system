from utils import require_non_empty
from student import add_student,view_all_students,search_student,update_student_details,remove_student
from teacher import add_teacher,view_all_teachers,search_teacher_by_id,update_teacher_details,remove_teacher

from mask_input import get_masked_input

class Admin:
	def __init__(self,id,name,password):
		self.id = id
		self.__name = name
		self.__password = password
	def check_name(self,name):
		return (self.__name == name)
	def check_password(self,password):
		return (self.__password == password)


def display_student_menu():
	while True:
		print("Student menu :")
		print()
		print("1. View All Students")
		print("2. Add Student")
		print("3. Search Student")
		print("4. Remove Student")
		print("5. Update Student details")
		#later I would give this option after opening the student details
		print("6. Back to admin menu")
		print("\n")
		choice = input("Enter your choice : ")
		print()
		if choice == "1":
			view_all_students()
		elif choice == "2":
			add_student()
		elif choice == "3":
			search_student()
		elif choice == "4":
			remove_student()
		elif choice == "5":
			update_student_details()
		elif choice == "6":
			print("\nBack to admin menu...\n")
			break
		else:
			print("\nInvalid Choice.\n")


def display_teacher_menu():
	while True:
		print("Teacher menu:")
		print()
		print("1. View All Teachers")
		print("2. Add Teacher")
		print("3. Search Teacher")
		print("4. Remove teacher")
		print("5. Update teacher details")
		print("6. Back to admin menu")
		print("\n")
		choice = input("Enter your choice : ")
		print()
		if choice == "1":
			view_all_teachers()
		elif choice == "2":
			add_teacher()
		elif choice == "3":
			search_teacher_by_id()
		elif choice == "4":
			remove_teacher()
		elif choice == "5":
			update_teacher_details()
		elif choice == "6":
			print("\nBack to admin menu...\n")
			break
		else:
			print("\nInvalid Choice.\n")


def admin_menu(admin):
	prompt = "Enter your name : "
	admin_name = require_non_empty(prompt)
	if admin.check_name(admin_name):
		print("Enter your password : ",end = '',flush = True)
		password = get_masked_input()
		if admin.check_password(password):
			print()
			print(f"Welcome {admin_name}")
			print()
			while True:
				print("\nMenu :\n")
				print("1. Student Menu")
				print("2. Teacher Menu")
				print("3. Logout")
				print()
				choice = input("Enter your choice : ")
				print()
				if choice == "1":
					display_student_menu()
				elif choice == "2":
					display_teacher_menu()
				elif choice == "3":
					print("Logging out...")
					print()
					break
				else:
					print("Invalid Input.")
					print()
		else:
				print("\nInvalid Password.\n")
	else:
		print("\nAdmin not found.\n")

