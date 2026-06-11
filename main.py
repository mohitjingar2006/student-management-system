from admin import admin_menu
from teacher import load_teachers,teacher_menu
from student import load_students
import config

config.students = load_students()
config.teachers = load_teachers()

while True:
	print("========================================================================================= Student Management System =============================================================================================")
	print("\n\n")
	print("1.Login")
	print("2.Exit Program")
	print("\n\n")
	main_choice = input("Enter your choice : ")
	print()
	if main_choice == "1":
		while True:
			print("Main Menu : ")
			print()
			print("1.Login as Admin")
			print("2.Login as Teacher")
			print("3.Exit")
			print()
			login_choice = input("Enter your choice : ")
			print("\n")
			if login_choice == "1":
				admin_menu()
			elif login_choice == "2":
				teacher_menu()
			elif login_choice == "3":
				print("\nReturning to main menu...\n")
				break
			else:
				print("\nInvalid Input.\n")
	elif main_choice == "2":
		print("\nExiting program...\n")
		break
	else:
		print("\nInvalid Input.\n")


