class Admin:
	def __init__(self,name,password):
		self.__name = name
		self.__password = password
	def check_name(self,name):
		return (self.__name == name)
	def check_password(self,password):
		return (self.__password == password)




