import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import requests
from typing import List, Dict, Optional
import threading

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class APIClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url

    def get(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def post(self, endpoint, data):
        try:
            response = requests.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def put(self, endpoint, data):
        try:
            response = requests.put(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def delete(self, endpoint):
        try:
            response = requests.delete(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

class StudentManagementApp:
    def __init__(self):
        self.api = APIClient()
        self.root = ctk.CTk()
        self.root.geometry("1200x800")
        self.root.title("EduCore - Student Management System")
        
        # Initialize data
        self.students = []
        self.courses = []
        
        self.setup_ui()
        self.load_courses()
        self.refresh_students()

    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(self.main_frame, text="EduCore - Student Management System", 
                           font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Create tabs
        self.create_students_tab()
        self.create_grades_tab()
        self.create_reports_tab()

    def create_students_tab(self):
        # Students tab
        self.students_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.students_frame, text="Students")

        # Controls frame
        controls_frame = ctk.CTkFrame(self.students_frame)
        controls_frame.pack(fill="x", padx=20, pady=20)

        # Add student section
        add_frame = ctk.CTkFrame(controls_frame)
        add_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(add_frame, text="Add Student", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        input_frame = ctk.CTkFrame(add_frame)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Student code entry
        ctk.CTkLabel(input_frame, text="Student Code:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.student_code_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 24-49051")
        self.student_code_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Name entry
        ctk.CTkLabel(input_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="Student Name")
        self.name_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Course dropdown
        ctk.CTkLabel(input_frame, text="Course:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.course_var = tk.StringVar(value="BSIT")
        self.course_dropdown = ctk.CTkComboBox(input_frame, variable=self.course_var, values=["BSIT", "BSCS"])
        self.course_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Add button
        ctk.CTkButton(input_frame, text="Add Student", command=self.add_student).grid(row=1, column=2, padx=5, pady=5)

        # Update course section
        update_frame = ctk.CTkFrame(add_frame)
        update_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(update_frame, text="Update Course:").grid(row=0, column=0, padx=5, pady=5)
        self.update_code_entry = ctk.CTkEntry(update_frame, placeholder_text="Student Code")
        self.update_code_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.update_course_var = tk.StringVar(value="BSIT")
        self.update_course_dropdown = ctk.CTkComboBox(update_frame, variable=self.update_course_var, values=["BSIT", "BSCS"])
        self.update_course_dropdown.grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkButton(update_frame, text="Update", command=self.update_student_course).grid(row=0, column=3, padx=5, pady=5)

        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        # Students list
        list_frame = ctk.CTkFrame(self.students_frame)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(list_frame, text="Students List", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Treeview for students
        self.students_tree = ttk.Treeview(list_frame, columns=("Code", "Name", "Course", "GWA", "Description"), show="headings", height=15)
        
        # Configure columns
        self.students_tree.heading("Code", text="Student Code")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.heading("Course", text="Course")
        self.students_tree.heading("GWA", text="GWA")
        self.students_tree.heading("Description", text="Description")

        self.students_tree.column("Code", width=100)
        self.students_tree.column("Name", width=200)
        self.students_tree.column("Course", width=80)
        self.students_tree.column("GWA", width=80)
        self.students_tree.column("Description", width=120)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)

        self.students_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.students_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(buttons_frame, text="Refresh", command=self.refresh_students).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Delete Selected", command=self.delete_student).pack(side="left", padx=5)

    def create_grades_tab(self):
        # Grades tab
        self.grades_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.grades_frame, text="Grades")

        # Controls frame
        controls_frame = ctk.CTkFrame(self.grades_frame)
        controls_frame.pack(fill="x", padx=20, pady=20)

        # Add grade section
        add_grade_frame = ctk.CTkFrame(controls_frame)
        add_grade_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(add_grade_frame, text="Add Grade", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        grade_input_frame = ctk.CTkFrame(add_grade_frame)
        grade_input_frame.pack(fill="x", padx=10, pady=5)

        # Student code entry
        ctk.CTkLabel(grade_input_frame, text="Student Code:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.grade_student_code_entry = ctk.CTkEntry(grade_input_frame, placeholder_text="Student Code")
        self.grade_student_code_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Subject code entry
        ctk.CTkLabel(grade_input_frame, text="Subject Code:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.subject_code_entry = ctk.CTkEntry(grade_input_frame, placeholder_text="e.g., CS 131")
        self.subject_code_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Subject name entry
        ctk.CTkLabel(grade_input_frame, text="Subject Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.subject_name_entry = ctk.CTkEntry(grade_input_frame, placeholder_text="Subject Name")
        self.subject_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Grade entry
        ctk.CTkLabel(grade_input_frame, text="Grade (1.0-5.0):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.grade_entry = ctk.CTkEntry(grade_input_frame, placeholder_text="e.g., 1.25")
        self.grade_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Add grade button
        ctk.CTkButton(grade_input_frame, text="Add Grade", command=self.add_grade).grid(row=2, column=1, columnspan=2, pady=10)

        # Configure grid weights
        grade_input_frame.columnconfigure(1, weight=1)
        grade_input_frame.columnconfigure(3, weight=1)

        # View grades section
        view_frame = ctk.CTkFrame(self.grades_frame)
        view_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(view_frame, text="Student Grades", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Student selection for viewing grades
        select_frame = ctk.CTkFrame(view_frame)
        select_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(select_frame, text="Select Student:").pack(side="left", padx=5)
        self.view_student_code_entry = ctk.CTkEntry(select_frame, placeholder_text="Student Code")
        self.view_student_code_entry.pack(side="left", padx=5)
        ctk.CTkButton(select_frame, text="View Grades", command=self.view_student_grades).pack(side="left", padx=5)

        # Grades treeview
        self.grades_tree = ttk.Treeview(view_frame, columns=("Subject Code", "Subject Name", "Grade", "Description"), show="headings", height=12)
        
        self.grades_tree.heading("Subject Code", text="Subject Code")
        self.grades_tree.heading("Subject Name", text="Subject Name")
        self.grades_tree.heading("Grade", text="Grade")
        self.grades_tree.heading("Description", text="Description")

        self.grades_tree.column("Subject Code", width=100)
        self.grades_tree.column("Subject Name", width=300)
        self.grades_tree.column("Grade", width=80)
        self.grades_tree.column("Description", width=120)

        grades_scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=grades_scrollbar.set)

        self.grades_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        grades_scrollbar.pack(side="right", fill="y", pady=10)

    def create_reports_tab(self):
        # Reports tab
        self.reports_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reports")

        # GWA Report section
        gwa_frame = ctk.CTkFrame(self.reports_frame)
        gwa_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(gwa_frame, text="GWA Report", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Refresh button
        ctk.CTkButton(gwa_frame, text="Refresh GWA Report", command=self.refresh_gwa_report).pack(pady=5)

        # GWA report treeview
        self.gwa_tree = ttk.Treeview(gwa_frame, columns=("Code", "Name", "Course", "GWA", "Description"), show="headings", height=20)
        
        self.gwa_tree.heading("Code", text="Student Code")
        self.gwa_tree.heading("Name", text="Name")
        self.gwa_tree.heading("Course", text="Course")
        self.gwa_tree.heading("GWA", text="GWA")
        self.gwa_tree.heading("Description", text="Description")

        self.gwa_tree.column("Code", width=100)
        self.gwa_tree.column("Name", width=200)
        self.gwa_tree.column("Course", width=80)
        self.gwa_tree.column("GWA", width=80)
        self.gwa_tree.column("Description", width=120)

        gwa_scrollbar = ttk.Scrollbar(gwa_frame, orient="vertical", command=self.gwa_tree.yview)
        self.gwa_tree.configure(yscrollcommand=gwa_scrollbar.set)

        self.gwa_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        gwa_scrollbar.pack(side="right", fill="y", pady=10)

    def load_courses(self):
        """Load courses from API"""
        def load():
            result = self.api.get("/courses")
            if 'error' not in result:
                self.courses = result
                # Update course dropdowns
                course_codes = [course['code'] for course in self.courses]
                self.course_dropdown.configure(values=course_codes)
                self.update_course_dropdown.configure(values=course_codes)
            else:
                messagebox.showerror("Error", f"Failed to load courses: {result['error']}")
        
        threading.Thread(target=load).start()

    def refresh_students(self):
        """Refresh students list"""
        def refresh():
            result = self.api.get("/students")
            if 'error' not in result:
                self.students = result
                self.update_students_tree()
            else:
                messagebox.showerror("Error", f"Failed to load students: {result['error']}")
        
        threading.Thread(target=refresh).start()

    def update_students_tree(self):
        """Update the students treeview"""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)

        # Add students to tree
        for student in self.students:
            gwa = student.get('gwa', 0)
            formatted_gwa = f"{gwa:.2f}" if gwa > 0 else "N/A"
            description = self.get_grade_description(gwa)
            
            self.students_tree.insert("", "end", values=(
                student['student_code'],
                student['name'],
                student['course_code'],
                formatted_gwa,
                description
            ))

    def add_student(self):
        """Add a new student"""
        student_code = self.student_code_entry.get().strip()
        name = self.name_entry.get().strip()
        course = self.course_var.get()

        if not all([student_code, name, course]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        def add():
            data = {
                'student_code': student_code,
                'name': name,
                'course_code': course
            }
            result = self.api.post("/students", data)
            
            if 'error' not in result:
                messagebox.showinfo("Success", "Student added successfully")
                self.student_code_entry.delete(0, 'end')
                self.name_entry.delete(0, 'end')
                self.refresh_students()
            else:
                messagebox.showerror("Error", f"Failed to add student: {result['error']}")

        threading.Thread(target=add).start()

    def delete_student(self):
        """Delete selected student"""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a student to delete")
            return

        item = self.students_tree.item(selection[0])
        student_code = item['values'][0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_code}?"):
            def delete():
                result = self.api.delete(f"/students/{student_code}")
                
                if 'error' not in result:
                    messagebox.showinfo("Success", "Student deleted successfully")
                    self.refresh_students()
                else:
                    messagebox.showerror("Error", f"Failed to delete student: {result['error']}")

            threading.Thread(target=delete).start()

    def update_student_course(self):
        """Update student's course"""
        student_code = self.update_code_entry.get().strip()
        new_course = self.update_course_var.get()

        if not student_code:
            messagebox.showerror("Error", "Please enter student code")
            return

        def update():
            data = {'course_code': new_course}
            result = self.api.put(f"/students/{student_code}", data)
            
            if 'error' not in result:
                messagebox.showinfo("Success", "Student course updated successfully")
                self.update_code_entry.delete(0, 'end')
                self.refresh_students()
            else:
                messagebox.showerror("Error", f"Failed to update student: {result['error']}")

        threading.Thread(target=update).start()

    def add_grade(self):
        """Add a grade for a student"""
        student_code = self.grade_student_code_entry.get().strip()
        subject_code = self.subject_code_entry.get().strip()
        subject_name = self.subject_name_entry.get().strip()
        grade_str = self.grade_entry.get().strip()

        if not all([student_code, subject_code, subject_name, grade_str]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            grade = float(grade_str)
            if grade < 1.0 or grade > 5.0:
                messagebox.showerror("Error", "Grade must be between 1.0 and 5.0")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid grade format")
            return

        def add():
            data = {
                'student_code': student_code,
                'subject_code': subject_code,
                'subject_name': subject_name,
                'grade': grade
            }
            result = self.api.post("/grades", data)
            
            if 'error' not in result:
                messagebox.showinfo("Success", "Grade added successfully")
                self.grade_student_code_entry.delete(0, 'end')
                self.subject_code_entry.delete(0, 'end')
                self.subject_name_entry.delete(0, 'end')
                self.grade_entry.delete(0, 'end')
                self.refresh_students()  # Refresh to update GWA
            else:
                messagebox.showerror("Error", f"Failed to add grade: {result['error']}")

        threading.Thread(target=add).start()

    def view_student_grades(self):
        """View grades for a specific student"""
        student_code = self.view_student_code_entry.get().strip()
        
        if not student_code:
            messagebox.showerror("Error", "Please enter student code")
            return

        def view():
            result = self.api.get(f"/grades/{student_code}")
            
            if 'error' not in result:
                self.update_grades_tree(result)
            else:
                messagebox.showerror("Error", f"Failed to load grades: {result['error']}")

        threading.Thread(target=view).start()

    def update_grades_tree(self, grades):
        """Update the grades treeview"""
        # Clear existing items
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)

        # Add grades to tree
        for grade in grades:
            self.grades_tree.insert("", "end", values=(
                grade['subject_code'],
                grade['subject_name'],
                grade['formatted_grade'],
                grade['description']
            ))

    def refresh_gwa_report(self):
        """Refresh GWA report"""
        def refresh():
            result = self.api.get("/gwa-report")
            
            if 'error' not in result:
                self.update_gwa_tree(result)
            else:
                messagebox.showerror("Error", f"Failed to load GWA report: {result['error']}")

        threading.Thread(target=refresh).start()

    def update_gwa_tree(self, students):
        """Update the GWA report treeview"""
        # Clear existing items
        for item in self.gwa_tree.get_children():
            self.gwa_tree.delete(item)

        # Add students to tree
        for student in students:
            self.gwa_tree.insert("", "end", values=(
                student['student_code'],
                student['name'],
                student['course_code'],
                student['formatted_gwa'],
                student['description']
            ))

    def get_grade_description(self, grade):
        """Get grade description"""
        if grade == 0:
            return "Not yet graded"
        elif grade == 1.0:
            return "Excellent"
        elif grade <= 1.75:
            return "Very Good"
        elif grade <= 2.5:
            return "Good"
        elif grade <= 3.0:
            return "Satisfactory"
        else:
            return "Failed"

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StudentManagementApp()
    app.run()