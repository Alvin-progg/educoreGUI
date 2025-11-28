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
import qrcode
import cv2
from pyzbar.pyzbar import decode
import os
import numpy as np

# Configure CustomTkinter appearance
ctk.set_appearance_mode("light")
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
    """Custom styled button with modern design"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            border_width=0,
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """Custom styled entry with modern design"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=2,
            border_color="#e5e7eb",
            **kwargs
        )


class RoleSelectionWindow:
    """Role selection window - Teacher or Student"""
    
    def __init__(self):
        self.selected_role = None
        
        # Create role selection window
        self.window = ctk.CTk()
        self.window.geometry("600x650")
        self.window.title("EduCore - Welcome")
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_role_selection_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_role_selection_ui(self):
        """Create role selection interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color=("#6366f1", "#6366f1"), corner_radius=20)
        header_frame.pack(fill="x", pady=(0, 40))
        
        ctk.CTkLabel(
            header_frame,
            text="🎓",
            font=ctk.CTkFont(size=60)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="EduCore System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack()
        
        ctk.CTkLabel(
            header_frame,
            text="Academic Management System",
            font=ctk.CTkFont(size=14),
            text_color="#e0e7ff"
        ).pack(pady=(5, 20))
        
        # Selection frame
        selection_frame = ctk.CTkFrame(main_frame)
        selection_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            selection_frame,
            text="Who are you?",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(30, 40))
        
        # Teacher button
        teacher_btn = ctk.CTkButton(
            selection_frame,
            text="👨‍🏫 Teacher / Admin",
            command=lambda: self.select_role("teacher"),
            height=80,
            corner_radius=15,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5"
        )
        teacher_btn.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            selection_frame,
            text="Access management features and administrative tools",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280"
        ).pack(pady=(0, 20))
        
        # Student button
        student_btn = ctk.CTkButton(
            selection_frame,
            text="👨‍🎓 Student",
            command=lambda: self.select_role("student"),
            height=80,
            corner_radius=15,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669"
        )
        student_btn.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            selection_frame,
            text="View your grades, reports, and academic performance",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280"
        ).pack(pady=(0, 30))
        
    def select_role(self, role):
        """Handle role selection"""
        self.selected_role = role
        self.window.destroy()
        
    def run(self):
        """Run the role selection window"""
        self.window.mainloop()
        return self.selected_role


class LoginWindow:
    """Login window for authentication"""
    
    def __init__(self, api_client):
        self.api = api_client
        self.login_successful = False
        self.user_data = None
        
        # Create login window
        self.window = ctk.CTk()
        self.window.geometry("550x800")
        self.window.title("EduCore - Teacher Login")
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_login_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_login_ui(self):
        """Create the login interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo/Title section
        title_frame = ctk.CTkFrame(main_frame, fg_color=("#6366f1", "#6366f1"), corner_radius=20)
        title_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            title_frame,
            text="🎓",
            font=ctk.CTkFont(size=60)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="EduCore System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="Academic Management System",
            font=ctk.CTkFont(size=14),
            text_color="#e0e7ff"
        ).pack(pady=(0, 20))
        
        # Login form
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(
            form_frame,
            text="Sign In",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 30))
        
        # Username
        ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=40)
        
        self.username_entry = ModernEntry(
            form_frame,
            placeholder_text="Enter your username",
            height=40
        )
        self.username_entry.pack(fill="x", padx=40, pady=(5, 20))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Password
        ctk.CTkLabel(
            form_frame,
            text="Password",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=40)
        
        self.password_entry = ModernEntry(
            form_frame,
            placeholder_text="Enter your password",
            show="•",
            height=40
        )
        self.password_entry.pack(fill="x", padx=40, pady=(5, 10))
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar(value=False)
        show_password_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            font=ctk.CTkFont(size=11)
        )
        show_password_checkbox.pack(anchor="w", padx=40, pady=(0, 20))
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.error_label.pack(pady=(0, 10))
        
        # Login button
        self.login_button = ctk.CTkButton(
            form_frame,
            text="Login",
            command=self.login,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5"
        )
        self.login_button.pack(fill="x", padx=40, pady=(10, 20))
        
        # Focus on username
        self.username_entry.focus()
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")
            

            
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Disable login button
        self.login_button.configure(state="disabled", text="Logging in...")
        self.error_label.configure(text="")
        
        def do_login():
            data = {
                "username": username,
                "password": password
            }
            result = self.api.post("/auth/login", data)
            
            if 'error' in result:
                self.window.after(0, lambda: self.show_error(f"Connection error: {result['error']}"))
                self.window.after(0, lambda: self.login_button.configure(state="normal", text="Login"))
            elif result.get('success'):
                self.user_data = result.get('user')
                self.login_successful = True
                self.window.after(0, self.window.destroy)
            else:
                self.window.after(0, lambda: self.show_error(result.get('message', 'Login failed')))
                self.window.after(0, lambda: self.login_button.configure(state="normal", text="Login"))
        
        threading.Thread(target=do_login, daemon=True).start()
        
    def show_error(self, message):
        """Show error message"""
        self.error_label.configure(text=message)
        
    def run(self):
        """Run the login window"""
        self.window.mainloop()
        return self.login_successful, self.user_data


