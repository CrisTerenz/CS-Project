import sqlite3
import re

# Database
DB_NAME = "students.db"
def connect_db():
    return sqlite3.connect(DB_NAME)

# Add student
def add_student():
    return

# View students
def view_students():
    return

# Update student
def update_student():
    return

# Delete students
def delete_student():
    return

# Main
while True:
    print("""
1. Add Student
2. View Students
3. Update Student
4. Delete Student
5. Exit
""")

    choice = input("Enter choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        update_student()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        print("Terminating")
        break
    else:
        print("Invalid choice.")
