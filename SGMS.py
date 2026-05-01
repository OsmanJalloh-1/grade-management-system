import json
import os
import hashlib
import secrets

FILE_NAME = "data.json"


class SGMS:
    def __init__(self):
        self.current_user = None
        self.users = {}
        self.students = {}
        self.teachers = {}
        self.load_data()
        if "admin" not in self.users:
            hashed_data = self._hash_password("Defaulthaydonadmin")
            self.users["admin"] = {
                "salt": hashed_data["salt"],
                "hash": hashed_data["hash"],
                "role": "admin"
            }
            print("A default admin account was created")
            self.save_data()

    def load_data(self):
        if not os.path.isfile(FILE_NAME):
            print("No save file was found now creating...")
            self.save_data()
            return

        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                self.users = data.get("users", {})
                self.students = data.get("students", {})
                self.teachers = data.get("teachers", {})
            print("Data loaded")
        except:
            print("Error reading file")
            self.users = {}
            self.students = {}

    def save_data(self):
        data = {
            "users": self.users,
            "student": self.students,
            "teachers": self.teachers
        }
        with open(FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)
        print("Data is saved.")

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)

        salted_password = salt + password
        hash_value = hashlib.sha256(salted_password.encode()).hexdigest()
        return {"salt": salt, "hash": hash_value}

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in self.users:
            user_data = self.users[username]
            stored_salt = user_data["salt"]
            stored_hash = user_data["hash"]
            input_data = self._hash_password(password, stored_salt)
            input_hash = input_data["hash"]

            if input_hash == stored_hash:
                self.current_user = {
                    "username": username,
                    "role": user_data.get("role", "unknown")
                }
                print("Login was successful, welcome " + username)
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Username wasn't found.")
            return False

    def add_student(self, student_id=None, name=None):
        if self.current_user["role"] != "admin" and self.current_user["role"] != "teacher":
            print("You do not have permission to add students.")
            return
        if student_id is None:
            student_id = input("Enter student ID: ")
        if name is None:
            name = input("Enter student name: ")

        if student_id == "" or name == "":
            print("Student ID and name cannot be empty.")
            return

        if student_id in self.students:
            print("A student with this ID already exists.")
            return

        self.students[student_id] = {
            "name": name,
            "grades": {}
        }

        print("Student added successfully.")
        self.save_data()

    def view_students(self):
        if self.current_user["role"] != "admin" and self.current_user["role"] != "teacher":
            print("You do not have permission to view students.")
            return

        if len(self.students) == 0:
            print("No students are in the system yet.")
            return

        print("\nList of students:")
        for student_id in self.students:
            name = self.students[student_id]["name"]
            print(student_id + " - " + name)

    def add_grade(self, student_id=None, subject=None, grade=None):
        if self.current_user["role"] != "admin" and self.current_user["role"] != "teacher":
            print("You do not have permission to add grades.")
            return
        if student_id is None:
            student_id = input("Enter student ID: ")
        if student_id not in self.students:
            print("Student ID not found.")
            return
        if subject is None:
            subject = input("Enter subject name: ")
        if subject == "":
            print("Subject cannot be empty.")
            return
        if grade is None:
            grade_input = input("Enter grade (0-9): ")
            try:
                grade = int(grade_input)
            except ValueError:
                print("Grade must be a number.")
                return
        else:
            pass

        if grade < 0 or grade > 9:
            print("Grade must be between 0 and 9.")
            return

        self.students[student_id]["grades"][subject] = grade
        print(f"Grade added successfully for {self.students[student_id]['name']}")
        self.save_data()

    def view_grades(self):
        if self.current_user["role"] != "admin" and self.current_user["role"] != "teacher":
            print("You do not have permission to view grades.")
            return
        student_id = input("Enter student ID: ")
        if student_id not in self.students:
            print("Student ID not found.")
            return

        student = self.students[student_id]
        grades = student["grades"]

        if len(grades) == 0:
            print("No grades recorded for this student yet.")
            return

        print("\nGrades for " + student["name"] + " (" + student_id + "):")

        total = 0
        count = 0

        for subject in grades:
            grade = grades[subject]
            print(subject + ": " + str(grade))
            total = total + grade
            count = count + 1

        if count > 0:
            average = total / count
            print("Average grade: " + str(average))
        else:
            print("No grades to calculate average.")

    def main_menu(self):
        print(" SGMS Menu ")
        print("1) Login")
        print("2) Exit")

        choice = input("Select option: ")

        if choice == "1":
            if self.login():
                self.logged_in_menu()
            else:
                self.main_menu()
        elif choice == "2":
            quit()
        else:
            print("Please choose a valid option.")
            self.main_menu()



    def logged_in_menu(self):
        while self.current_user is not None:
            role = self.current_user["role"]
            print("\nWelcome back, " + self.current_user["username"] + " (" + role + ")")

            if role == "admin" or role == "teacher":
                print("1) Add student")
                print("2) View students")
                print("3) Add grade")
                print("4) View grades")
                print("5) Logout")

                choice = input("Select option: ")

                if choice == "1":
                    self.add_student()
                elif choice == "2":
                    self.view_students()
                elif choice == "3":
                    self.add_grade()
                elif choice == "4":
                    self.view_grades()
                elif choice == "5":
                    print("Logged out.")
                    self.current_user = None
                else:
                    print("Please choose a valid option.")
            else:
                print("Unknown role.")
                self.current_user = None

    def start(self):
        while True:
            if self.current_user is None:
                self.main_menu()
            else:
                self.logged_in_menu()

    def start(self):
        while True:
            if self.current_user is None:
                self.main_menu()
            else:
                role = self.current_user["role"]
                print("\nWelcome back, " + self.current_user["username"] + " (" + role + ")")
                if role == "admin" or role == "teacher":
                    print("1) Add student")
                    print("2) View students")
                    print("3) Add grade")
                    print("4) View grades")
                    print("5) Logout")

                    choice = input("Select option: ")
                    if choice == "1":
                        self.add_student()
                    elif choice == "2":
                        self.view_students()
                    elif choice == "3":
                        self.add_grade()
                    elif choice == "4":
                        self.view_grades()
                    elif choice == "5":
                        print("Logged out.")
                        self.current_user = None
                    else:
                        print("Please choose a valid option.")
                else:
                    print("Unknown role.")
                    self.current_user = None