class MenuWindow:
    """Navigation menu window shown after login"""
    
    def __init__(self, user_data, api_client):
        self.user_data = user_data
        self.api = api_client
        self.selected_feature = None
        
        # Create menu window
        self.window = ctk.CTk()
        self.window.geometry("700x650")
        self.window.title("EduCore - Main Menu")
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_menu_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_menu_ui(self):
        """Create the menu interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header section
        header_frame = ctk.CTkFrame(main_frame, fg_color=("#6366f1", "#6366f1"), corner_radius=20)
        header_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            header_frame,
            text="🎓",
            font=ctk.CTkFont(size=50)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="EduCore System",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="white"
        ).pack()
        
        user_name = self.user_data.get('full_name', 'User')
        ctk.CTkLabel(
            header_frame,
            text=f"Welcome, {user_name}!",
            font=ctk.CTkFont(size=14),
            text_color="#e0e7ff"
        ).pack(pady=(5, 20))
        
        # Menu options frame
        menu_frame = ctk.CTkFrame(main_frame)
        menu_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            menu_frame,
            text="Select a Feature",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 25))
        
        # Menu buttons
        buttons_info = [
            ("👥 Students Management", "Manage student records, add new students, update information", "Students", "#10b981"),
            ("📝 Grades Management", "Add and view student grades, track academic performance", "Grades", "#3b82f6"),
            ("📊 Reports", "View GWA reports and academic standings", "Reports", "#f59e0b"),
            ("📈 Analytics Dashboard", "View statistics, charts, and performance insights", "Analytics", "#8b5cf6"),
            ("📚 Courses & Subjects", "Browse available courses and subjects", "Courses", "#6366f1"),
        ]
        
        for icon_text, description, feature, color in buttons_info:
            btn_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=30, pady=8)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=icon_text,
                command=lambda f=feature: self.open_feature(f),
                height=50,
                corner_radius=10,
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=color,
                hover_color=self.adjust_color_brightness(color, 0.8),
                anchor="w"
            )
            btn.pack(fill="x")
            
            ctk.CTkLabel(
                btn_frame,
                text=description,
                font=ctk.CTkFont(size=10),
                text_color="#6b7280"
            ).pack(anchor="w", padx=10, pady=(2, 0))
        
        # Logout button
        ctk.CTkButton(
            menu_frame,
            text="🚪 Logout",
            command=self.logout,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color="#ef4444",
            hover_color="#dc2626"
        ).pack(fill="x", padx=30, pady=(20, 20))
        
    def adjust_color_brightness(self, hex_color, factor):
        """Adjust color brightness for hover effect"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"
        
    def open_feature(self, feature):
        """Open selected feature"""
        self.selected_feature = feature
        self.window.destroy()
        
    def logout(self):
        """Logout and close window"""
        self.selected_feature = None
        self.window.destroy()
        
    def run(self):
        """Run the menu window"""
        self.window.mainloop()
        return self.selected_feature


