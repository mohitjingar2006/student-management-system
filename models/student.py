class Student:
	def __init__(self,name,roll_number,grade,branch):
		self.name = name
		self.roll_number = roll_number
		self.grade = grade
		self.branch = branch
	def __str__(self):
		return (
			f"{'Name' :<12}: {self.name}\n"
			f"{'Roll Number' :<12}: {self.roll_number}\n"
			f"{'Grade' :<12}: {self.grade}\n"
			f"{'Branch' :<12}: {self.branch}\n"
			)
