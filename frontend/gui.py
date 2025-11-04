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
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import io

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
            'primary_dark': '#14375e',
            'secondary': '#14375e',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db',
            'border': '#3a3a3a'
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
        self.tabview.add("Students")
        self.tabview.add("Grades")
        self.tabview.add("Reports")
        self.tabview.add("Analytics")
        self.tabview.add("Courses")
        
        # Setup each tab
        self.create_students_tab()
        self.create_grades_tab()
        self.create_reports_tab()
        self.create_analytics_tab()
        self.create_courses_tab()
    
    def create_students_tab(self):
        """Create students management tab"""
        tab = self.tabview.tab("Students")
        
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
        tab = self.tabview.tab("Grades")
        
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
        student_code_label_frame = ctk.CTkFrame(add_section, fg_color="transparent")
        student_code_label_frame.pack(fill="x", padx=10, anchor="w")
        ctk.CTkLabel(student_code_label_frame, text="Student Code", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(student_code_label_frame, text="(Press Enter to load subjects)", 
                    font=ctk.CTkFont(size=9), text_color="gray60").pack(side="left", padx=(5, 0))
        
        self.grade_student_code_entry = ModernEntry(
            add_section,
            placeholder_text="e.g., 24-49051"
        )
        self.grade_student_code_entry.pack(fill="x", padx=10, pady=(5, 10))
        self.grade_student_code_entry.bind("<Return>", lambda e: self.load_subjects_for_student())
        
        # Subject Code (with autocomplete dropdown)
        subject_label_frame = ctk.CTkFrame(add_section, fg_color="transparent")
        subject_label_frame.pack(fill="x", padx=10, anchor="w")
        ctk.CTkLabel(subject_label_frame, text="Subject Code", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(subject_label_frame, text="(Select from dropdown)", 
                    font=ctk.CTkFont(size=9), text_color="gray60").pack(side="left", padx=(5, 0))
        
        self.subject_code_combobox = ctk.CTkComboBox(
            add_section,
            values=["Enter student code first..."],
            command=self.on_subject_selected,
            state="readonly",
            font=ctk.CTkFont(size=12),
            dropdown_font=ctk.CTkFont(size=11),
            height=35,
            button_color=self.colors['primary'],
            button_hover_color=self.colors['primary_dark'],
            border_color=self.colors['border']
        )
        self.subject_code_combobox.pack(fill="x", padx=10, pady=(5, 10))
        self.subject_code_combobox.set("Select a subject code...")
        
        # Store subject data for auto-fill
        self.subjects_data = {}
        
        # Subject Name (auto-filled, read-only)
        ctk.CTkLabel(add_section, text="Subject Name", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.subject_name_entry = ModernEntry(
            add_section,
            placeholder_text="Auto-filled when subject is selected"
        )
        self.subject_name_entry.pack(fill="x", padx=10, pady=(5, 10))
        self.subject_name_entry.configure(state="disabled")  # Make it read-only
        
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
        tab = self.tabview.tab("Reports")
        
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
    
    def create_analytics_tab(self):
        """Create analytics dashboard tab with charts"""
        tab = self.tabview.tab("Analytics")
        
        # Header
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text="Analytics Dashboard",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        ModernButton(
            header_frame,
            text="🔄 Refresh Analytics",
            command=self.refresh_analytics,
            width=160,
            height=35
        ).pack(side="right")
        
        # Create canvas with scrollbar for better performance
        canvas_frame = ctk.CTkFrame(tab)
        canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Create canvas and scrollbar
        self.analytics_canvas = tk.Canvas(canvas_frame, bg="#2b2b2b", highlightthickness=0)
        analytics_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.analytics_canvas.yview)
        
        # Create frame inside canvas
        self.analytics_content = ctk.CTkFrame(self.analytics_canvas, fg_color="transparent")
        
        # Configure canvas
        self.analytics_canvas.configure(yscrollcommand=analytics_scrollbar.set)
        
        # Pack scrollbar and canvas
        analytics_scrollbar.pack(side="right", fill="y")
        self.analytics_canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.analytics_window = self.analytics_canvas.create_window((0, 0), window=self.analytics_content, anchor="nw")
        
        # Bind configuration events
        self.analytics_content.bind("<Configure>", lambda e: self.analytics_canvas.configure(scrollregion=self.analytics_canvas.bbox("all")))
        self.analytics_canvas.bind("<Configure>", lambda e: self.analytics_canvas.itemconfig(self.analytics_window, width=e.width))
        
        # Bind mouse wheel for smooth scrolling
        def _on_mousewheel(event):
            self.analytics_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.analytics_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Statistics Overview
        stats_frame = ctk.CTkFrame(self.analytics_content)
        stats_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 Overview Statistics",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=10, pady=(0, 15))
        
        # Create stat boxes
        self.analytics_students_label = self.create_stat_box(
            stats_container, "Total Students", "0", self.colors['info']
        )
        self.analytics_students_label.pack(side="left", expand=True, fill="x", padx=5)
        
        self.analytics_courses_label = self.create_stat_box(
            stats_container, "Total Courses", "0", self.colors['primary']
        )
        self.analytics_courses_label.pack(side="left", expand=True, fill="x", padx=5)
        
        self.analytics_grades_label = self.create_stat_box(
            stats_container, "Total Grades", "0", self.colors['warning']
        )
        self.analytics_grades_label.pack(side="left", expand=True, fill="x", padx=5)
        
        self.analytics_avg_gwa_label = self.create_stat_box(
            stats_container, "Overall Avg GWA", "0.00", self.colors['success']
        )
        self.analytics_avg_gwa_label.pack(side="left", expand=True, fill="x", padx=5)
        
        # Charts container
        charts_frame = ctk.CTkFrame(self.analytics_content)
        charts_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Top row - 2 charts
        top_row = ctk.CTkFrame(charts_frame, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=10)
        
        # Course Distribution Chart (left)
        course_chart_frame = ctk.CTkFrame(top_row, width=400, height=300)
        course_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        course_chart_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            course_chart_frame,
            text="Students per Course",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.course_chart_label = ctk.CTkLabel(course_chart_frame, text="")
        self.course_chart_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grade Distribution Chart (right)
        grade_chart_frame = ctk.CTkFrame(top_row, width=400, height=300)
        grade_chart_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))
        grade_chart_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            grade_chart_frame,
            text="Grade Distribution",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.grade_chart_label = ctk.CTkLabel(grade_chart_frame, text="")
        self.grade_chart_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bottom row - Course Performance Chart
        bottom_row = ctk.CTkFrame(charts_frame, fg_color="transparent")
        bottom_row.pack(fill="x", padx=10, pady=(5, 10))
        
        performance_chart_frame = ctk.CTkFrame(bottom_row, height=300)
        performance_chart_frame.pack(fill="both", expand=True)
        performance_chart_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            performance_chart_frame,
            text="Average GWA per Course",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.performance_chart_label = ctk.CTkLabel(performance_chart_frame, text="")
        self.performance_chart_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top Performers List
        top_performers_frame = ctk.CTkFrame(self.analytics_content)
        top_performers_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            top_performers_frame,
            text="🏆 Top 10 Performers (GWA ≤ 1.75)",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Treeview for top performers
        tree_container = ctk.CTkFrame(top_performers_frame)
        tree_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.top_performers_tree = ttk.Treeview(
            tree_container,
            columns=("Rank", "Code", "Name", "Course", "GWA"),
            show="headings",
            height=10
        )
        
        self.top_performers_tree.heading("Rank", text="Rank")
        self.top_performers_tree.heading("Code", text="Student Code")
        self.top_performers_tree.heading("Name", text="Full Name")
        self.top_performers_tree.heading("Course", text="Course")
        self.top_performers_tree.heading("GWA", text="GWA")
        
        self.top_performers_tree.column("Rank", width=60, anchor="center")
        self.top_performers_tree.column("Code", width=120, anchor="center")
        self.top_performers_tree.column("Name", width=300)
        self.top_performers_tree.column("Course", width=100, anchor="center")
        self.top_performers_tree.column("GWA", width=100, anchor="center")
        
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.top_performers_tree.yview)
        self.top_performers_tree.configure(yscrollcommand=vsb.set)
        
        self.top_performers_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        vsb.pack(side="right", fill="y", pady=10)
    
    def create_courses_tab(self):
        """Create courses reference tab"""
        tab = self.tabview.tab("Courses")
        
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
        subject_code = self.subject_code_combobox.get().strip()
        
        # Check if a valid subject is selected
        if subject_code in ["Enter student code first...", "Select a subject code...", "No subjects available"]:
            self.show_error("Validation Error", "Please select a valid subject code")
            return
        
        # Get subject name from stored data
        subject_name = self.subjects_data.get(subject_code, "")
        
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
        gwa_display = f"{gwa:.2f}" if gwa > 0 else "N/A"
        info_text = f"Student: {student_info['name']} ({student_info['student_code']}) | Course: {student_info['course_code']} | GWA: {gwa_display}"
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
    
    def refresh_analytics(self):
        """Refresh analytics dashboard"""
        def refresh():
            result = self.api.get("/analytics/overview")
            
            if 'error' not in result:
                self.root.after(0, lambda: self.update_analytics_dashboard(result))
            else:
                self.root.after(0, lambda: self.show_error("Failed to load analytics", result['error']))
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def update_analytics_dashboard(self, data):
        """Update analytics dashboard with data and charts"""
        # Update statistics
        self.analytics_students_label.value_label.configure(text=str(data['total_students']))
        self.analytics_courses_label.value_label.configure(text=str(data['total_courses']))
        self.analytics_grades_label.value_label.configure(text=str(data['total_grades']))
        self.analytics_avg_gwa_label.value_label.configure(
            text=f"{data['overall_avg_gwa']:.2f}" if data['overall_avg_gwa'] > 0 else "N/A"
        )
        
        # Generate and display charts
        self.generate_course_distribution_chart(data['course_distribution'])
        self.generate_grade_distribution_chart(data['grade_distribution'])
        self.generate_course_performance_chart(data['course_performance'])
        
        # Update top performers
        self.update_top_performers(data['top_students'])
    
    def generate_course_distribution_chart(self, course_data):
        """Generate pie chart for students per course"""
        if not course_data:
            return
        
        # Set dark theme for matplotlib
        plt.style.use('dark_background')
        
        fig, ax = plt.subplots(figsize=(5, 3.5), facecolor='#2b2b2b', dpi=80)
        ax.set_facecolor('#2b2b2b')
        
        courses = [item['course'] for item in course_data]
        counts = [item['count'] for item in course_data]
        
        colors = ['#1f538d', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        
        ax.pie(counts, labels=courses, autopct='%1.1f%%', startangle=90, colors=colors[:len(courses)])
        ax.axis('equal')
        
        # Convert to image
        self.display_chart(fig, self.course_chart_label)
    
    def generate_grade_distribution_chart(self, grade_data):
        """Generate bar chart for grade distribution"""
        if not grade_data:
            return
        
        plt.style.use('dark_background')
        
        fig, ax = plt.subplots(figsize=(5, 3.5), facecolor='#2b2b2b', dpi=80)
        ax.set_facecolor('#2b2b2b')
        
        ranges = [item['range'] for item in grade_data]
        counts = [item['count'] for item in grade_data]
        
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e67e22', '#e74c3c']
        
        bars = ax.bar(range(len(ranges)), counts, color=colors)
        ax.set_xticks(range(len(ranges)))
        ax.set_xticklabels([r.split(' (')[0] for r in ranges], rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Number of Grades', fontsize=9)
        ax.set_title('Grade Distribution', fontsize=10)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        self.display_chart(fig, self.grade_chart_label)
    
    def generate_course_performance_chart(self, performance_data):
        """Generate bar chart for average GWA per course"""
        if not performance_data:
            return
        
        plt.style.use('dark_background')
        
        fig, ax = plt.subplots(figsize=(7, 3.5), facecolor='#2b2b2b', dpi=80)
        ax.set_facecolor('#2b2b2b')
        
        courses = [item['course'] for item in performance_data]
        avg_gwas = [item['avg_gwa'] for item in performance_data]
        
        colors = ['#2ecc71' if gwa <= 1.75 else '#3498db' if gwa <= 2.5 else '#f39c12' 
                  for gwa in avg_gwas]
        
        bars = ax.bar(courses, avg_gwas, color=colors)
        ax.set_ylabel('Average GWA', fontsize=9)
        ax.set_title('Average GWA per Course', fontsize=10)
        ax.set_ylim(0, max(avg_gwas) + 0.5 if avg_gwas else 5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=8)
        
        # Add reference lines
        ax.axhline(y=1.75, color='#2ecc71', linestyle='--', alpha=0.5, label='Excellent')
        ax.axhline(y=2.5, color='#3498db', linestyle='--', alpha=0.5, label='Good')
        ax.axhline(y=3.0, color='#f39c12', linestyle='--', alpha=0.5, label='Satisfactory')
        ax.legend(fontsize=8)
        
        plt.tight_layout()
        self.display_chart(fig, self.performance_chart_label)
    
    def display_chart(self, fig, label_widget):
        """Convert matplotlib figure to image and display in label"""
        # Save figure to bytes buffer with optimized DPI for performance
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=80, facecolor='#2b2b2b', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        # Convert to PhotoImage
        image = Image.open(buf)
        # Resize for better fit if needed
        photo = ImageTk.PhotoImage(image)
        
        # Update label
        label_widget.configure(image=photo, text="")
        label_widget.image = photo  # Keep a reference to prevent garbage collection
        buf.close()  # Clean up buffer
    
    def update_top_performers(self, top_students):
        """Update top performers treeview"""
        # Clear existing items
        for item in self.top_performers_tree.get_children():
            self.top_performers_tree.delete(item)
        
        # Add top students
        for rank, student in enumerate(top_students, 1):
            self.top_performers_tree.insert("", "end", values=(
                f"#{rank}",
                student['student_code'],
                student['name'],
                student['course_code'],
                f"{student['gwa']:.2f}"
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
    
    def load_subjects_for_student(self):
        """Load subjects based on student's course"""
        student_code = self.grade_student_code_entry.get().strip()
        
        if not student_code:
            self.show_error("Validation Error", "Please enter a student code")
            return
        
        def load():
            # Get student info to find their course
            student_result = self.api.get(f"/students/{student_code}")
            
            if 'error' in student_result:
                self.root.after(0, lambda: self.show_error("Student Not Found", 
                    "Could not find student with that code. Please check and try again."))
                self.root.after(0, lambda: self.subject_code_combobox.configure(values=["Student not found"]))
                self.root.after(0, lambda: self.subject_code_combobox.set("Student not found"))
                return
            
            course_code = student_result.get('course_code')
            
            # Get subjects for this course
            subjects_result = self.api.get(f"/courses/{course_code}/subjects")
            
            if 'error' in subjects_result or not subjects_result:
                self.root.after(0, lambda: self.show_error("No Subjects", 
                    f"No subjects found for course {course_code}"))
                self.root.after(0, lambda: self.subject_code_combobox.configure(values=["No subjects available"]))
                self.root.after(0, lambda: self.subject_code_combobox.set("No subjects available"))
                return
            
            # Store subject data and prepare dropdown values
            self.subjects_data = {}
            subject_codes = []
            for subject in subjects_result:
                subject_code = subject['subject_code']
                subject_name = subject['subject_name']
                self.subjects_data[subject_code] = subject_name
                subject_codes.append(subject_code)
            
            # Update combobox
            self.root.after(0, lambda: self.subject_code_combobox.configure(values=subject_codes))
            self.root.after(0, lambda: self.subject_code_combobox.set("Select a subject code..."))
            self.root.after(0, lambda: self.show_success(f"Loaded {len(subject_codes)} subjects for {course_code}"))
        
        threading.Thread(target=load, daemon=True).start()
    
    def on_subject_selected(self, selected_code):
        """Handle subject code selection - auto-fill subject name"""
        if selected_code in self.subjects_data:
            subject_name = self.subjects_data[selected_code]
            # Temporarily enable the entry to update it
            self.subject_name_entry.configure(state="normal")
            self.subject_name_entry.delete(0, 'end')
            self.subject_name_entry.insert(0, subject_name)
            self.subject_name_entry.configure(state="disabled")
    
    def clear_grade_form(self):
        """Clear grade form fields"""
        self.grade_student_code_entry.delete(0, 'end')
        self.subject_code_combobox.set("Select a subject code...")
        self.subject_name_entry.configure(state="normal")
        self.subject_name_entry.delete(0, 'end')
        self.subject_name_entry.configure(state="disabled")
        self.grade_entry.delete(0, 'end')
        self.subjects_data = {}
    
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

