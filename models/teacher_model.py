class Teacher:
	def __init__(self,name,id,password,subject,grades):
		self.name = name
		self.id = id
		self.password = password
		self.subject = subject
		self.grades = grades
	def check_password(self,password):
		return (self.password == password)