import csv
from admin import Admin
from student import add_student,view_all_students,load_students,search_student,update_student_details,remove_student
import config

config.students = load_students()

admin_name = ""
admin_password = ""
try:
	with open("admin.csv",newline = "") as file:
		reader = csv.reader(file)
		admin_name ,admin_password = next(reader)
except FileNotFoundError:
	print("admin.csv file not found.")
	print()
admin = Admin(admin_name,admin_password)


while True:
	print("=================================================================================================== Student Management System =======================================================================================================")
	print("\n\n")
	print("Login as Admin")
	print("\n\n")
	admin_name = input("Enter your name : ").strip()
	while admin_name == "":
		name = input("Name cannot be empty : ").strip()
	if(admin.check_name(admin_name)):
		password = input("Enter your password : ").strip()
		if(admin.check_password(password)):
			while True:
				print("\nMenu :\n")
				print("1. View All Students")
				print("2. Add Student")
				print("3. Search Student")
				print("4. Remove Student")
				print("5. Update Student details")
				#later I would give this option after opening the student details 
				print("6. Exit")
				print("\n")
				choice = input("Enter your choice : ")
				print("\n")
				if(choice == "1"):
					view_all_students()
				elif(choice == "2"):
					add_student()
				elif(choice == "3"):
					search_student()
				elif(choice == "4"):
					remove_student()
				elif(choice == "5"):
					update_student_details()
				elif(choice == "6"):
					print("\nExiting system...\n")
					break
				else:
					print("\nInvalid Choice.\n")
		else:
			print("\nInvalid Password.\n")
	else:
		print("\nAdmin not found.\n")


