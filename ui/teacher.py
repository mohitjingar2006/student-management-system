from services.teacher_service import (
	teacher_exist,
	find_teacher_by_id
)
from services.student_service import (
	view_all_students,
	search_student
)
from utils import require_non_empty
from mask_input import get_masked_input


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



