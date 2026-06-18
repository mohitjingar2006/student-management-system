import json
import sqlite3

# Helper Functions

def get_connection():
	return sqlite3.connect("student_management.db")


def initialise_database():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS students(
			roll_number TEXT PRIMARY KEY,
			name TEXT NOT NULL,
			grade TEXT NOT NULL,
			branch TEXT NOT NULL
		);
		""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS teachers(
			ID TEXT PRIMARY KEY,
			name TEXT NOT NULL,
			password TEXT,
			subject TEXT NOT NULL,
			grades TEXT NOT NULL
		);
		""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS admin(
			ID INT PRIMARY KEY,
			name TEXT,
			password TEXT
		);
		""")
	conn.commit()
	conn.close()

# Admin setup

def setup_admin():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		INSERT OR IGNORE  INTO admin
		(ID,name,password)
		VALUES (1,"admin","admin123")
		""")
	conn.commit()
	conn.close()

def load_admin():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT *
		FROM admin
		WHERE ID = 1
		"""
	)
	row = cursor.fetchone()
	conn.close()
	return row


# Student setup

def save_student(student):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		INSERT INTO students
		(name,roll_number,grade,branch)
		VALUES
		(?,?,?,?)
		""",(
			student.name,
			student.roll_number,
			student.grade,
			student.branch
			)
	)
	conn.commit()
	conn.close()

def load_students_from_database():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT*
		FROM students
		ORDER BY roll_number
	"""
	)
	rows = cursor.fetchall()

	conn.close()
	return rows


def load_student_by_roll_num(roll_num):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT *
		FROM students
		WHERE roll_number = ?
	""",(roll_num,)
	)
	student = cursor.fetchone()
	conn.close()

	return student

def count_students_by_grade(input_grade):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT COUNT(*)
		FROM students
		WHERE grade = ?
	""",(input_grade,)
	)
	count, = cursor.fetchone()
	conn.close()
	return count


def count_students():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT COUNT(*)
		FROM students
	""")
	count, = cursor.fetchone()
	conn.close()
	return count

def max_roll_num_grade(input_grade):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT MAX(roll_number)
		FROM students
		WHERE grade = ?
	""",(input_grade,)
	)
	result = cursor.fetchone()[0]
	conn.commit()
	conn.close()
	return result


def update_student_branch_db(input_branch,input_roll_num):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		UPDATE students
		SET branch = ?
		WHERE roll_number = ?
	""",(input_branch,input_roll_num)
	)
	conn.commit()
	conn.close()

def update_student_grade_db(input_grade,input_roll_num):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		UPDATE students
		SET grade = ?
		WHERE roll_number = ?
	""",(input_grade,input_roll_num)
	)
	conn.commit()
	conn.close()


def delete_student(roll_num):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		DELETE FROM students
		WHERE roll_number = ?
	""",(roll_num,)
	)
	conn.commit()
	conn.close()



# Teacher setup

def save_teacher(teacher):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		INSERT INTO teachers
		(ID,name,password,subject,grades)
		VALUES
		(?,?,?,?,?)
	""",(
		teacher.id,
		teacher.name,
		teacher.password,
		teacher.subject,
		json.dumps(teacher.grades)
		)
	)
	conn.commit()
	conn.close()


def load_teachers_from_database():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT *
		FROM teachers
	""")
	rows = cursor.fetchall()
	conn.close()
	return rows


def load_teacher_by_id(id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT *
		FROM teachers
		WHERE ID = ?
	""",(id,)
	)
	teacher = cursor.fetchone()
	conn.close()

	return teacher


def count_teachers():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT COUNT(*)
		FROM teachers
	""")
	count, = cursor.fetchone()
	return count


def max_id():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT MAX(ID)
		FROM teachers
	"""
	)
	result = cursor.fetchone()[0]
	conn.commit()
	conn.close()
	return result


def update_teacher_grades_db(input_grades,input_id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		UPDATE teachers
		SET grades = ?
		WHERE ID = ?
	""",(input_grades,input_id)
	)
	conn.commit()
	conn.close()


def update_teacher_subject_db(input_subject,input_id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		UPDATE teachers
		SET subject = ?
		WHERE ID = ?
	""",(input_subject,input_id)
	)
	conn.commit()
	conn.close()


def delete_teacher(id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		DELETE FROM teachers
		WHERE ID = ?
	""",(id,)
	)
	conn.commit()
	conn.close()
