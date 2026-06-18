class Admin:
	def __init__(self,id,name,password):
		self.id = id
		self.__name = name
		self.__password = password
	def check_name(self,name):
		return (self.__name == name)
	def check_password(self,password):
		return (self.__password == password)
