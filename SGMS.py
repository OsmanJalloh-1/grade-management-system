import json
import os
import hashlib
import secrets
DATA_FILE = "data.json"


class System:
    def __init__(self):
        self.data = {"users": {}, "student": {}}
        self.load()
    #Storing main attributes
    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
    #Checks if the data file is actually existing
                self.data = json.load(f)
        else:
            self.save()
    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)
    def require_role(self, roles):
        # One of if not the most important function since it prevents student malpractice
        return True

    def admin_menu(self):
        #Admin menu function
        while True:
            print("1. Add a student")
            #   Allows for user input when wanting to add a student
            print("2. View students")
            #Allows for user input when wanting to view the students that are currently in the data.json record
            print("3. Add grade")
            #Allows for user input when wanting to add a grade
            print("4. Log out")
            #User is able to exit

            choice = input("Choose an option: ") #User has to pick a choice between 1 and 4
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.add_grade()
            elif choice == "4":
                break
    def add_student(self):
        student_id = input("Enter student ID: ") #Makes it so that the user can add a student ID for the added student

        #User can enter the student's ID
        name = input("Enter student name: ")
        #User can enter the student's name

        if not student_id or not name:
            print("Student ID and name cannot be empty.")

            #If there isnt a student ID or name the program will return

            return

        if student_id in self.data["student"]:
            print("This student already exists.")
#This allows for non duplicates of the same student
            return
        self.data["student"][student_id] = {
            "name": name,
            "grades": {}
        }
        self.save()
        print("The student was added successfully.")

    def view_students(self):
        if not self.require_role(["admin", "teacher"]):
            return
        if not self.data["student"]:
            #If the student an admin or teacher searched for wasnt in the record the below print statement is printed out
            print("There were no students found.")
            return
        for student_id, info in self.data["student"].items():
            print(student_id, "-", info["name"])

    def add_grade(self):
        if not self.require_role(["admin", "teacher"]):
            return
#  Functions above are exclusive to teachers/admins
        student_id = input("Student ID: ")
        if student_id not in self.data["student"]:
            print("Student was not found.")
            return

        subject = input("Subject: ")
        if not subject:
            print("Empty subject.")
            return

        grade_str = input("Grade (0-9): ")
        #Below if statement mmakes sure that the grade must be an integer
        if not grade_str.isdigit():
            print("Grade has to be an integer.")
            return

        grade = int(grade_str)
        if grade < 0 or grade > 9:
            print("Grade must be between 0 and 9.")
        #Grrade must be between 0 and 0 as thats the minumum and maximum grade that they can store for a gcse student
            return

        record = self.data["student"][student_id]
        record["grades"][subject] = grade

        self.save()
        print(f"Grade saved: {record['name']} | {subject} = {grade}")


def hash_password(password: str, salt: str = None) -> dict:
    if not password:
        raise ValueError("Password cannot be empty.") #If the password is empty the value error is raised


    if salt is None:
        salt = secrets.token_hex(10)

    salted_password = (salt + password).encode()
    hash_digest = hashlib.sha256(salted_password).hexdigest()

    return {"salt": salt, "hash": hash_digest}