class EduCoreApp:
    """Main application class"""
    
    def __init__(self, user_data=None, initial_tab=None):
        self.api = APIClient()
        self.user_data = user_data or {}
        self.root = ctk.CTk()
        self.root.geometry("1400x850")
        
        # Update title with user info
        user_name = self.user_data.get('full_name', 'User')
        self.root.title(f"EduCore - Academic Management System v2.0 - Welcome, {user_name}")
        self.root.minsize(1200, 700)
        
        # QR Code directory
        self.qr_code_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "qr_codes")
        os.makedirs(self.qr_code_dir, exist_ok=True)
        
        # Initialize data storage
        self.students = []
        self.courses = []
        self.current_student_grades = []
        self.initial_tab = initial_tab
        
        # Color scheme - Modern palette
        self.colors = {
            'primary': '#6366f1',
            'primary_dark': '#4f46e5',
            'secondary': '#8b5cf6',
            'success': '#10b981',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6',
            'border': '#e5e7eb',
            'bg_light': '#f9fafb',
            'text_primary': '#111827',
            'text_secondary': '#6b7280'
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
            text_color="#6b7280"
        )
        subtitle.pack(anchor="w")
        
        # Right side buttons
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", padx=30)
        
        # Back to menu button
        ctk.CTkButton(
            right_frame,
            text="🏠 Main Menu",
            command=self.back_to_menu,
            width=120,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark']
        ).pack(side="right", padx=(0, 10))
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            right_frame,
            text="● Connected",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['success']
        )
        self.status_label.pack(side="right", padx=(0, 10))
    
    def create_tabview(self):
        """Create main tabview"""
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=10)
        self.tabview.pack(fill="both", expand=True)
        
        # Configure global treeview style for light theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                            background="#ffffff",
                            foreground="#111827",
                            fieldbackground="#ffffff",
                            borderwidth=1,
                            bordercolor="#e5e7eb",
                            rowheight=28,
                            font=('Segoe UI', 10))
        self.style.configure("Treeview.Heading",
                            background="#6366f1",
                            foreground="white",
                            borderwidth=0,
                            relief="flat",
                            font=('Segoe UI', 11, 'bold'))
        self.style.map('Treeview', 
                      background=[('selected', '#e0e7ff')],
                      foreground=[('selected', '#4f46e5')])
        
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
        
        # Set initial tab if specified
        if self.initial_tab:
            self.tabview.set(self.initial_tab)
            # Auto-load analytics if that's the initial tab
            if self.initial_tab == "Analytics":
                self.root.after(100, self.refresh_analytics)
        
        # Store original command and wrap it to auto-load analytics
        self._original_tab_command = self.tabview._segmented_button.cget("command")
        self.tabview._segmented_button.configure(command=self._on_tab_change)
    
    def _on_tab_change(self, tab_name):
        """Handle tab change events"""
        # Call the original command to actually change the tab
        if self._original_tab_command:
            self._original_tab_command(tab_name)
        
        # Auto-refresh analytics when switching to it
        if tab_name == "Analytics":
            self.root.after(100, self.refresh_analytics)
    
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
            corner_radius=10,
            border_width=2,
            border_color="#e5e7eb",
            button_color="#6366f1",
            button_hover_color="#4f46e5"
        )
        self.course_dropdown.pack(fill="x", padx=10, pady=(5, 15))
        
        # Add Button
        ModernButton(
            add_section,
            text="Add Student",
            command=self.add_student,
            fg_color=self.colors['success'],
            hover_color="#059669",
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
            corner_radius=10,
            border_width=2,
            border_color="#e5e7eb",
            button_color="#6366f1",
            button_hover_color="#4f46e5"
        )
        self.update_course_dropdown.pack(fill="x", padx=10, pady=(5, 15))
        
        ModernButton(
            update_section,
            text="Update Course",
            command=self.update_student_course,
            fg_color=self.colors['info'],
            hover_color="#2563eb",
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
            text="📱 View QR",
            command=self.show_student_qr_code,
            fg_color=self.colors['warning'],
            hover_color="#d97706",
            width=120,
            height=35
        ).pack(side="right", padx=5)
        
        ModernButton(
            header_frame,
            text="🗑️ Delete",
            command=self.delete_student,
            fg_color=self.colors['danger'],
            hover_color="#dc2626",
            width=120,
            height=35
        ).pack(side="right")
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(right_panel)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
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
            corner_radius=10,
            border_width=2,
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
        info_frame = ctk.CTkFrame(add_section, fg_color=("#f3f4f6", "#f3f4f6"))
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
            text_color="#4b5563"
        ).pack(padx=10, pady=10, anchor="w")
        
        # Add Button
        ModernButton(
            add_section,
            text="Submit Grade",
            command=self.add_grade,
            fg_color=self.colors['success'],
            hover_color="#059669",
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
            text="📷 Scan QR",
            command=lambda: self.scan_qr_code(self.view_student_code_entry),
            width=120,
            height=35,
            fg_color=self.colors['warning'],
            hover_color="#d97706"
        ).pack(side="left", padx=(0, 10))
        
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
            text_color="#6b7280"
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
        self.analytics_canvas = tk.Canvas(canvas_frame, bg="#f9fafb", highlightthickness=0)
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
        # Load analytics if it's the initial tab
        if self.initial_tab == "Analytics":
            self.refresh_analytics()
    
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
            header = ctk.CTkFrame(course_frame, fg_color=(self.colors['primary'], self.colors['primary']))
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
                    subject_item = ctk.CTkFrame(subjects_frame, fg_color=("#f9fafb", "#f9fafb"))
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
                # Generate QR code for the student
                self.generate_qr_code(student_code, name)
                self.root.after(0, lambda: self.show_success(f"Student added successfully!\nQR code generated for {student_code}"))
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
        
        # Set light theme for matplotlib
        plt.style.use('default')
        
        fig, ax = plt.subplots(figsize=(5, 3.5), facecolor='white', dpi=80)
        ax.set_facecolor('white')
        
        courses = [item['course'] for item in course_data]
        counts = [item['count'] for item in course_data]
        
        colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        
        ax.pie(counts, labels=courses, autopct='%1.1f%%', startangle=90, colors=colors[:len(courses)])
        ax.axis('equal')
        
        # Convert to image
        self.display_chart(fig, self.course_chart_label)
    
    def generate_grade_distribution_chart(self, grade_data):
        """Generate bar chart for grade distribution"""
        if not grade_data:
            return
        
        plt.style.use('default')
        
        fig, ax = plt.subplots(figsize=(5, 3.5), facecolor='white', dpi=80)
        ax.set_facecolor('white')
        
        ranges = [item['range'] for item in grade_data]
        counts = [item['count'] for item in grade_data]
        
        colors = ['#10b981', '#3b82f6', '#f59e0b', '#fb923c', '#ef4444']
        
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
        
        plt.style.use('default')
        
        fig, ax = plt.subplots(figsize=(7, 3.5), facecolor='white', dpi=80)
        ax.set_facecolor('white')
        
        courses = [item['course'] for item in performance_data]
        avg_gwas = [item['avg_gwa'] for item in performance_data]
        
        colors = ['#10b981' if gwa <= 1.75 else '#3b82f6' if gwa <= 2.5 else '#f59e0b' 
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
        ax.axhline(y=1.75, color='#10b981', linestyle='--', alpha=0.6, label='Excellent')
        ax.axhline(y=2.5, color='#3b82f6', linestyle='--', alpha=0.6, label='Good')
        ax.axhline(y=3.0, color='#f59e0b', linestyle='--', alpha=0.6, label='Satisfactory')
        ax.legend(fontsize=8)
        
        plt.tight_layout()
        self.display_chart(fig, self.performance_chart_label)
    
    def display_chart(self, fig, label_widget):
        """Convert matplotlib figure to image and display in label"""
        # Save figure to bytes buffer with optimized DPI for performance
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=80, facecolor='white', bbox_inches='tight')
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
    
    # ==================== QR Code Methods ====================
    
    def generate_qr_code(self, student_code, student_name):
        """Generate QR code for a student"""
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(student_code)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            filename = f"{student_code.replace('-', '_')}.png"
            filepath = os.path.join(self.qr_code_dir, filename)
            img.save(filepath)
            
            print(f"QR code generated: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
    
    def scan_qr_code(self, entry_widget):
        """Scan QR code using camera and fill the entry widget"""
        def scan():
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.root.after(0, lambda: self.show_error("Camera Error", "Could not access camera"))
                    return
                
                # Create a small window for camera feed
                cv2.namedWindow("QR Code Scanner - Press ESC to cancel", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("QR Code Scanner - Press ESC to cancel", 640, 480)
                
                scanned = False
                while not scanned:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Decode QR codes in frame
                    decoded_objects = decode(frame)
                    
                    for obj in decoded_objects:
                        # Draw rectangle around QR code
                        points = obj.polygon
                        if len(points) == 4:
                            pts = [(point.x, point.y) for point in points]
                            cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 3)
                        
                        # Get the data
                        qr_data = obj.data.decode('utf-8')
                        
                        # Display success message on frame
                        cv2.putText(frame, f"Scanned: {qr_data}", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(frame, "Press any key to confirm", (10, 60), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                        
                        cv2.imshow("QR Code Scanner - Press ESC to cancel", frame)
                        cv2.waitKey(1000)  # Show for 1 second
                        
                        # Fill the entry widget
                        self.root.after(0, lambda: entry_widget.delete(0, 'end'))
                        self.root.after(0, lambda d=qr_data: entry_widget.insert(0, d))
                        self.root.after(0, lambda d=qr_data: self.show_success(f"QR Code scanned: {d}"))
                        
                        scanned = True
                        break
                    
                    # Display instructions
                    cv2.putText(frame, "Align QR code in camera view", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, "Press ESC to cancel", (10, 60), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    cv2.imshow("QR Code Scanner - Press ESC to cancel", frame)
                    
                    # Check for ESC key
                    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                        break
                
                cap.release()
                cv2.destroyAllWindows()
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error("Scan Error", f"Error scanning QR code: {str(e)}"))
        
        threading.Thread(target=scan, daemon=True).start()
    
    def show_student_qr_code(self):
        """Show QR code for selected student"""
        selection = self.students_tree.selection()
        if not selection:
            self.show_error("Selection Error", "Please select a student to view QR code")
            return
        
        item = self.students_tree.item(selection[0])
        student_code = item['values'][0]
        student_name = item['values'][1]
        
        # Check if QR code exists
        filename = f"{student_code.replace('-', '_')}.png"
        filepath = os.path.join(self.qr_code_dir, filename)
        
        if not os.path.exists(filepath):
            # Generate if it doesn't exist
            filepath = self.generate_qr_code(student_code, student_name)
            if not filepath:
                self.show_error("Error", "Failed to generate QR code")
                return
        
        # Create a new window to display QR code
        qr_window = ctk.CTkToplevel(self.root)
        qr_window.title(f"QR Code - {student_name} ({student_code})")
        qr_window.geometry("400x500")
        qr_window.resizable(False, False)
        
        # Student info
        info_frame = ctk.CTkFrame(qr_window)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text=f"{student_name}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            info_frame,
            text=f"Student Code: {student_code}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 10))
        
        # Display QR code
        try:
            img = Image.open(filepath)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            qr_label = tk.Label(qr_window, image=photo, bg="white")
            qr_label.image = photo  # Keep a reference
            qr_label.pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(
                qr_window,
                text=f"Error loading QR code:\n{str(e)}",
                font=ctk.CTkFont(size=12)
            ).pack(pady=20)
        
        # Instructions
        ctk.CTkLabel(
            qr_window,
            text="Scan this QR code for quick student lookup",
            font=ctk.CTkFont(size=11),
            text_color="gray70"
        ).pack(pady=(10, 20))
    
    def show_success(self, message):
        """Show success message"""
        messagebox.showinfo("Success", message)
    
    def show_error(self, title, message):
        """Show error message"""
        messagebox.showerror(title, message)
    
    def back_to_menu(self):
        """Return to main menu"""
        if messagebox.askyesno("Return to Menu", "Do you want to return to the main menu?"):
            self.root.destroy()
            # Relaunch menu
            menu = MenuWindow(self.user_data, self.api)
            selected = menu.run()
            if selected:
                app = EduCoreApp(self.user_data, initial_tab=selected)
                app.run()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


class StudentPortalWindow:
    """Student portal window with QR scanning and grade viewing"""
    
    def __init__(self, api_client):
        self.api = api_client
        self.student_data = None
        self.current_student_code = None
        
        # Create window
        self.window = ctk.CTk()
        self.window.geometry("1200x800")
        self.window.title("EduCore - Student Portal")
        self.window.minsize(900, 600)
        
        # QR Code directory
        self.qr_code_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "qr_codes")
        
        # Colors
        self.colors = {
            'primary': '#10b981',
            'primary_dark': '#059669',
            'success': '#10b981',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6',
            'secondary': '#8b5cf6',
            'bg_light': '#f9fafb'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the student portal UI"""
        # Header
        header = ctk.CTkFrame(self.window, height=100, corner_radius=0, fg_color=("#10b981", "#10b981"))
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="👨‍🎓 Student Portal",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="View your grades and academic performance",
            font=ctk.CTkFont(size=13),
            text_color="#d1fae5"
        ).pack(anchor="w")
        
        # Back button
        ctk.CTkButton(
            header,
            text="🏠 Back to Home",
            command=self.go_back,
            width=140,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="white",
            text_color="#10b981",
            hover_color="#f0fdf4"
        ).pack(side="right", padx=30)
        
        # Main content
        self.main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Show scan interface initially
        self.show_scan_interface()
        
    def show_scan_interface(self):
        """Show QR code scanning interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Center frame
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Scan card
        scan_card = ctk.CTkFrame(center_frame, width=550, height=500, corner_radius=20)
        scan_card.pack(padx=40, pady=40)
        scan_card.pack_propagate(False)
        
        ctk.CTkLabel(
            scan_card,
            text="📱",
            font=ctk.CTkFont(size=80)
        ).pack(pady=(40, 20))
        
        ctk.CTkLabel(
            scan_card,
            text="Scan Your Student QR Code",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            scan_card,
            text="Click the button below to scan your QR code\nor enter your student code manually",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280"
        ).pack(pady=(0, 30))
        
        # Manual entry
        entry_frame = ctk.CTkFrame(scan_card, fg_color="transparent")
        entry_frame.pack(pady=(0, 20), padx=40, fill="x")
        
        self.student_code_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Enter Student Code (e.g., 24-49051)",
            height=45,
            font=ctk.CTkFont(size=13),
            corner_radius=10,
            border_width=2,
            border_color="#e5e7eb"
        )
        self.student_code_entry.pack(fill="x", pady=(0, 15))
        self.student_code_entry.bind("<Return>", lambda e: self.load_student_data())
        
        # Buttons
        ctk.CTkButton(
            entry_frame,
            text="📷 Scan QR Code",
            command=self.scan_qr_and_load,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark']
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            entry_frame,
            text="🔍 View My Records",
            command=self.load_student_data,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.colors['info'],
            hover_color="#2563eb"
        ).pack(fill="x")
        
    def scan_qr_and_load(self):
        """Scan QR code and load student data"""
        def scan():
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.window.after(0, lambda: messagebox.showerror("Camera Error", "Could not access camera"))
                    return
                
                self.window.after(0, lambda: messagebox.showinfo("QR Scanner", "Position your QR code in front of the camera.\nPress 'Q' to cancel."))
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    decoded_objects = decode(frame)
                    
                    for obj in decoded_objects:
                        student_code = obj.data.decode('utf-8')
                        cap.release()
                        cv2.destroyAllWindows()
                        
                        self.window.after(0, lambda code=student_code: self.student_code_entry.delete(0, 'end'))
                        self.window.after(0, lambda code=student_code: self.student_code_entry.insert(0, code))
                        self.window.after(100, self.load_student_data)
                        return
                    
                    cv2.imshow('QR Code Scanner - Press Q to quit', frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                cap.release()
                cv2.destroyAllWindows()
                
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Scan Error", f"Error scanning QR code:\n{str(e)}"))
        
        threading.Thread(target=scan, daemon=True).start()
        
    def load_student_data(self):
        """Load student data from API"""
        student_code = self.student_code_entry.get().strip()
        
        if not student_code:
            messagebox.showerror("Validation Error", "Please enter a student code")
            return
        
        def load():
            # Get student info
            student_result = self.api.get(f"/students/{student_code}")
            
            if 'error' in student_result:
                self.window.after(0, lambda: messagebox.showerror("Error", f"Student not found: {student_result['error']}"))
                return
            
            # Get grades
            grades_result = self.api.get(f"/grades/{student_code}")
            
            if 'error' in grades_result:
                self.window.after(0, lambda: messagebox.showerror("Error", f"Could not load grades: {grades_result['error']}"))
                return
            
            self.student_data = student_result
            self.current_student_code = student_code
            self.window.after(0, lambda: self.show_student_dashboard(student_result, grades_result))
        
        threading.Thread(target=load, daemon=True).start()
        
    def show_student_dashboard(self, student_info, grades_data):
        """Show student dashboard with grades and analytics"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.main_container)
        scroll_frame.pack(fill="both", expand=True)
        
        # Student Info Card
        info_card = ctk.CTkFrame(scroll_frame, corner_radius=15)
        info_card.pack(fill="x", pady=(0, 20), padx=10)
        
        info_header = ctk.CTkFrame(info_card, fg_color=("#10b981", "#10b981"), corner_radius=15)
        info_header.pack(fill="x", padx=0, pady=0)
        
        info_content = ctk.CTkFrame(info_header, fg_color="transparent")
        info_content.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(
            info_content,
            text=student_info['name'],
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        details_frame = ctk.CTkFrame(info_content, fg_color="transparent")
        details_frame.pack(anchor="w", pady=(10, 0))
        
        ctk.CTkLabel(
            details_frame,
            text=f"Student Code: {student_info['student_code']}  •  Course: {student_info['course_code']}",
            font=ctk.CTkFont(size=14),
            text_color="#d1fae5"
        ).pack(side="left")
        
        # GWA Display
        gwa = student_info.get('gwa', 0)
        gwa_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        gwa_frame.pack(fill="x", padx=30, pady=20)
        
        gwa_value = f"{gwa:.2f}" if gwa > 0 else "N/A"
        gwa_color = "#10b981" if gwa <= 1.75 else "#3b82f6" if gwa <= 2.5 else "#f59e0b" if gwa <= 3.0 else "#ef4444"
        gwa_status = self.get_grade_description(gwa)
        
        ctk.CTkLabel(
            gwa_frame,
            text="General Weighted Average (GWA)",
            font=ctk.CTkFont(size=14),
            text_color="#6b7280"
        ).pack(anchor="w")
        
        gwa_display_frame = ctk.CTkFrame(gwa_frame, fg_color="transparent")
        gwa_display_frame.pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(
            gwa_display_frame,
            text=gwa_value,
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=gwa_color
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            gwa_display_frame,
            text=f"• {gwa_status}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=gwa_color
        ).pack(side="left")
        
        # Grades Section
        grades_card = ctk.CTkFrame(scroll_frame, corner_radius=15)
        grades_card.pack(fill="both", expand=True, pady=(0, 20), padx=10)
        
        ctk.CTkLabel(
            grades_card,
            text="📝 Your Grades",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        if grades_data:
            # Treeview for grades
            tree_frame = ctk.CTkFrame(grades_card)
            tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            style = ttk.Style()
            style.configure("Student.Treeview",
                          background="#ffffff",
                          foreground="#111827",
                          fieldbackground="#ffffff",
                          rowheight=35,
                          font=('Segoe UI', 11))
            style.configure("Student.Treeview.Heading",
                          background="#10b981",
                          foreground="white",
                          font=('Segoe UI', 12, 'bold'))
            style.map('Student.Treeview',
                     background=[('selected', '#d1fae5')],
                     foreground=[('selected', '#065f46')])
            
            grades_tree = ttk.Treeview(
                tree_frame,
                columns=("Subject Code", "Subject Name", "Grade", "Status"),
                show="headings",
                height=8,
                style="Student.Treeview"
            )
            
            grades_tree.heading("Subject Code", text="Subject Code")
            grades_tree.heading("Subject Name", text="Subject Name")
            grades_tree.heading("Grade", text="Grade")
            grades_tree.heading("Status", text="Status")
            
            grades_tree.column("Subject Code", width=120, anchor="center")
            grades_tree.column("Subject Name", width=400)
            grades_tree.column("Grade", width=100, anchor="center")
            grades_tree.column("Status", width=150, anchor="center")
            
            for grade in grades_data:
                grades_tree.insert("", "end", values=(
                    grade['subject_code'],
                    grade['subject_name'],
                    grade['formatted_grade'],
                    grade['description']
                ))
            
            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=grades_tree.yview)
            grades_tree.configure(yscrollcommand=vsb.set)
            
            grades_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            vsb.pack(side="right", fill="y", pady=10)
            
            # Performance Analysis
            self.show_performance_analysis(scroll_frame, grades_data, gwa)
        else:
            ctk.CTkLabel(
                grades_card,
                text="No grades recorded yet",
                font=ctk.CTkFont(size=14),
                text_color="#6b7280"
            ).pack(pady=30)
        
    def show_performance_analysis(self, parent, grades_data, gwa):
        """Show performance analysis and recommendations"""
        analysis_card = ctk.CTkFrame(parent, corner_radius=15)
        analysis_card.pack(fill="x", pady=(0, 20), padx=10)
        
        ctk.CTkLabel(
            analysis_card,
            text="📊 Performance Analysis",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        content_frame = ctk.CTkFrame(analysis_card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Calculate statistics
        total_subjects = len(grades_data)
        excellent = len([g for g in grades_data if float(g['grade']) <= 1.75])
        good = len([g for g in grades_data if 1.75 < float(g['grade']) <= 2.5])
        satisfactory = len([g for g in grades_data if 2.5 < float(g['grade']) <= 3.0])
        failed = len([g for g in grades_data if float(g['grade']) > 3.0])
        
        # Stats boxes
        stats_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 20))
        
        self.create_stat_box_student(stats_container, "Total Subjects", str(total_subjects), "#3b82f6").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_box_student(stats_container, "Excellent", str(excellent), "#10b981").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_box_student(stats_container, "Good", str(good), "#3b82f6").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_box_student(stats_container, "Needs Improvement", str(satisfactory + failed), "#f59e0b").pack(side="left", expand=True, fill="x", padx=5)
        
        # Recommendations
        recommendations = self.generate_recommendations(grades_data, gwa)
        
        if recommendations['strengths']:
            strength_frame = ctk.CTkFrame(content_frame, fg_color=("#d1fae5", "#d1fae5"), corner_radius=10)
            strength_frame.pack(fill="x", pady=(0, 10))
            
            ctk.CTkLabel(
                strength_frame,
                text="💪 Your Strengths",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#065f46"
            ).pack(anchor="w", padx=15, pady=(15, 10))
            
            for strength in recommendations['strengths']:
                ctk.CTkLabel(
                    strength_frame,
                    text=f"• {strength}",
                    font=ctk.CTkFont(size=12),
                    text_color="#047857",
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=2)
            
            ctk.CTkLabel(strength_frame, text="").pack(pady=5)
        
        if recommendations['improvements']:
            improve_frame = ctk.CTkFrame(content_frame, fg_color=("#fef3c7", "#fef3c7"), corner_radius=10)
            improve_frame.pack(fill="x", pady=(0, 10))
            
            ctk.CTkLabel(
                improve_frame,
                text="📈 Areas for Improvement",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#92400e"
            ).pack(anchor="w", padx=15, pady=(15, 10))
            
            for improvement in recommendations['improvements']:
                ctk.CTkLabel(
                    improve_frame,
                    text=f"• {improvement}",
                    font=ctk.CTkFont(size=12),
                    text_color="#b45309",
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=2)
            
            ctk.CTkLabel(improve_frame, text="").pack(pady=5)
        
        # Overall message
        message_frame = ctk.CTkFrame(content_frame, fg_color=("#dbeafe", "#dbeafe"), corner_radius=10)
        message_frame.pack(fill="x")
        
        ctk.CTkLabel(
            message_frame,
            text="💡 " + recommendations['message'],
            font=ctk.CTkFont(size=13),
            text_color="#1e40af",
            wraplength=800,
            justify="left"
        ).pack(padx=15, pady=15)
        
    def create_stat_box_student(self, parent, title, value, color):
        """Create a statistics box for student portal"""
        box = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        
        ctk.CTkLabel(
            box,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="white"
        ).pack(pady=(12, 5))
        
        ctk.CTkLabel(
            box,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        ).pack(pady=(0, 12))
        
        return box
        
    def generate_recommendations(self, grades_data, gwa):
        """Generate personalized recommendations"""
        strengths = []
        improvements = []
        
        # Analyze grades
        excellent_subjects = [g for g in grades_data if float(g['grade']) <= 1.75]
        weak_subjects = [g for g in grades_data if float(g['grade']) > 2.5]
        
        # Strengths
        if excellent_subjects:
            if len(excellent_subjects) >= len(grades_data) * 0.7:
                strengths.append("Outstanding academic performance across most subjects!")
            subject_names = ", ".join([g['subject_name'] for g in excellent_subjects[:3]])
            strengths.append(f"Excelling in: {subject_names}")
        
        if gwa <= 1.75:
            strengths.append("Your GWA qualifies you for academic honors - keep it up!")
        
        # Improvements
        if weak_subjects:
            subject_names = ", ".join([g['subject_name'] for g in weak_subjects[:3]])
            improvements.append(f"Focus more on: {subject_names}")
            improvements.append("Consider seeking help from teachers or study groups for challenging subjects")
        
        if gwa > 2.5:
            improvements.append("Work on improving your overall GWA by focusing on weaker subjects")
        
        # Overall message
        if gwa <= 1.75:
            message = "Excellent work! You're performing at a very high level. Continue your excellent study habits and consider helping peers who might benefit from your knowledge."
        elif gwa <= 2.5:
            message = "Good job! You're doing well overall. With some extra effort in a few areas, you can achieve even better results. Keep up the consistent work!"
        elif gwa <= 3.0:
            message = "You're making satisfactory progress. Focus on strengthening your understanding in subjects where you're struggling. Don't hesitate to ask for help when needed."
        else:
            message = "It's important to address your academic challenges. Consider talking to your teachers about extra support, joining study groups, or adjusting your study methods."
        
        return {
            'strengths': strengths,
            'improvements': improvements,
            'message': message
        }
        
    def get_grade_description(self, grade: float) -> str:
        """Get description for a grade"""
        if grade == 0:
            return "Not yet graded"
        elif grade <= 1.75:
            return "Excellent"
        elif grade <= 2.5:
            return "Good"
        elif grade <= 3.0:
            return "Satisfactory"
        else:
            return "Needs Improvement"
            
    def go_back(self):
        """Go back to role selection"""
        self.window.destroy()
        
    def run(self):
        """Run the student portal"""
        self.window.mainloop()


def main():
    """Main entry point"""
    print("=================================================")
    print("  EduCore Academic Management System v2.0")
    print("=================================================")
    print("Starting GUI application...")
    print("Make sure the FastAPI backend is running on port 8000")
    print("=================================================\n")
    
    # Create API client
    api_client = APIClient()
    
    # Main application loop
    while True:
        # Show role selection
        print("Opening role selection...")
        role_window = RoleSelectionWindow()
        selected_role = role_window.run()
        
        if not selected_role:
            print("Application closed. Goodbye!")
            break
        
        if selected_role == "teacher":
            # Teacher/Admin flow
            print("Opening teacher login window...")
            login_window = LoginWindow(api_client)
            success, user_data = login_window.run()
            
            if not success:
                print("Login cancelled or failed. Returning to role selection...")
                continue
            
            print(f"Login successful! Welcome, {user_data.get('full_name', 'User')}")
            print(f"Role: {user_data.get('role', 'N/A')}")
            print("Loading main menu...\n")
            
            # Show menu window and get selected feature
            while True:
                menu = MenuWindow(user_data, api_client)
                selected_feature = menu.run()
                
                if not selected_feature:
                    # User logged out or closed menu
                    print("Logged out. Returning to role selection...")
                    break
                
                print(f"Opening {selected_feature} module...\n")
                
                # Create and run main application with selected tab
                app = EduCoreApp(user_data, initial_tab=selected_feature)
                app.run()
                
                # After closing app, loop back to menu unless user exits
                print("Returning to menu...\n")
        
        elif selected_role == "student":
            # Student flow
            print("Opening student portal...")
            student_portal = StudentPortalWindow(api_client)
            student_portal.run()
            print("Student portal closed. Returning to role selection...")
    
    print("\nApplication closed. Goodbye!")


if __name__ == "__main__":
    main()

