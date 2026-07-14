class Admin:
	def __init__(self,id,name,password):
		self.id = id
		self.name = name
		self.password = password
	def check_name(self,name):
		return (self.name == name)
	def check_password(self,password):
		return (self.password == password)
