class Teacher:
	def __init__(self,name,ID,password,subject,grades):
		self.name = name
		self.id = ID
		self.password = password
		self.subject = subject
		self.grades = grades
	def check_password(self,password):
		return (self.password == password)
	def check_id(self,id):
		return self.id == id