import tkinter as tk
from tkinter import ttk, messagebox
from SGMS import SGMS

class SGMS_GUI:
    def __init__(self):
        self.system = SGMS()
        self.root = tk.Tk()
        self.root.title("SGMS - Student Grade Management System")
        self.root.geometry("1000x750")
        self.root.resizable(False, False)

        self.current_user = None
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="SGMS", font=("Arial", 36, "bold")).pack(pady=(0, 20))
        ttk.Label(main_frame, text="Main Menu", font=("Arial", 14)).pack(anchor="w", pady=(0, 15))

        login_frame = ttk.LabelFrame(main_frame, text=" Login ", padding=25)
        login_frame.pack(fill="x", pady=10)

        ttk.Label(login_frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.username_entry = ttk.Entry(login_frame, width=35, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, pady=8, padx=15)

        ttk.Label(login_frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.password_entry = ttk.Entry(login_frame, width=35, font=("Arial", 11), show="*")
        self.password_entry.grid(row=1, column=1, pady=8, padx=15)

        btn_frame = ttk.Frame(login_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=25)
        ttk.Button(btn_frame, text="Login", command=self.handle_login, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit, width=18).pack(side="left", padx=8)

        self.username_entry.focus()

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if username in self.system.users:
            user_data = self.system.users[username]
            stored_salt = user_data.get("salt")
            stored_hash = user_data.get("hash")
            input_data = self.system._hash_password(password, stored_salt)
            input_hash = input_data["hash"]

            if input_hash == stored_hash:
                self.system.current_user = {
                    "username": username,
                    "role": user_data.get("role", "student")
                }
                self.current_user = self.system.current_user

                messagebox.showinfo("Login Successful",
                                    f"Welcome back, {username} ({self.current_user['role']})!")
                self.show_user_menu()
                return
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "Username not found.")

    def show_user_menu(self):
        self.clear_window()
        if self.current_user is None:
            messagebox.showerror("Error", "No user logged in.")
            self.show_login_screen()
            return

        role = self.current_user["role"]
        username = self.current_user["username"]
        if username in self.system.students:
            display_name = self.system.students[username].get("name", username)
        elif username in self.system.teachers:
            display_name = self.system.teachers[username].get("name", username)
        else:
            display_name = username
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text=f"Welcome back, {display_name}",
                  font=("Arial", 18, "bold")).pack(pady=(0, 5))
        ttk.Label(main_frame, text=f"Role: {role.capitalize()}",
                  font=("Arial", 12)).pack(pady=(0, 30))

        menu_frame = ttk.LabelFrame(main_frame, text=" User Menu ", padding=30)
        menu_frame.pack(fill="x", pady=10)

        if role in ["admin", "teacher"]:
            ttk.Button(menu_frame, text="1. Add Student", width=35,
                       command=self.open_add_student_window).pack(pady=6)
            ttk.Button(menu_frame, text="2. View all Students", width=35,
                       command=self.open_view_students_window).pack(pady=6)
            ttk.Button(menu_frame, text="3. Add Grade", width=35,
                       command=self.open_add_grade_window).pack(pady=6)
            ttk.Button(menu_frame, text="4. View student grades and averages", width=35,
                       command=self.open_view_grades_window).pack(pady=6)
            ttk.Button(menu_frame, text="Create Student Account", width=35,
                       command=self.open_create_student_account).pack(pady=6)

            if role == "admin":
                ttk.Button(menu_frame, text="Create Teacher Account", width=35,
                           command=self.open_create_teacher_account).pack(pady=6)
                ttk.Button(menu_frame, text="View/Reset User Password", width=35,
                           command=self.open_view_reset_password).pack(pady=6)
        else:
            ttk.Button(menu_frame, text="View My Grades", width=35,
                       command=self.open_view_my_grades).pack(pady=6)

        logout_btn = ttk.Button(menu_frame, text="5. Logout", width=35,
                                command=self.show_login_screen)
        logout_btn.pack(pady=35)
        style = ttk.Style()
        style.configure("Logout.TButton", foreground="red", font=("Arial", 10, "bold"))
        logout_btn.configure(style="Logout.TButton")
    def open_view_reset_password(self):
        if self.current_user["role"] != "admin":
            messagebox.showerror("Access Denied", "Only admins can view or reset passwords.")
            return

        pw_win = tk.Toplevel(self.root)
        pw_win.title("View /Reset User Password")
        pw_win.geometry("520x420")
        pw_win.grab_set()
        ttk.Label(pw_win, text="View or Reset User Password", font=("Arial", 14, "bold")).pack(pady=15)
        ttk.Label(pw_win, text="Enter Username (Student or Teacher ID):").pack(anchor="w", padx=40, pady=(10, 0))
        username_entry = ttk.Entry(pw_win, width=40)
        username_entry.pack(padx=40, pady=5)
        result_label = ttk.Label(pw_win, text="", foreground="blue", justify="left")
        result_label.pack(pady=20, padx=40, anchor="w")
        def show_info():
            username = username_entry.get()
            if not username:
                messagebox.showerror("Error", "Please enter a username.")
                return

            if username not in self.system.users:
                messagebox.showerror("Error", "Username not found.")
                return

            user_data = self.system.users[username]
            role = user_data.get("role", "unknown")

            result_label.config(text=f"Username: {username}\n"
                                     f"Role: {role.capitalize()}\n\n"
                                     f"Password Status: Hashed for security\n\n"
                                     f"Reset Method: Use 'Create Student Account' or 'Create Teacher Account'\n"
                                     f"to generate a new temporary password for this user.")

        btn_frame = ttk.Frame(pw_win)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Show Info", command=show_info, width=18).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Close", command=pw_win.destroy, width=18).pack(side="left", padx=10)

    def open_view_my_grades(self):
        student_id = self.current_user["username"]
        if student_id not in self.system.students:
            messagebox.showerror("Error", "Your student record was not found.")
            return
        self.view_student_grades(student_id)


    def open_add_student_window(self):
        if self.current_user["role"] not in ["admin", "teacher"]:
            messagebox.showerror("Access Denied", "Only admins and teachers can add students.")
            return
        add_win = tk.Toplevel(self.root)
        add_win.title("Add New Student")
        add_win.geometry("420x300")
        add_win.grab_set()

        ttk.Label(add_win, text="Add New Student", font=("Arial", 14, "bold")).pack(pady=15)
        ttk.Label(add_win, text="Student ID:").pack(anchor="w", padx=40, pady=(10, 0))
        self.id_entry = ttk.Entry(add_win, width=40)
        self.id_entry.pack(padx=40, pady=5)

        ttk.Label(add_win, text="Student Name:").pack(anchor="w", padx=40, pady=(15, 0))
        self.name_entry = ttk.Entry(add_win, width=40)
        self.name_entry.pack(padx=40, pady=5)

        def save_student():
            student_id = self.id_entry.get()
            name = self.name_entry.get()

            if not student_id or not name:
                messagebox.showerror("Error", "Student ID and Name cannot be empty.")
                return

            try:
                self.system.add_student(student_id, name)
                messagebox.showinfo("Success", f"Student '{name}' added successfully")
                add_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not add student.\n{str(e)}")

        btn_frame = ttk.Frame(add_win)
        btn_frame.pack(pady=25)

        ttk.Button(btn_frame, text="Save Student", command=save_student, width=15).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=add_win.destroy, width=15).pack(side="left", padx=10)

    def open_view_students_window(self):
        if self.current_user["role"] not in ["admin", "teacher"]:
            messagebox.showerror("Access Denied", "Only admins and teachers can view all students.")
            return

        view_win = tk.Toplevel(self.root)
        view_win.title("View All Students")
        view_win.geometry("650x550")
        view_win.grab_set()
        ttk.Label(view_win, text="All Students", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(view_win, text="Search by ID or Name:").pack(anchor="w", padx=40, pady=(10, 0))
        search_entry = ttk.Entry(view_win, width=40)
        search_entry.pack(padx=40, pady=5)
        columns = ("Student ID", "Name")
        tree = ttk.Treeview(view_win, columns=columns, show="headings", height=15)
        tree.heading("Student ID", text="Student ID")
        tree.heading("Name", text="Student Name")
        tree.column("Student ID", width=180, anchor="center")
        tree.column("Name", width=380, anchor="w")
        tree.pack(padx=40, pady=10, fill="both", expand=True)

        def refresh_table(filter_text=""):
            for item in tree.get_children():
                tree.delete(item)
            filter_text = filter_text.lower()
            for student_id, info in self.system.students.items():
                name = info["name"].lower()
                if filter_text == "" or filter_text in student_id.lower() or filter_text in name:
                    tree.insert("", "end", values=(student_id, info["name"]))
        refresh_table()
        ttk.Button(view_win, text="Search",
                   command=lambda: refresh_table(search_entry.get())).pack(pady=8)

        ttk.Button(view_win, text="Close", command=view_win.destroy).pack(pady=10)

    def get_letter_grade(self, grade):
        if grade >= 9:
            return "A*"
        elif grade >= 7:
            return "A"
        elif grade == 6:
            return "B"
        elif grade >= 4:
            return "C"
        else:
            return "U"

    def open_add_grade_window(self):
        if self.current_user["role"] not in ["admin", "teacher"]:
            messagebox.showerror("Access Denied", "Only admins and teachers can add grades.")
            return
        grade_win = tk.Toplevel(self.root)
        grade_win.title("Add Grade")
        grade_win.geometry("420x320")
        grade_win.grab_set()

        ttk.Label(grade_win, text="Add Grade for Student", font=("Arial", 14, "bold")).pack(pady=15)

        ttk.Label(grade_win, text="Student ID:").pack(anchor="w", padx=40, pady=(10, 0))
        student_id_entry = ttk.Entry(grade_win, width=40)
        student_id_entry.pack(padx=40, pady=5)
        ttk.Label(grade_win, text="Subject:").pack(anchor="w", padx=40, pady=(15, 0))
        subject_entry = ttk.Entry(grade_win, width=40)
        subject_entry.pack(padx=40, pady=5)
        ttk.Label(grade_win, text="Grade (0-9):").pack(anchor="w", padx=40, pady=(15, 0))
        grade_entry = ttk.Entry(grade_win, width=40)
        grade_entry.pack(padx=40, pady=5)

        def save_grade():
            student_id = student_id_entry.get()
            subject = subject_entry.get()
            grade_str = grade_entry.get()
            if not student_id or not subject or not grade_str:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                grade = int(grade_str)
            except ValueError:
                messagebox.showerror("Error", "Grade must be a number.")
                return
            if grade < 0 or grade > 9:
                messagebox.showerror("Error", "Grade must be between 0 and 9.")
                return
            try:
                self.system.add_grade(student_id, subject, grade)
                messagebox.showinfo("Success", f"Grade for {subject} added successfully!")
                grade_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add grade.\n{str(e)}")

        btn_frame = ttk.Frame(grade_win)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="Save Grade", command=save_grade, width=15).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=grade_win.destroy, width=15).pack(side="left", padx=10)

    def get_performance_level(self, grade):
        if grade == 9:
            return "Excellent"
        elif grade >= 7:
            return "Performing Well"
        elif grade >= 5:
            return "Decent"
        elif grade == 4:
            return "Borderline"
        else:
            return "Underperforming"

    def open_view_grades_window(self):
        if self.current_user["role"] not in ["admin", "teacher"]:
            messagebox.showerror("Access Denied", "Only admins and teachers can view grades.")
            return

        view_win = tk.Toplevel(self.root)
        view_win.title("View Student Grades")
        view_win.geometry("720x580")
        view_win.grab_set()

        ttk.Label(view_win, text="View Student Grades", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(view_win, text="Enter Student ID:").pack(anchor="w", padx=40, pady=(10, 0))
        student_id_entry = ttk.Entry(view_win, width=40)
        student_id_entry.pack(padx=40, pady=5)
        self.result_frame = ttk.Frame(view_win)
        self.result_frame.pack(padx=40, pady=15, fill="x")

        def show_grades():
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            student_id = student_id_entry.get()

            if not student_id:
                messagebox.showerror("Error", "Please enter a Student ID.")
                return

            if student_id not in self.system.students:
                messagebox.showerror("Error", "Student ID not found.")
                return
            student = self.system.students[student_id]
            grades = student.get("grades", {})

            if not grades:
                ttk.Label(self.result_frame, text="No grades recorded for this student yet.",
                          foreground="red").pack(pady=10)
                return

            columns = ("Subject", "Grade", "Letter Grade", "Performance Level")
            tree = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=10)
            tree.heading("Subject", text="Subject")
            tree.heading("Grade", text="Grade")
            tree.heading("Letter Grade", text="Letter Grade")
            tree.heading("Performance Level", text="Performance Level")
            tree.column("Subject", width=200)
            tree.column("Grade", width=80, anchor="center")
            tree.column("Letter Grade", width=100, anchor="center")
            tree.column("Performance Level", width=180, anchor="w")
            tree.pack(fill="x", pady=5)

            total = 0
            count = 0

            for subject, grade in grades.items():
                letter = self.get_letter_grade(grade)
                performance = self.get_performance_level(grade)
                tree.insert("", "end", values=(subject, grade, letter, performance))
                total += grade
                count += 1
            if count > 0:
                average = round(total / count, 1)
                avg_letter = self.get_letter_grade(average)
                avg_performance = self.get_performance_level(average)

                ttk.Label(self.result_frame,
                          text=f"Overall Average: {average} ({avg_letter}) - {avg_performance}",
                          font=("Arial", 12, "bold")).pack(pady=15)

        btn_frame = ttk.Frame(view_win)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Show Grades", command=show_grades, width=15).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Close", command=view_win.destroy, width=15).pack(side="left", padx=10)

    def view_student_grades(self, student_id):
        view_win = tk.Toplevel(self.root)
        view_win.title("My Grades")
        view_win.geometry("700x520")
        view_win.grab_set()

        student = self.system.students[student_id]

        ttk.Label(view_win, text=f"Grades for {student['name']}",
                  font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("Subject", "Grade", "Letter Grade", "Performance")
        tree = ttk.Treeview(view_win, columns=columns, show="headings", height=12)

        tree.heading("Subject", text="Subject")
        tree.heading("Grade", text="Grade")
        tree.heading("Letter Grade", text="Letter Grade")
        tree.heading("Performance", text="Performance Level")
        tree.column("Subject", width=220, anchor="w")
        tree.column("Grade", width=80, anchor="center")
        tree.column("Letter Grade", width=100, anchor="center")
        tree.column("Performance", width=200, anchor="w")
        tree.pack(padx=40, pady=15, fill="x")

        total = 0
        count = 0

        for subject, grade in student.get("grades", {}).items():
            letter = self.get_letter_grade(grade)
            performance = self.get_performance_level(grade)
            tree.insert("", "end", values=(subject, grade, letter, performance))
            total += grade
            count += 1

        if count > 0:
            average = round(total / count, 1)
            avg_letter = self.get_letter_grade(average)
            avg_performance = self.get_performance_level(average)
            ttk.Label(view_win, text=f"Overall Average: {average} ({avg_letter}) - {avg_performance}",
                      font=("Arial", 12, "bold")).pack(pady=15)

        ttk.Button(view_win, text="Close", command=view_win.destroy).pack(pady=10)




    def run(self):
        self.root.mainloop()

    def open_create_student_account(self):
        if self.current_user["role"] != "admin":
            messagebox.showerror("Access Denied", "Only admins can create student accounts.")
            return

        create_win = tk.Toplevel(self.root)
        create_win.title("Create Student Account")
        create_win.geometry("450x340")
        create_win.grab_set()

        ttk.Label(create_win, text="Create Student Account", font=("Arial", 14, "bold")).pack(pady=15)
        ttk.Label(create_win, text="Student ID (will be username):").pack(anchor="w", padx=40, pady=(10, 0))
        id_entry = ttk.Entry(create_win, width=40)
        id_entry.pack(padx=40, pady=5)
        ttk.Label(create_win, text="Student Full Name:").pack(anchor="w", padx=40, pady=(15, 0))
        name_entry = ttk.Entry(create_win, width=40)
        name_entry.pack(padx=40, pady=5)
        ttk.Label(create_win, text="Temporary Password:").pack(anchor="w", padx=40, pady=(15, 0))
        password_entry = ttk.Entry(create_win, width=40, show="*")
        password_entry.pack(padx=40, pady=5)

        def create_account():
            student_id = id_entry.get().strip()
            name = name_entry.get().strip()
            password = password_entry.get().strip()
            if not student_id or not name or not password:
                messagebox.showerror("Error", "All fields are required.")
                return

            if student_id in self.system.students:
                messagebox.showerror("Error", "A student with this ID already exists.")
                return

            try:
                self.system.students[student_id] = {
                    "name": name,
                    "grades": {}
                }
                hashed_data = self.system._hash_password(password)
                self.system.users[student_id] = {
                    "salt": hashed_data["salt"],
                    "hash": hashed_data["hash"],
                    "role": "student"
                }
                self.system.save_data()
                messagebox.showinfo("Success",
                                    f"Student account for {name} (ID: {student_id}) created successfully!\n\nTemporary password: {password}")
                create_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create account.\n{str(e)}")
        btn_frame = ttk.Frame(create_win)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="Create Account", command=create_account, width=18).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=create_win.destroy, width=18).pack(side="left", padx=10)

    def open_create_teacher_account(self):
        if self.current_user["role"] != "admin":
            messagebox.showerror("Access Denied", "Only admins can create teacher accounts.")
            return

        create_win = tk.Toplevel(self.root)
        create_win.title("Create Teacher Account")
        create_win.geometry("450x340")
        create_win.grab_set()

        ttk.Label(create_win, text="Create Teacher Account", font=("Arial", 14, "bold")).pack(pady=15)

        ttk.Label(create_win, text="Teacher Username (ID):").pack(anchor="w", padx=40, pady=(10, 0))
        id_entry = ttk.Entry(create_win, width=40)
        id_entry.pack(padx=40, pady=5)

        ttk.Label(create_win, text="Teacher Full Name:").pack(anchor="w", padx=40, pady=(15, 0))
        name_entry = ttk.Entry(create_win, width=40)
        name_entry.pack(padx=40, pady=5)

        ttk.Label(create_win, text="Temporary Password:").pack(anchor="w", padx=40, pady=(15, 0))
        password_entry = ttk.Entry(create_win, width=40, show="*")
        password_entry.pack(padx=40, pady=5)

        def create_teacher_account():
            teacher_id = id_entry.get().strip()
            name = name_entry.get().strip()
            password = password_entry.get().strip()

            if not teacher_id or not name or not password:
                messagebox.showerror("Error", "All fields are required.")
                return

            if teacher_id in self.system.users:
                messagebox.showerror("Error", "A user with this username already exists.")
                return

            try:
                self.system.teachers[teacher_id] = {
                    "name": name
                }

                hashed_data = self.system._hash_password(password)
                self.system.users[teacher_id] = {
                    "salt": hashed_data["salt"],
                    "hash": hashed_data["hash"],
                    "role": "teacher"
                }

                self.system.save_data()
                messagebox.showinfo("Success",
                                    f"Teacher account for {name} (Username: {teacher_id}) created successfully!\n\n"
                                    f"Temporary password: {password}")
                create_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create teacher account.\n{str(e)}")

        btn_frame = ttk.Frame(create_win)
        btn_frame.pack(pady=25)

        ttk.Button(btn_frame, text="Create Teacher", command=create_teacher_account, width=18).pack(side="left",
                                                                                                    padx=10)
        ttk.Button(btn_frame, text="Cancel", command=create_win.destroy, width=18).pack(side="left", padx=10)


if __name__ == "__main__":
    app = SGMS_GUI()
    app.run()
