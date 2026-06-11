def require_non_empty(prompt,error_message="Input cannot be empty."):
	value = input(prompt).strip()
	while value == '':
		print(error_message)
		value = input(prompt).strip()
	return value

