import json
import sqlite3

# Helper Functions

def get_connection() -> sqlite3.Connection:
	conn = sqlite3.connect("student_management.db",timeout=20)
	conn.row_factory = sqlite3.Row
	return conn


def initialise_database() -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS admin(
				ID INT PRIMARY KEY,
				name TEXT,
				password TEXT
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
			CREATE TABLE IF NOT EXISTS students(
				roll_number TEXT PRIMARY KEY,
				name TEXT NOT NULL,
				grade TEXT NOT NULL,
				branch TEXT NOT NULL
			);
			""")
		conn.commit()


# Admin setup

def setup_admin() -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			INSERT OR IGNORE  INTO admin
			(ID,name,password)
			VALUES (1,"admin","admin123")
			""")
		conn.commit()


def load_admin()-> sqlite3.Row | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT *
			FROM admin
			WHERE ID = 1
			"""
		)
		row = cursor.fetchone()
		return row


# Student setup

def save_student(student) -> None:
	with get_connection() as conn:
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
	

def load_students_from_database() -> list[sqlite3.Row] | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT*
			FROM students
			ORDER BY roll_number
		"""
		)
		rows = cursor.fetchall()
		return rows


def load_student_by_roll_number(roll_number : str) -> sqlite3.Row | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT *
			FROM students
			WHERE roll_number = ?
		""",(roll_number,)
		)
		student = cursor.fetchone()
		return student


def count_students_by_grade(grade : str) -> int:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT COUNT(*)
			FROM students
			WHERE grade = ?
		""",(grade,)
		)
		count, = cursor.fetchone()
		return count


def get_student_count() -> int:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT COUNT(*)
			FROM students
		""")
		count, = cursor.fetchone()
		return count


def max_roll_number_grade(grade : str) -> str | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT MAX(roll_number)
			FROM students
			WHERE grade = ?
		""",(grade,)
		)
		result = cursor.fetchone()[0]
		return result


def update_student_branch_db(branch : str, roll_number : str) -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			UPDATE students
			SET branch = ?
			WHERE roll_number = ?
		""",(branch,roll_number)
		)
		conn.commit()
	

def update_student_grade_db(grade : str, roll_number : str) -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			UPDATE students
			SET grade = ?
			WHERE roll_number = ?
		""",(grade,roll_number)
		)
		conn.commit()
	

def delete_student(roll_number : str) -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			DELETE FROM students
			WHERE roll_number = ?
		""",(roll_number,)
		)
		conn.commit()


# Teacher setup

def save_teacher(teacher) -> None:
	with get_connection() as conn:
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
	

def load_teachers_from_database() -> list[sqlite3.Row] | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT *
			FROM teachers
		""")
		rows = cursor.fetchall()
		return rows


def load_teacher_by_id(id : str) -> sqlite3.Row | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT *
			FROM teachers
			WHERE ID = ?
		""",(id,)
		)
		teacher = cursor.fetchone()
		return teacher


def get_teacher_count() -> int:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT COUNT(*)
			FROM teachers
		""")
		count, = cursor.fetchone()
		return count


def get_last_teacher_id() -> str | None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			SELECT MAX(ID)
			FROM teachers
		"""
		)
		result = cursor.fetchone()[0]
		return result


def update_teacher_grades_db(grades : str,id : str) -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			UPDATE teachers
			SET grades = ?
			WHERE ID = ?
		""",(grades,id)
		)
		conn.commit()
	

def update_teacher_subject_db(subject : str, id : str) -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			UPDATE teachers
			SET subject = ?
			WHERE ID = ?
		""",(subject,id)
		)
		conn.commit()
	

def delete_teacher(id : str) -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			DELETE FROM teachers
			WHERE ID = ?
		""",(id,)
		)
		conn.commit()
	
