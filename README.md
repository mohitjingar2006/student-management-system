![Python](https://img.shields.io/badge/Python-3.12-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Status](https://img.shields.io/badge/Status-Active-success)

# Student Management System

A console-based Student Management System built using Python and SQLite.

This project was developed to learn software development fundamentals, Object-Oriented Programming, database management, software architecture, and backend development concepts.

---

# Features

## Authentication

### Admin Login

* Secure admin authentication
* Password masking in terminal

### Teacher Login

* Teacher authentication using ID and password
* Password masking support

### Cross-Platform Support

* Works on Windows, Linux, and macOS terminals

---

# Student Management

* Add Student
* View All Students
* Search Student by Roll Number
* Update Student Details

  * Change Grade
  * Change Branch
* Remove Student
* Automatic Roll Number Generation

---

# Teacher Management

* Add Teacher
* View All Teachers
* Search Teacher by ID
* Update Teacher Details

  * Change Subject
  * Change Grades
* Remove Teacher
* Automatic Teacher ID Generation
* Automatic Password Generation

---

# Database Features

* SQLite Database Integration
* Persistent Data Storage
* Automatic Database Initialization
* Automatic Admin Account Setup
* Parameterized SQL Queries for Improved Security

---

# Software Architecture

The project follows a layered architecture inspired by real-world applications.

### UI Layer

Handles all user interaction and menu navigation.

### Service Layer

Contains business logic and application rules.

### Model Layer

Defines core entities such as Student, Teacher, and Admin.

### Database Layer

Responsible for database access and persistence.

---

# Technologies Used

* Python 3
* SQLite3
* JSON Module
* Object-Oriented Programming (OOP)

---

# Project Structure

```text
student-management-system/
│
├── main.py
├── database.py
├── constants.py
├── utils.py
├── mask_input.py
│
├── models/
│   ├── admin_model.py
│   ├── student.py
│   └── teacher_model.py
│
├── services/
│   ├── student_service.py
│   └── teacher_service.py
│
├── ui/
│   ├── admin.py
│   └── teacher.py
│
├── student_management.db
│
└── README.md
```

---

# Concepts Practiced

* Classes and Objects
* Encapsulation
* Dunder Methods (`__str__`)
* Modular Programming
* Layered Architecture
* Separation of Concerns
* SQLite Database Operations
* CRUD Operations
* Authentication Systems
* Input Validation
* JSON Serialization
* Cross-Platform Terminal Handling

---

# How to Run

## Clone the Repository

```bash
git clone <repository-url>
```

## Navigate to Project Directory

```bash
cd student-management-system
```

## Run the Application

```bash
python3 main.py
```

---

# Default Admin Credentials

```text
Username: admin
Password: admin123
```

---

# Future Improvements

## Planned Features

* Flask Web Application
* HTML/CSS Frontend
* Password Hashing
* Role-Based Authorization
* Advanced Search and Filtering
* Student Promotion System
* Logging System
* Unit Testing
* REST API Development
* Repository/Data Access Layer
* Deployment on Cloud Platforms

---

# Learning Objectives

This project is being developed as a practical learning exercise for:

* Python Programming
* Object-Oriented Design
* Database Design
* SQL and SQLite
* Backend Development
* Software Architecture
* Software Engineering Principles
* Web Development with Flask

---

# Author

Mohit Jingar

B.Tech Electrical Engineering

Indian Institute of Technology Jodhpur

---

# Project Status

Actively under development and continuously being improved as part of the learning journey.

---

# Version History

## v1.0 - CSV Storage
- Student Management System using CSV files
- Admin and Teacher authentication
- Student CRUD operations
- Teacher CRUD operations
- Password masking

## v2.0 - SQLite Migration (Current)
- Migrated from CSV to SQLite
- Improved project architecture
- Introduced Models, Services, and UI layers
- Added JSON serialization for teacher grades
- Improved code organization and maintainability

## v3.0 - Planned
- Flask Web Application
- HTML/CSS Frontend
- Password Hashing
- REST API Development
- Deployment