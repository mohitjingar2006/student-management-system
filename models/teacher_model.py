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
