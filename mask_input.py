import os
def get_masked_input_windows():
	import msvcrt
	password_lst = []
	while True:
		ch = msvcrt.getch().decode()
		if ch in ('\n','\r'):
			password_string = ''.join(password_lst)
			return password_string
		elif ch in ('\x08','\x7f'):
			if password_lst :
				password_lst.pop()
				print("\b \b",end ='',flush = True)
			else:
				continue
		else:
			password_lst.append(ch)
			print("*",end = '',flush = True)



def get_masked_input_posix():
	import sys
	import termios
	password_lst = []
	fd = sys.stdin.fileno()
	original_settings = termios.tcgetattr(fd)
	new_settings = termios.tcgetattr(fd)
	new_settings[3] = new_settings[3] & ~termios.ECHO & ~termios.ICANON
	try:
		termios.tcsetattr(fd,termios.TCSANOW,new_settings)
		password_lst = []
		while True:
			ch = sys.stdin.read(1)
			if ch in ('\n','\r'):
				password_string = ''.join(password_lst)
				return password_string
			elif ch in ('\x08','\x7f'):
				if password_lst:
					password_lst.pop()
					print("\b \b",end ='',flush = True)
				else:
					continue
			else:
				password_lst.append(ch)
				print("*",end = '',flush = True)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN,original_settings)
		print()


def get_masked_input():
	if os.name == 'nt':
		return get_masked_input_windows()
	return get_masked_input_posix()
	
