"""
EduCore Academic Management System - Modern GUI
Custom Tkinter Desktop Application
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import requests
from typing import List, Dict, Optional
import threading
import json

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class APIClient:
    """API Client for communicating with FastAPI backend"""
    
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.timeout = 10
    
    def get(self, endpoint):
        """Send GET request"""
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def post(self, endpoint, data):
        """Send POST request"""
        try:
            response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def put(self, endpoint, data):
        """Send PUT request"""
        try:
            response = requests.put(f"{self.base_url}{endpoint}", json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def delete(self, endpoint):
        """Send DELETE request"""
        try:
            response = requests.delete(f"{self.base_url}{endpoint}", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}


class ModernButton(ctk.CTkButton):
    """Custom styled button"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """Custom styled entry"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            **kwargs
        )


class EduCoreApp:
    """Main application class"""
    
    def __init__(self):
        self.api = APIClient()
        self.root = ctk.CTk()
        self.root.geometry("1400x850")
        self.root.title("EduCore - Academic Management System v2.0")
        self.root.minsize(1200, 700)
        
        # Initialize data storage
        self.students = []
        self.courses = []
        self.current_student_grades = []
        
        # Color scheme
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#14375e',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        }
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Header
        self.create_header()
        
        # Main content area
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create notebook with tabs
        self.create_tabview()
    
    def create_header(self):
        """Create application header"""
        header = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        # Title and subtitle
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=30, pady=15)
        
        title = ctk.CTkLabel(
            title_frame,
            text="🎓 EduCore",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Academic Management System - Student, Course & Grade Management",
            font=ctk.CTkFont(size=13),
            text_color="gray70"
        )
        subtitle.pack(anchor="w")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header,
            text="● Connected",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['success']
        )
        self.status_label.pack(side="right", padx=30)
    
    def create_tabview(self):
        """Create main tabview"""
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=10)
        self.tabview.pack(fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("👥 Students")
        self.tabview.add("📝 Grades")
        self.tabview.add("📊 Reports")
        self.tabview.add("📚 Courses")
        
        # Setup each tab
        self.create_students_tab()
        self.create_grades_tab()
        self.create_reports_tab()
        self.create_courses_tab()
    
    def create_students_tab(self):
        """Create students management tab"""
        tab = self.tabview.tab("👥 Students")
        
        # Left panel - Student form
        left_panel = ctk.CTkFrame(tab, width=400)
        left_panel.pack(side="left", fill="both", padx=(0, 10), pady=0)
        left_panel.pack_propagate(False)
        
        # Add Student Section
        add_section = ctk.CTkFrame(left_panel)
        add_section.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            add_section,
            text="➕ Add New Student",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 15))
        
        # Student Code
        ctk.CTkLabel(add_section, text="Student Code", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.student_code_entry = ModernEntry(
            add_section,
            placeholder_text="e.g., 24-49051"
        )
        self.student_code_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Name
        ctk.CTkLabel(add_section, text="Full Name", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.name_entry = ModernEntry(
            add_section,
            placeholder_text="Enter student full name"
        )
        self.name_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Course
        ctk.CTkLabel(add_section, text="Course", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.course_var = tk.StringVar(value="BSIT")
        self.course_dropdown = ctk.CTkComboBox(
            add_section,
            variable=self.course_var,
            values=["BSIT", "BSCS", "BSBA"],
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        self.course_dropdown.pack(fill="x", padx=10, pady=(5, 15))
        
        # Add Button
        ModernButton(
            add_section,
            text="Add Student",
            command=self.add_student,
            fg_color=self.colors['success'],
            hover_color="#27ae60",
            height=40
        ).pack(fill="x", padx=10, pady=(0, 15))
        
        # Update Course Section
        update_section = ctk.CTkFrame(left_panel)
        update_section.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            update_section,
            text="✏️ Update Student Course",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 15))
        
        ctk.CTkLabel(update_section, text="Student Code", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.update_code_entry = ModernEntry(
            update_section,
            placeholder_text="Enter student code"
        )
        self.update_code_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkLabel(update_section, text="New Course", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.update_course_var = tk.StringVar(value="BSIT")
        self.update_course_dropdown = ctk.CTkComboBox(
            update_section,
            variable=self.update_course_var,
            values=["BSIT", "BSCS", "BSBA"],
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        self.update_course_dropdown.pack(fill="x", padx=10, pady=(5, 15))
        
        ModernButton(
            update_section,
            text="Update Course",
            command=self.update_student_course,
            fg_color=self.colors['info'],
            hover_color="#2980b9",
            height=40
        ).pack(fill="x", padx=10, pady=(0, 15))
        
        # Right panel - Students list
        right_panel = ctk.CTkFrame(tab)
        right_panel.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Header with search and refresh
        header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text="Students List",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        ModernButton(
            header_frame,
            text="🔄 Refresh",
            command=self.refresh_students,
            width=120,
            height=35
        ).pack(side="right", padx=5)
        
        ModernButton(
            header_frame,
            text="🗑️ Delete",
            command=self.delete_student,
            fg_color=self.colors['danger'],
            hover_color="#c0392b",
            width=120,
            height=35
        ).pack(side="right")
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(right_panel)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Create Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#144870')])
        
        self.students_tree = ttk.Treeview(
            tree_frame,
            columns=("Code", "Name", "Course", "GWA", "Status"),
            show="headings",
            height=20
        )
        
        # Configure columns
        self.students_tree.heading("Code", text="Student Code")
        self.students_tree.heading("Name", text="Full Name")
        self.students_tree.heading("Course", text="Course")
        self.students_tree.heading("GWA", text="GWA")
        self.students_tree.heading("Status", text="Academic Status")
        
        self.students_tree.column("Code", width=120, anchor="center")
        self.students_tree.column("Name", width=250)
        self.students_tree.column("Course", width=100, anchor="center")
        self.students_tree.column("GWA", width=80, anchor="center")
        self.students_tree.column("Status", width=150, anchor="center")
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.students_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.students_tree.xview)
        self.students_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.students_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        vsb.grid(row=0, column=1, sticky="ns", pady=10)
        hsb.grid(row=1, column=0, sticky="ew", padx=(10, 0))
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_grades_tab(self):
        """Create grades management tab"""
        tab = self.tabview.tab("📝 Grades")
        
        # Left panel - Add grade form
        left_panel = ctk.CTkFrame(tab, width=400)
        left_panel.pack(side="left", fill="both", padx=(0, 10), pady=0)
        left_panel.pack_propagate(False)
        
        # Add Grade Section
        add_section = ctk.CTkFrame(left_panel)
        add_section.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            add_section,
            text="➕ Add/Update Grade",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 15))
        
        # Student Code
        ctk.CTkLabel(add_section, text="Student Code", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.grade_student_code_entry = ModernEntry(
            add_section,
            placeholder_text="e.g., 24-49051"
        )
        self.grade_student_code_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Subject Code
        ctk.CTkLabel(add_section, text="Subject Code", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.subject_code_entry = ModernEntry(
            add_section,
            placeholder_text="e.g., CS 131"
        )
        self.subject_code_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Subject Name
        ctk.CTkLabel(add_section, text="Subject Name", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.subject_name_entry = ModernEntry(
            add_section,
            placeholder_text="Enter subject name"
        )
        self.subject_name_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Grade
        ctk.CTkLabel(add_section, text="Grade (1.0 - 5.0)", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.grade_entry = ModernEntry(
            add_section,
            placeholder_text="e.g., 1.25"
        )
        self.grade_entry.pack(fill="x", padx=10, pady=(5, 15))
        
        # Grade Scale Info
        info_frame = ctk.CTkFrame(add_section, fg_color="#2b2b2b")
        info_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        grade_info = """
Grade Scale:
• 1.0 = Excellent (97-100%)
• 1.25-1.75 = Very Good (90-96%)
• 2.0-2.5 = Good (83-89%)
• 2.75-3.0 = Satisfactory (75-82%)
• 3.0+ = Failed
        """.strip()
        
        ctk.CTkLabel(
            info_frame,
            text=grade_info,
            font=ctk.CTkFont(size=10),
            justify="left",
            text_color="gray70"
        ).pack(padx=10, pady=10, anchor="w")
        
        # Add Button
        ModernButton(
            add_section,
            text="Submit Grade",
            command=self.add_grade,
            fg_color=self.colors['success'],
            hover_color="#27ae60",
            height=40
        ).pack(fill="x", padx=10, pady=(0, 15))
        
        # Right panel - View grades
        right_panel = ctk.CTkFrame(tab)
        right_panel.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Header
        header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text="Student Grades",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        # Search frame
        search_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(
            search_frame,
            text="Enter Student Code:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.view_student_code_entry = ModernEntry(
            search_frame,
            placeholder_text="Student Code",
            width=200
        )
        self.view_student_code_entry.pack(side="left", padx=(0, 10))
        
        ModernButton(
            search_frame,
            text="🔍 View Grades",
            command=self.view_student_grades,
            width=140,
            height=35
        ).pack(side="left")
        
        # Grades info frame
        self.grades_info_frame = ctk.CTkFrame(right_panel)
        self.grades_info_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.student_info_label = ctk.CTkLabel(
            self.grades_info_frame,
            text="Select a student to view grades",
            font=ctk.CTkFont(size=13),
            text_color="gray70"
        )
        self.student_info_label.pack(pady=10)
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(right_panel)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.grades_tree = ttk.Treeview(
            tree_frame,
            columns=("Subject Code", "Subject Name", "Grade", "Status"),
            show="headings",
            height=15
        )
        
        self.grades_tree.heading("Subject Code", text="Subject Code")
        self.grades_tree.heading("Subject Name", text="Subject Name")
        self.grades_tree.heading("Grade", text="Grade")
        self.grades_tree.heading("Status", text="Status")
        
        self.grades_tree.column("Subject Code", width=120, anchor="center")
        self.grades_tree.column("Subject Name", width=350)
        self.grades_tree.column("Grade", width=100, anchor="center")
        self.grades_tree.column("Status", width=150, anchor="center")
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.grades_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.grades_tree.xview)
        self.grades_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.grades_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        vsb.grid(row=0, column=1, sticky="ns", pady=10)
        hsb.grid(row=1, column=0, sticky="ew", padx=(10, 0))
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_reports_tab(self):
        """Create reports tab"""
        tab = self.tabview.tab("📊 Reports")
        
        # Header
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text="General Weighted Average (GWA) Report",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        ModernButton(
            header_frame,
            text="🔄 Refresh Report",
            command=self.refresh_gwa_report,
            width=150,
            height=35
        ).pack(side="right")
        
        # Statistics frame
        stats_frame = ctk.CTkFrame(tab)
        stats_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Statistics boxes
        stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=10, pady=10)
        
        self.total_students_label = self.create_stat_box(
            stats_container, "Total Students", "0", self.colors['info']
        )
        self.total_students_label.pack(side="left", expand=True, fill="x", padx=5)
        
        self.avg_gwa_label = self.create_stat_box(
            stats_container, "Average GWA", "0.00", self.colors['success']
        )
        self.avg_gwa_label.pack(side="left", expand=True, fill="x", padx=5)
        
        self.excellent_label = self.create_stat_box(
            stats_container, "Excellent (≤1.75)", "0", self.colors['warning']
        )
        self.excellent_label.pack(side="left", expand=True, fill="x", padx=5)
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(tab)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.gwa_tree = ttk.Treeview(
            tree_frame,
            columns=("Code", "Name", "Course", "GWA", "Status"),
            show="headings",
            height=20
        )
        
        self.gwa_tree.heading("Code", text="Student Code")
        self.gwa_tree.heading("Name", text="Full Name")
        self.gwa_tree.heading("Course", text="Course")
        self.gwa_tree.heading("GWA", text="GWA")
        self.gwa_tree.heading("Status", text="Academic Status")
        
        self.gwa_tree.column("Code", width=120, anchor="center")
        self.gwa_tree.column("Name", width=250)
        self.gwa_tree.column("Course", width=100, anchor="center")
        self.gwa_tree.column("GWA", width=100, anchor="center")
        self.gwa_tree.column("Status", width=150, anchor="center")
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.gwa_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.gwa_tree.xview)
        self.gwa_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.gwa_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        vsb.grid(row=0, column=1, sticky="ns", pady=10)
        hsb.grid(row=1, column=0, sticky="ew", padx=(10, 0))
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_courses_tab(self):
        """Create courses reference tab"""
        tab = self.tabview.tab("📚 Courses")
        
        # Header
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text="Available Courses & Subjects",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        ModernButton(
            header_frame,
            text="🔄 Refresh",
            command=self.load_courses,
            width=120,
            height=35
        ).pack(side="right")
        
        # Scrollable frame for courses
        self.courses_scroll = ctk.CTkScrollableFrame(tab)
        self.courses_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def create_stat_box(self, parent, title, value, color):
        """Create a statistics box"""
        box = ctk.CTkFrame(parent, fg_color=color)
        
        ctk.CTkLabel(
            box,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            box,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        value_label.pack(pady=(0, 15))
        
        # Store reference to update later
        box.value_label = value_label
        return box
    
    # ==================== Data Loading Methods ====================
    
    def load_initial_data(self):
        """Load all initial data"""
        threading.Thread(target=self._load_initial_data, daemon=True).start()
    
    def _load_initial_data(self):
        """Background thread for loading initial data"""
        self.load_courses()
        self.refresh_students()
        self.refresh_gwa_report()
    
    def load_courses(self):
        """Load courses from API"""
        def load():
            result = self.api.get("/courses")
            if 'error' not in result:
                self.courses = result
                self.root.after(0, self.update_course_dropdowns)
                self.root.after(0, self.display_courses)
            else:
                self.root.after(0, lambda: self.show_error("Failed to load courses", result['error']))
        
        threading.Thread(target=load, daemon=True).start()
    
    def update_course_dropdowns(self):
        """Update course dropdown menus"""
        if self.courses:
            course_codes = [course['code'] for course in self.courses]
            self.course_dropdown.configure(values=course_codes)
            self.update_course_dropdown.configure(values=course_codes)
    
    def display_courses(self):
        """Display courses and their subjects"""
        # Clear existing widgets
        for widget in self.courses_scroll.winfo_children():
            widget.destroy()
        
        for course in self.courses:
            # Course frame
            course_frame = ctk.CTkFrame(self.courses_scroll)
            course_frame.pack(fill="x", pady=10, padx=10)
            
            # Course header
            header = ctk.CTkFrame(course_frame, fg_color=self.colors['primary'])
            header.pack(fill="x", padx=0, pady=0)
            
            ctk.CTkLabel(
                header,
                text=f"{course['code']} - {course['name']}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="white"
            ).pack(pady=15, padx=20, anchor="w")
            
            # Subjects list
            if course.get('subjects'):
                subjects_frame = ctk.CTkFrame(course_frame, fg_color="transparent")
                subjects_frame.pack(fill="x", padx=20, pady=15)
                
                ctk.CTkLabel(
                    subjects_frame,
                    text="Subjects:",
                    font=ctk.CTkFont(size=13, weight="bold")
                ).pack(anchor="w", pady=(0, 10))
                
                for subject in course['subjects']:
                    subject_item = ctk.CTkFrame(subjects_frame, fg_color="#2b2b2b")
                    subject_item.pack(fill="x", pady=2)
                    
                    ctk.CTkLabel(
                        subject_item,
                        text=f"• {subject['subject_code']} - {subject['subject_name']}",
                        font=ctk.CTkFont(size=12),
                        anchor="w"
                    ).pack(pady=8, padx=15, anchor="w")
            else:
                ctk.CTkLabel(
                    course_frame,
                    text="No subjects defined",
                    font=ctk.CTkFont(size=12),
                    text_color="gray70"
                ).pack(pady=10)
    
    def refresh_students(self):
        """Refresh students list"""
        def refresh():
            result = self.api.get("/students")
            if 'error' not in result:
                self.students = result
                self.root.after(0, self.update_students_tree)
            else:
                self.root.after(0, lambda: self.show_error("Failed to load students", result['error']))
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def update_students_tree(self):
        """Update the students treeview"""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Add students to tree
        for student in self.students:
            gwa = student.get('gwa', 0)
            formatted_gwa = f"{gwa:.2f}" if gwa > 0 else "N/A"
            status = self.get_grade_description(gwa)
            
            # Color coding based on GWA
            self.students_tree.insert("", "end", values=(
                student['student_code'],
                student['name'],
                student['course_code'],
                formatted_gwa,
                status
            ))
    
    # ==================== Student Management Methods ====================
    
    def add_student(self):
        """Add a new student"""
        student_code = self.student_code_entry.get().strip()
        name = self.name_entry.get().strip()
        course = self.course_var.get()
        
        if not all([student_code, name, course]):
            self.show_error("Validation Error", "Please fill in all fields")
            return
        
        def add():
            data = {
                'student_code': student_code,
                'name': name,
                'course_code': course
            }
            result = self.api.post("/students", data)
            
            if 'error' not in result:
                self.root.after(0, lambda: self.show_success("Student added successfully"))
                self.root.after(0, self.clear_student_form)
                self.root.after(0, self.refresh_students)
            else:
                self.root.after(0, lambda: self.show_error("Failed to add student", result['error']))
        
        threading.Thread(target=add, daemon=True).start()
    
    def delete_student(self):
        """Delete selected student"""
        selection = self.students_tree.selection()
        if not selection:
            self.show_error("Selection Error", "Please select a student to delete")
            return
        
        item = self.students_tree.item(selection[0])
        student_code = item['values'][0]
        student_name = item['values'][1]
        
        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n{student_name} ({student_code})?\n\nThis will also delete all their grades."
        ):
            return
        
        def delete():
            result = self.api.delete(f"/students/{student_code}")
            
            if 'error' not in result:
                self.root.after(0, lambda: self.show_success("Student deleted successfully"))
                self.root.after(0, self.refresh_students)
            else:
                self.root.after(0, lambda: self.show_error("Failed to delete student", result['error']))
        
        threading.Thread(target=delete, daemon=True).start()
    
    def update_student_course(self):
        """Update student's course"""
        student_code = self.update_code_entry.get().strip()
        new_course = self.update_course_var.get()
        
        if not student_code:
            self.show_error("Validation Error", "Please enter student code")
            return
        
        def update():
            data = {'course_code': new_course}
            result = self.api.put(f"/students/{student_code}", data)
            
            if 'error' not in result:
                self.root.after(0, lambda: self.show_success("Student course updated successfully"))
                self.root.after(0, lambda: self.update_code_entry.delete(0, 'end'))
                self.root.after(0, self.refresh_students)
            else:
                self.root.after(0, lambda: self.show_error("Failed to update student", result['error']))
        
        threading.Thread(target=update, daemon=True).start()
    
    # ==================== Grade Management Methods ====================
    
    def add_grade(self):
        """Add a grade for a student"""
        student_code = self.grade_student_code_entry.get().strip()
        subject_code = self.subject_code_entry.get().strip()
        subject_name = self.subject_name_entry.get().strip()
        grade_str = self.grade_entry.get().strip()
        
        if not all([student_code, subject_code, subject_name, grade_str]):
            self.show_error("Validation Error", "Please fill in all fields")
            return
        
        try:
            grade = float(grade_str)
            if grade < 1.0 or grade > 5.0:
                self.show_error("Validation Error", "Grade must be between 1.0 and 5.0")
                return
        except ValueError:
            self.show_error("Validation Error", "Invalid grade format. Use decimal format (e.g., 1.25)")
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
                self.root.after(0, lambda: self.show_success("Grade added successfully"))
                self.root.after(0, self.clear_grade_form)
                self.root.after(0, self.refresh_students)
            else:
                self.root.after(0, lambda: self.show_error("Failed to add grade", result['error']))
        
        threading.Thread(target=add, daemon=True).start()
    
    def view_student_grades(self):
        """View grades for a specific student"""
        student_code = self.view_student_code_entry.get().strip()
        
        if not student_code:
            self.show_error("Validation Error", "Please enter student code")
            return
        
        def view():
            result = self.api.get(f"/grades/{student_code}")
            
            if 'error' not in result:
                # Also get student info
                student_result = self.api.get(f"/students/{student_code}")
                if 'error' not in student_result:
                    self.root.after(0, lambda: self.update_grades_display(result, student_result))
                else:
                    self.root.after(0, lambda: self.update_grades_tree(result))
            else:
                self.root.after(0, lambda: self.show_error("Failed to load grades", result['error']))
        
        threading.Thread(target=view, daemon=True).start()
    
    def update_grades_display(self, grades, student_info):
        """Update grades display with student info"""
        # Update info label
        gwa = student_info.get('gwa', 0)
        info_text = f"Student: {student_info['name']} ({student_info['student_code']}) | Course: {student_info['course_code']} | GWA: {gwa:.2f if gwa > 0 else 'N/A'}"
        self.student_info_label.configure(text=info_text, text_color="white")
        
        # Update tree
        self.update_grades_tree(grades)
    
    def update_grades_tree(self, grades):
        """Update the grades treeview"""
        # Clear existing items
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        if not grades:
            # Show message if no grades
            return
        
        # Add grades to tree
        for grade in grades:
            self.grades_tree.insert("", "end", values=(
                grade['subject_code'],
                grade['subject_name'],
                grade['formatted_grade'],
                grade['description']
            ))
    
    # ==================== Report Methods ====================
    
    def refresh_gwa_report(self):
        """Refresh GWA report"""
        def refresh():
            result = self.api.get("/gwa-report")
            
            if 'error' not in result:
                self.root.after(0, lambda: self.update_gwa_report(result))
            else:
                self.root.after(0, lambda: self.show_error("Failed to load GWA report", result['error']))
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def update_gwa_report(self, students):
        """Update the GWA report treeview and statistics"""
        # Clear existing items
        for item in self.gwa_tree.get_children():
            self.gwa_tree.delete(item)
        
        # Calculate statistics
        total_students = len(students)
        total_gwa = sum(s['gwa'] for s in students if s['gwa'] > 0)
        students_with_gwa = len([s for s in students if s['gwa'] > 0])
        avg_gwa = total_gwa / students_with_gwa if students_with_gwa > 0 else 0
        excellent_count = len([s for s in students if 0 < s['gwa'] <= 1.75])
        
        # Update statistics boxes
        self.total_students_label.value_label.configure(text=str(total_students))
        self.avg_gwa_label.value_label.configure(text=f"{avg_gwa:.2f}" if avg_gwa > 0 else "N/A")
        self.excellent_label.value_label.configure(text=str(excellent_count))
        
        # Add students to tree
        for student in students:
            self.gwa_tree.insert("", "end", values=(
                student['student_code'],
                student['name'],
                student['course_code'],
                student['formatted_gwa'],
                student['description']
            ))
    
    # ==================== Helper Methods ====================
    
    def get_grade_description(self, grade: float) -> str:
        """Get description for a grade"""
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
    
    def clear_student_form(self):
        """Clear student form fields"""
        self.student_code_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
    
    def clear_grade_form(self):
        """Clear grade form fields"""
        self.grade_student_code_entry.delete(0, 'end')
        self.subject_code_entry.delete(0, 'end')
        self.subject_name_entry.delete(0, 'end')
        self.grade_entry.delete(0, 'end')
    
    def show_success(self, message):
        """Show success message"""
        messagebox.showinfo("Success", message)
    
    def show_error(self, title, message):
        """Show error message"""
        messagebox.showerror(title, message)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    print("=================================================")
    print("  EduCore Academic Management System v2.0")
    print("=================================================")
    print("Starting GUI application...")
    print("Make sure the FastAPI backend is running on port 8000")
    print("=================================================\n")
    
    app = EduCoreApp()
    app.run()


if __name__ == "__main__":
    main()