if __name__ == "__main__":
    system = System()
    #Stored system as the variable
    system.admin_menu()
    #Allows the sytem to actually run

    def _ensure_admin_exists(self):
        #Makes sure that the admin is authorised
        if "admin" not in self.data["users"]:
            print("Creating default admin account (Haydon19/ 5LMB)") #Can give a default admin account
            salt, hashed = self._hash_password("admin guest")

            self.data["users"]["admin"] = {
                "salt": salt,
                "hash": hashed,
                "role": "admin"
            }
            self.save_data()

    def login(self):
        username = input("username: ")
        #User can give there username


        password = input("Password: ")
        user = self.data["users"].get(username)
        if not user:
            # If the user doesnt exist then its returned
            print("That user doesn't exist.")
            return

        salt = user["salt"] # Gives the user the salt




        #The function below ensures that the hash password would contain the password and the salt
        _, hashed = self._hash_password(password, salt)

        if hashed == user["hash"]:
            self.current_user = {
                "username": username,
                "role": user["role"]
            }
            print(f"Welcome back, {username}!")
        else:
            print("Incorrect password.")

    def logout(self):
        print("Logging out...")
        #User can now logout whenever they want
        self.current_user = None


    def add_student(self):
        #Can add the student
        if not self._check_role(["admin", "teacher"]): #Making sure that the role is an admin or a teacher role.
            #Will return
            return


        student_id = input("Student ID: ")
        #Gives student id an input
        name = str(input("Student name: ")) #Gives the name an input

        if student_id in self.data["student"]: #Verifies that the student ID is stored in the actual record
            print("There is already a student wth that same ID.")
            #Prints that there is already an existing student with that same ID allowing for the user to check there mistype
            return

        self.data["student"][student_id] = {
            "name": name,
            "grades": {}
        }

        self.save_data()
        print("Student added.")

    def view_students(self):
        if not self._check_role(["admin", "teacher"]): #Does not allow authorised access for people who dont have the role of an admin or teacher
            return

        if not self.data["student"]:
            print("No student is in the system yet.")
            return

    def add_grade(self):
        if not self._check_role(["admin", "teacher"]):
            return

        student_id = input("Student ID: ")
        student = self.data["student"].get(student_id)

        if not student:
            print("Student was not found.")
            return

        subject = input("Subject: ")
        grade_input = input("Grade (0-9): ")

        try:
            grade = int(grade_input)
        except ValueError:
            #Grade is an integer
            print("Grade must be a number.")
            #An integer input must be made
            return

        if grade < 0 or grade > 9:
            print("Grade must be between 0 and 9.")
            return

        student["grades"][subject] = grade
        #Student grades have now been saved

        self.save_data()
        #Saves student grade and subject data

        print("Grade saved.") #Gives a statement saying that their grade was saved

    def view_grades(self):
        if not self._check_role(["admin", "teacher"]):
            return
        student_id = input("Student ID: ")
        student = self.data["student"].get(student_id)

        if not student:
            #Returns and gives the statement that no grades were found
            print("Student not found.")
            return
        if not student["grades"]:
            print("No grades recorded.")

            return
        total = 0# The total will start as 0

        count = 0#The count will start from zero

        for subject, grade in student["grades"].items():
            print(f"- {subject}: {grade}")
            total = total + grade

            count = count + 1
            #The count will then increment by 1 whenever the function is returned



        avg = total / count

        #Can give an average of their subject grade
        print(avg)
    def _check_role(self, allowed_roles): #Will validate the user's role
        if not self.current_user:
            print("Log in first.")
            return False

        if self.current_user["role"] not in allowed_roles:
            print("Not allowed role.")
            return False

        return True

    def show_main_menu(self):
        print("1. Login") #Main menu is shown to user

        print("2. Exit")


        choice = input("Choose option: ")

        if choice == "1":
            self.login()



        elif choice == "2":
            system.exit()

        else:
            print("Not an option.")

    def show_user_menu(self): #User has their own menu displayed to them
        print("1. Add student")
        print("2. View students")
        print("3. Add grade")
        print("4. View grades")
        print("5. Logout")

        choice = input("Choose an option: ")


#The user is able to pick any number between 1 and 4 to give a choice
        if choice == "1":

            self.add_student()

        elif choice == "2":
            self.view_students()
        elif choice == "3":
            self.add_grade()
        elif choice == "4":
            self.view_grades()
        elif choice == "5":
            self.logout()
        else:
            print("Invalid option.")



    def run(self):
        while True:
            if self.current_user:
                self.show_user_menu()
            else:
                self.show_main_menu()


if __name__ == "__main__":
    project = SGMS()
    #System gets to run now
    SGMS.run()
    #