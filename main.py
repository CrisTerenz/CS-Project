import sqlite3
import re
import os

# --- DATABASE SETTINGS ---
DB_NAME = "students.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            middle_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            birthdate TEXT NOT NULL,
            place_of_birth TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contact_number TEXT NOT NULL,
            section TEXT NOT NULL,
            league_color TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- VALIDATION HELPER ---
def validate_input(pattern, prompt, error_msg):
    while True:
        user_input = input(prompt).strip()
        if re.fullmatch(pattern, user_input):
            return user_input
        print(f"Invalid format! {error_msg}")

# --- CORE CRUD FUNCTIONS ---

def add_student():
    print("\n--- Add New Student ---")
    s_id = validate_input(r"^20\d{2}-\d{3}$", "Student ID (20YY-XXX): ", "Format must be 20YY-XXX.")
    fname = input("First Name: ").strip()
    mname = input("Middle Name: ").strip()
    lname = input("Last Name: ").strip()
    gender = input("Gender (Male, Female, Others): ").strip()
    bday = validate_input(r"^\d{2}/\d{2}/\d{4}$", "Birthdate (MM/DD/YYYY): ", "Format must be MM/DD/YYYY.")
    bplace = input("Birthplace: ").strip()
    email = validate_input(r"^[\w\.-]+@[\w\.-]+\.\w+$", "Email: ", "Invalid email format.")
    contact = validate_input(r"^(09|\+639)\d{9}$", "Contact Number: ", "Must start with 09 or +639 followed by 9 digits.")
    section = validate_input(r"^Dahlia|Kamia|Rosal|Sampaguita$", "Section (Dahlia, Kamia, Rosal, Sampaguita): ", "Invalid section.")
    color = validate_input(r"^Red|Yellow|Green|Blue$", "League Color (Red, Yellow, Green, Blue): ", "Invalid color.")

    if not all([fname, mname, lname, gender, bplace, section, color]):
        print("Error: All fields are required.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (s_id, fname, mname, lname, gender, bday, bplace, email, contact, section, color))
        conn.commit()
        print("Student added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Student ID or Email already exists.")
    finally:
        conn.close()

def view_students():
    """Displays all records and handles the empty database case[cite: 1]."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    
    print("\n--- Student List ---")
    if not rows:
        print("No records found in the database.")
    else:
        for row in rows:
            print(row)
    conn.close()
    input("\nPress Enter to return to menu...")

def update_student():
    s_id = input("\nEnter Student ID to update (20YY-XXX): ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE id = ?", (s_id,))
    if not cursor.fetchone():
        print("Record not found.")
    else:
        print("Enter updated information:")
        new_email = validate_input(r"^[\w\.-]+@[\w\.-]+\.\w+$", "New Email: ", "Invalid format.")
        new_contact = validate_input(r"^(09|\+639)\d{9}$", "New Contact: ", "Invalid format.")
        
        cursor.execute("UPDATE students SET email = ?, contact_number = ? WHERE id = ?", 
                       (new_email, new_contact, s_id))
        conn.commit()
        print("Student updated successfully.")
    conn.close()

def delete_student():
    s_id = input("\nEnter Student ID to delete: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (s_id,))
    
    if cursor.rowcount > 0:
        conn.commit()
        print("Student record deleted.")
    else:
        print("Student ID not found.")
    conn.close()

# --- MAIN CONTROL FLOW ---

def main():
    init_db()
    
    while True:
        print("\n==== Student Information System ====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Exiting... Goodbye!")
            break 
        else:
            print("Invalid input. Please choose a number from 1 to 5.")

if __name__ == "__main__":
    main()

