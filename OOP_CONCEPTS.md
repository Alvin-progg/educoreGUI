# EduCore Project: Object-Oriented Programming (OOP) Concepts

## Overview
This document outlines the Object-Oriented Programming (OOP) concepts used in the EduCore Academic Management System v2.0 project with Authentication and QR Code features.

---

## Table: OOP Concepts

| **Concept** | **Definition** | **Where Used** | **Code Example from Project** |
|-------------|----------------|----------------|-------------------------------|
| **Class** | Blueprint for creating objects with attributes and methods | `models.py`: `Student`, `Course`, `Grade`, `CourseSubject`, `User`<br>`schemas.py`: `StudentCreate`, `GradeResponse`, `LoginRequest`, `LoginResponse`<br>`gui.py`: `APIClient`, `ModernButton`, `LoginWindow`, `EduCoreApp` | `class Student(Base):`<br>`    __tablename__ = "students"`<br>`    id = Column(Integer, primary_key=True)`<br><br>`class User(Base):`<br>`    __tablename__ = "users"`<br>`    username = Column(String(50), unique=True)` |
| **Inheritance** | Mechanism where a class derives properties/methods from parent class | `models.py`: All models inherit from `Base` (Student, Course, Grade, User)<br>`schemas.py`: `StudentCreate(StudentBase)`, `StudentUpdate(BaseModel)`, `LoginRequest(BaseModel)`<br>`gui.py`: `ModernButton(ctk.CTkButton)`, `ModernEntry(ctk.CTkEntry)`, `LoginWindow` creates CTk window | `class Student(Base):`<br>`    """Student model"""`<br><br>`class User(Base):`<br>`    """User authentication model"""` |
| **Encapsulation** | Bundling data and methods within a class; controlling access via private/public attributes | `gui.py`: `APIClient` encapsulates HTTP logic<br>`models.py`: Private attributes with SQLAlchemy columns<br>`gui.py`: `self.colors`, `self.students`, `self.api` | `class APIClient:`<br>`    def __init__(self, base_url="http://..."):`<br>`        self.base_url = base_url`<br>`        self.timeout = 10` |
| **Polymorphism** | Ability of different classes to be used through same interface | `gui.py`: `ModernButton` and `ModernEntry` override parent constructors<br>`schemas.py`: Multiple schema classes share `BaseModel` interface | `class ModernButton(ctk.CTkButton):`<br>`    def __init__(self, master, **kwargs):`<br>`        super().__init__(master, corner_radius=8, ...)` |
| **Method** | Function defined inside a class | `main.py`: `get_all_students()`, `add_student()`, `update_student_gwa()`<br>`gui.py`: `setup_ui()`, `add_student()`, `refresh_students()`<br>`schemas.py`: `validate_grade()` | `def add_student(student: StudentCreate, db: Session):`<br>`    existing = db.query(Student).filter(...).first()`<br>`    if existing:`<br>`        raise HTTPException(...)` |
| **Constructor (`__init__`)** | Special method to initialize object state | `gui.py`: `APIClient.__init__()`, `EduCoreApp.__init__()`<br>`models.py`: Implicit via SQLAlchemy | `def __init__(self):`<br>`    self.api = APIClient()`<br>`    self.root = ctk.CTk()`<br>`    self.students = []` |
| **Property/Attribute** | Class variables that store state | `models.py`: `student_code`, `name`, `gwa`, `created_at`<br>`gui.py`: `self.students`, `self.colors`, `self.api` | `student_code = Column(String(20), unique=True, nullable=False)`<br>`gwa = Column(Float, default=0.0)` |
| **String Representation (`__repr__`)** | Defines how object is represented as string | `models.py`: All model classes | `def __repr__(self):`<br>`    return f"<Student(code='{self.student_code}', name='{self.name}')>"` |
| **Class Configuration** | Nested Config class for Pydantic/SQLAlchemy settings | `schemas.py`: `Config` class in all response models | `class Config:`<br>`    from_attributes = True  # Pydantic v2`<br>`    orm_mode = True  # Pydantic v1` |
| **Super() Function** | Calls parent class methods | `gui.py`: `super().__init__()` in custom widgets | `super().__init__(master, corner_radius=8, font=..., **kwargs)` |
| **GUI Widget Inheritance** | Creating custom widgets by extending tkinter/customtkinter | `gui.py`: `ModernButton(ctk.CTkButton)`, `ModernEntry(ctk.CTkEntry)` | `class ModernButton(ctk.CTkButton):`<br>`    def __init__(self, master, **kwargs):`<br>`        super().__init__(master, corner_radius=8, ...)` |

---

## Key Classes and Their Purposes

### Backend (`backend/`)

#### `models.py`
- **`User`**: 🔐 Authentication model with username, password_hash, role
- **`Student`**: Represents a student with code, name, course, and GWA
- **`Course`**: Represents a course program (BSIT, BSCS, BSBA)
- **`CourseSubject`**: Maps subjects to courses
- **`Grade`**: Stores student grades for subjects

#### `schemas.py`
- **`LoginRequest`**: 🔐 Schema for login credentials
- **`LoginResponse`**: 🔐 Response format for authentication
- **`UserResponse`**: 🔐 User data response format
- **`StudentCreate`**: Validation schema for creating students
- **`StudentResponse`**: Response format for student data
- **`GradeCreate`**: Validation schema for grade input
- **`GradeResponse`**: Response format for grade data

### Frontend (`frontend/`)

#### `gui.py`
- **`APIClient`**: Handles HTTP communication with backend
- **`ModernButton`**: Custom styled button widget
- **`ModernEntry`**: Custom styled entry widget
- **`LoginWindow`**: 🔐 Authentication window class
- **`EduCoreApp`**: Main application class with GUI and QR code features

---

## Core OOP Principles in Action

### 1. **Inheritance**
- All database models inherit from SQLAlchemy's `Base` class
- Schema classes inherit from Pydantic's `BaseModel`
- Custom GUI widgets inherit from CustomTkinter components
- Enables code reuse and extension of functionality

### 2. **Encapsulation**
- Database logic encapsulated in model classes
- API communication encapsulated in `APIClient`
- UI logic organized within `EduCoreApp` class
- Private attributes protected with naming conventions

### 3. **Polymorphism**
- Custom widgets override parent class methods
- Multiple schema classes implement same interface
- Different handlers respond to similar events
- Enables flexible and extensible code

### 4. **Abstraction**
- Complex database operations hidden behind simple methods
- API details abstracted away from GUI code
- User doesn't need to know implementation details
- Simplifies usage and maintenance

---

## Design Patterns

### 1. **Model-View Pattern**
- **Models** (`models.py`): Data structure and business logic
- **Views** (`gui.py`): User interface and presentation
- Separation of concerns for maintainability

### 2. **Dependency Injection**
- Database sessions injected into endpoints
- Configuration passed to classes at initialization
- Reduces coupling between components

### 3. **Factory Pattern** (Implicit)
- SQLAlchemy session factory via `get_db()`
- Object creation abstracted from usage
- Centralized object instantiation

### 4. **Observer Pattern**
- GUI event handlers respond to user actions
- Callbacks registered for button clicks
- Loose coupling between UI and logic

---

## Conclusion

This project demonstrates comprehensive use of **core OOP principles**:
- **Classes and Objects**: Blueprint pattern for creating instances
- **Inheritance**: Code reuse through parent-child relationships
- **Encapsulation**: Data hiding and access control
- **Polymorphism**: Flexible interfaces and method overriding
- **Abstraction**: Hiding complexity behind simple interfaces

The codebase follows modern OOP best practices, making it maintainable, scalable, and well-structured.
