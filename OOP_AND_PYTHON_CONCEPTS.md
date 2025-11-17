# EduCore Project: OOP and Advanced Python Concepts

## Overview
This document outlines the Object-Oriented Programming (OOP) concepts and advanced Python features used in the EduCore Academic Management System v2.0 project with Authentication and QR Code features.

---

## Table: OOP Concepts and Advanced Python Features

| **Concept** | **Definition** | **Where Used** | **Code Example from Project** |
|-------------|----------------|----------------|-------------------------------|
| **Class** | Blueprint for creating objects with attributes and methods | `models.py`: `Student`, `Course`, `Grade`, `CourseSubject`, `User`<br>`schemas.py`: `StudentCreate`, `GradeResponse`, `LoginRequest`, `LoginResponse`<br>`gui.py`: `APIClient`, `ModernButton`, `LoginWindow`, `EduCoreApp` | `class Student(Base):`<br>`    __tablename__ = "students"`<br>`    id = Column(Integer, primary_key=True)`<br><br>`class User(Base):`<br>`    __tablename__ = "users"`<br>`    username = Column(String(50), unique=True)` |
| **Inheritance** | Mechanism where a class derives properties/methods from parent class | `models.py`: All models inherit from `Base` (Student, Course, Grade, User)<br>`schemas.py`: `StudentCreate(StudentBase)`, `StudentUpdate(BaseModel)`, `LoginRequest(BaseModel)`<br>`gui.py`: `ModernButton(ctk.CTkButton)`, `ModernEntry(ctk.CTkEntry)`, `LoginWindow` creates CTk window | `class Student(Base):`<br>`    """Student model"""`<br><br>`class User(Base):`<br>`    """User authentication model"""` |
| **Encapsulation** | Bundling data and methods within a class; controlling access via private/public attributes | `gui.py`: `APIClient` encapsulates HTTP logic<br>`models.py`: Private attributes with SQLAlchemy columns<br>`gui.py`: `self.colors`, `self.students`, `self.api` | `class APIClient:`<br>`    def __init__(self, base_url="http://..."):`<br>`        self.base_url = base_url`<br>`        self.timeout = 10` |
| **Polymorphism** | Ability of different classes to be used through same interface | `gui.py`: `ModernButton` and `ModernEntry` override parent constructors<br>`schemas.py`: Multiple schema classes share `BaseModel` interface | `class ModernButton(ctk.CTkButton):`<br>`    def __init__(self, master, **kwargs):`<br>`        super().__init__(master, corner_radius=8, ...)` |
| **Method** | Function defined inside a class | `main.py`: `get_all_students()`, `add_student()`, `update_student_gwa()`<br>`gui.py`: `setup_ui()`, `add_student()`, `refresh_students()`<br>`schemas.py`: `validate_grade()` | `def add_student(student: StudentCreate, db: Session):`<br>`    existing = db.query(Student).filter(...).first()`<br>`    if existing:`<br>`        raise HTTPException(...)` |
| **Constructor (`__init__`)** | Special method to initialize object state | `gui.py`: `APIClient.__init__()`, `EduCoreApp.__init__()`<br>`models.py`: Implicit via SQLAlchemy | `def __init__(self):`<br>`    self.api = APIClient()`<br>`    self.root = ctk.CTk()`<br>`    self.students = []` |
| **Relationship (ORM)** | Defines associations between database tables | `models.py`: `Student.course`, `Student.grades`, `Course.students`, `Course.subjects` | `course = relationship("Course", back_populates="students")`<br>`grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")` |
| **Decorator** | Function that modifies behavior of another function | `main.py`: `@app.get()`, `@app.post()`, `@app.on_event()`<br>`schemas.py`: `@validator()` | `@app.get("/api/students", response_model=List[StudentResponse])`<br>`def get_all_students(db: Session = Depends(get_db)):` |
| **Type Hints** | Static type annotations for variables/parameters | `main.py`: All function signatures<br>`schemas.py`: All Pydantic models<br>`gui.py`: `List[Dict]`, `Optional[str]` | `def get(self, endpoint) -> dict:`<br>`def add_grade(grade_data: GradeCreate, db: Session):` |
| **Dependency Injection** | Pattern where dependencies are provided externally | `main.py`: `db: Session = Depends(get_db)` used in all endpoints | `def get_all_students(db: Session = Depends(get_db)):`<br>`    students = db.query(Student).order_by(...)` |
| **Context Manager** | Objects that manage resource setup/cleanup (implicit via SQLAlchemy sessions) | `main.py`: `db = next(get_db())` in startup event | `db = next(get_db())`<br>`try:`<br>`    # operations`<br>`finally:`<br>`    db.close()` |
| **Property/Attribute** | Class variables that store state | `models.py`: `student_code`, `name`, `gwa`, `created_at`<br>`gui.py`: `self.students`, `self.colors`, `self.api` | `student_code = Column(String(20), unique=True, nullable=False)`<br>`gwa = Column(Float, default=0.0)` |
| **Foreign Key** | Database constraint establishing relationship | `models.py`: `course_code` in `Student`, `student_code` in `Grade` | `course_code = Column(String(20), ForeignKey("courses.code"), nullable=False)` |
| **Cascade Operations** | Automatic propagation of operations to related entities | `models.py`: `cascade="all, delete-orphan"` on relationships | `grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")` |
| **Unique Constraint** | Database constraint ensuring uniqueness | `models.py`: `UniqueConstraint` on `Grade` and `CourseSubject` | `__table_args__ = (`<br>`    UniqueConstraint('student_code', 'subject_code', name='uq_student_subject'),`<br>`)` |
| **Data Validation** | Ensuring data integrity via Pydantic validators | `schemas.py`: `@validator('grade')`, `Field(..., ge=1.0, le=5.0)` | `@validator('grade')`<br>`def validate_grade(cls, v):`<br>`    if v < 1.0 or v > 5.0:`<br>`        raise ValueError('...')`<br>`    return round(v, 2)` |
| **Pydantic BaseModel** | Data validation and serialization class | `schemas.py`: All schema classes inherit from `BaseModel` | `class StudentCreate(StudentBase):`<br>`    pass`<br><br>`class GradeCreate(BaseModel):`<br>`    student_code: str = Field(...)` |
| **String Representation (`__repr__`)** | Defines how object is represented as string | `models.py`: All model classes | `def __repr__(self):`<br>`    return f"<Student(code='{self.student_code}', name='{self.name}')>"` |
| **Class Configuration** | Nested Config class for Pydantic/SQLAlchemy settings | `schemas.py`: `Config` class in all response models | `class Config:`<br>`    from_attributes = True  # Pydantic v2`<br>`    orm_mode = True  # Pydantic v1` |
| **Async Event Handler** | Asynchronous function for startup events | `main.py`: `@app.on_event("startup")` with `async def` | `@app.on_event("startup")`<br>`async def startup_event():`<br>`    db = next(get_db())`<br>`    # Initialize courses` |
| **Exception Handling** | Managing errors via try-except and HTTPException | `main.py`: `HTTPException` for API errors<br>`gui.py`: `requests.exceptions.RequestException` | `if not student:`<br>`    raise HTTPException(status_code=404, detail="Student not found")` |
| **List Comprehension** | Concise way to create lists | `main.py`: Building response lists, grade distributions | `result = [`<br>`    {"student_code": s.student_code, "name": s.name}`<br>`    for s in top_performers`<br>`]` |
| **Dictionary** | Key-value data structure | `gui.py`: `self.colors` configuration<br>`main.py`: Response dictionaries | `self.colors = {`<br>`    'primary': '#1f538d',`<br>`    'success': '#2ecc71',`<br>`    'danger': '#e74c3c'`<br>`}` |
| **Threading** | Concurrent execution (imported but pattern available) | `gui.py`: `import threading` | `import threading` (imported for potential background tasks) |
| **Query Building (SQLAlchemy ORM)** | Constructing database queries using ORM | `main.py`: `db.query(Student).filter().first()`, `.order_by()`, `.group_by()` | `avg_grade = db.query(func.avg(Grade.grade))`<br>`.filter(Grade.student_code == student_code)`<br>`.scalar()` |
| **Aggregation Functions** | SQL aggregate functions via ORM | `main.py`: `func.avg()`, `func.count()` | `total_students = db.query(Student).count()`<br>`avg_gwa = db.query(func.avg(Student.gwa)).scalar()` |
| **Default Values** | Setting default parameter/attribute values | `models.py`: `gwa = Column(Float, default=0.0)`<br>`schemas.py`: `Field(..., description="...")` | `gwa = Column(Float, default=0.0)`<br>`self.timeout = 10` |
| **Optional Types** | Type hints for nullable values | `schemas.py`: `Optional[datetime]` for timestamps | `created_at: Optional[datetime]`<br>`updated_at: Optional[datetime]` |
| **Server-side Defaults** | Database-level default values | `models.py`: `server_default=func.now()` | `created_at = Column(DateTime(timezone=True), server_default=func.now())` |
| **CRUD Operations** | Create, Read, Update, Delete patterns | `main.py`: Complete CRUD for Student, Grade, Course | `db.add(new_student)  # Create`<br>`db.query(Student).all()  # Read`<br>`student.course_code = ...  # Update`<br>`db.delete(student)  # Delete`<br>`db.commit()` |
| **RESTful API Endpoints** | HTTP methods mapped to operations | `main.py`: GET, POST, PUT, DELETE endpoints | `@app.get("/api/students")`<br>`@app.post("/api/students")`<br>`@app.put("/api/students/{student_code}")`<br>`@app.delete("/api/students/{student_code}")` |
| **Middleware** | Processing layer between request/response | `main.py`: CORS middleware configuration | `app.add_middleware(`<br>`    CORSMiddleware,`<br>`    allow_origins=["*"],`<br>`    allow_methods=["*"]`<br>`)` |
| **GUI Widget Inheritance** | Creating custom widgets by extending tkinter/customtkinter | `gui.py`: `ModernButton(ctk.CTkButton)`, `ModernEntry(ctk.CTkEntry)` | `class ModernButton(ctk.CTkButton):`<br>`    def __init__(self, master, **kwargs):`<br>`        super().__init__(master, corner_radius=8, ...)` |
| **Event Binding** | Connecting GUI events to handler functions | `gui.py`: `.bind("<Return>", lambda e: ...)`, `command=self.add_student` | `self.grade_student_code_entry.bind("<Return>", lambda e: self.load_subjects_for_student())` |
| **Super() Function** | Calls parent class methods | `gui.py`: `super().__init__()` in custom widgets | `super().__init__(master, corner_radius=8, font=..., **kwargs)` |
| **Password Hashing** 🔐 | Encrypting passwords using bcrypt algorithm | `main.py`: `pwd_context.hash()`, `pwd_context.verify()` | `password_hash = pwd_context.hash(password)`<br>`is_valid = pwd_context.verify(plain_password, hashed)` |
| **Authentication** 🔐 | User login validation system | `main.py`: `/api/auth/login` endpoint<br>`gui.py`: `LoginWindow` class | `@app.post("/api/auth/login")`<br>`def login(credentials: LoginRequest, db: Session):` |
| **Modal Window** 🔐 | Separate window for specific task | `gui.py`: `LoginWindow` creates login dialog | `self.window = ctk.CTk()`<br>`self.window.geometry("550x700")`<br>`self.window.mainloop()` |
| **QR Code Generation** 📱 | Creating QR codes from data | `gui.py`: `generate_qr_code()` method using qrcode library | `qr = qrcode.QRCode(...)`<br>`qr.add_data(student_code)`<br>`img = qr.make_image()`<br>`img.save(filepath)` |
| **Camera Access** 📱 | Opening and reading from webcam | `gui.py`: `scan_qr_code()` using OpenCV | `cap = cv2.VideoCapture(0)`<br>`ret, frame = cap.read()`<br>`cap.release()` |
| **QR Code Decoding** 📱 | Reading and extracting data from QR codes | `gui.py`: Using pyzbar to decode QR from camera | `decoded_objects = decode(frame)`<br>`qr_data = obj.data.decode('utf-8')` |
| **Image Processing** 📱 | Manipulating images and video frames | `gui.py`: OpenCV frame processing and PIL image operations | `cv2.polylines(frame, [pts], True, (0, 255, 0), 3)`<br>`img.resize((300, 300), Image.Resampling.LANCZOS)` |
| **File I/O** 📱 | Reading and writing files | `gui.py`: Saving QR codes as PNG files | `img.save(filepath)`<br>`img = Image.open(filepath)`<br>`os.path.exists(filepath)` |
| **Threading** 📱 | Running code in background threads | `gui.py`: Background operations for API calls and scanning | `threading.Thread(target=scan, daemon=True).start()` |
| **Window Destruction** | Closing and removing GUI windows | `gui.py`: Destroying login window after authentication | `self.window.after(0, self.window.destroy)` |
| **Boolean State** | Using flags to track application state | `gui.py`: `login_successful` flag in LoginWindow | `self.login_successful = False`<br>`if not success: return` |
| **Password Visibility Toggle** | Show/hide password in input field | `gui.py`: Checkbox controlling password display | `if self.show_password_var.get():`<br>`    self.password_entry.configure(show="")`<br>`else:`<br>`    self.password_entry.configure(show="•")` |

---

## Summary of Advanced Python Features

### 1. **ORM (SQLAlchemy)**
- Declarative Base
- Relationships (one-to-many, many-to-one)
- Foreign keys
- Cascade operations
- Unique constraints
- Query building and filtering

### 2. **API Framework (FastAPI)**
- Route decorators (`@app.get`, `@app.post`, `@app.put`, `@app.delete`)
- Dependency injection with `Depends()`
- Async event handlers
- Middleware configuration (CORS)
- Automatic API documentation

### 3. **Data Validation (Pydantic)**
- BaseModel for schema definition
- Field validators and constraints
- Custom validators with `@validator`
- Type coercion and validation
- Automatic JSON serialization

### 4. **Type System**
- Type hints for parameters and return values
- Generic types (`List[StudentResponse]`)
- Optional types for nullable values
- Static type checking support

### 5. **GUI Framework (CustomTkinter)**
- Widget inheritance and customization
- Event binding and handling
- Layout management (pack, grid)
- Custom styling and theming

### 6. **HTTP Client (Requests)**
- REST API communication
- Exception handling
- Timeout management
- JSON request/response handling

### 7. **Database Patterns**
- CRUD operations
- Query building with ORM
- Aggregation functions
- Transaction management
- Data integrity constraints

### 8. **Design Patterns**
- Dependency injection
- Encapsulation of API logic
- Factory pattern (implicit in ORM)
- Observer pattern (GUI event handlers)

---

## Key Classes and Their Purposes

### Backend (`backend/`)

#### `models.py`
- **`User`**: 🔐 NEW! Authentication model with username, password_hash, role
- **`Student`**: Represents a student with code, name, course, and GWA
- **`Course`**: Represents a course program (BSIT, BSCS, BSBA)
- **`CourseSubject`**: Maps subjects to courses
- **`Grade`**: Stores student grades for subjects

#### `schemas.py`
- **`LoginRequest`**: 🔐 NEW! Schema for login credentials
- **`LoginResponse`**: 🔐 NEW! Response format for authentication
- **`UserResponse`**: 🔐 NEW! User data response format
- **`StudentCreate`**: Validation schema for creating students
- **`StudentResponse`**: Response format for student data
- **`GradeCreate`**: Validation schema for grade input
- **`GradeResponse`**: Response format for grade data

#### `main.py`
- **FastAPI Application**: REST API server
- **CRUD Endpoints**: Student, Grade, Course management
- **Analytics Endpoints**: GWA reports and statistics
- **Helper Functions**: GWA calculation, grade formatting

### Frontend (`frontend/`)

#### `gui.py`
- **`APIClient`**: Handles HTTP communication with backend
- **`ModernButton`**: Custom styled button widget
- **`ModernEntry`**: Custom styled entry widget
- **`LoginWindow`**: 🔐 NEW! Authentication window class
- **`EduCoreApp`**: Main application class with GUI and QR code features

---

## Functions and Definitions

### Backend Functions (main.py)

| Function | Purpose | Parameters | Return Type |
|----------|---------|------------|-------------|
| `get_all_students()` | Retrieve all students | `db: Session` | `List[StudentResponse]` |
| `add_student()` | Create new student | `student: StudentCreate, db: Session` | `StudentResponse` |
| `get_student()` | Get student by code | `student_code: str, db: Session` | `StudentResponse` |
| `update_student()` | Update student course | `student_code: str, student_update: StudentUpdate, db: Session` | `StudentResponse` |
| `delete_student()` | Delete student and grades | `student_code: str, db: Session` | `dict` |
| `get_student_grades()` | Get all grades for student | `student_code: str, db: Session` | `List[GradeResponse]` |
| `add_grade()` | Add or update grade | `grade_data: GradeCreate, db: Session` | `GradeResponse` |
| `get_gwa_report()` | Generate GWA report | `db: Session` | `List[GWAReportResponse]` |
| `update_student_gwa()` | Calculate and update GWA | `student_code: str, db: Session` | `None` |
| `get_grade_description()` | Get description for grade | `grade: float` | `str` |
| `format_grade()` | Format grade for display | `grade: float` | `str` |
| `get_analytics_overview()` | Get statistics dashboard | `db: Session` | `dict` |

### Frontend Methods (gui.py)

| Method | Purpose | Class |
|--------|---------|-------|
| `__init__()` | Initialize application | `EduCoreApp` |
| `setup_ui()` | Build main interface | `EduCoreApp` |
| `create_header()` | Create app header | `EduCoreApp` |
| `create_tabview()` | Create tab navigation | `EduCoreApp` |
| `create_students_tab()` | Build students tab | `EduCoreApp` |
| `create_grades_tab()` | Build grades tab | `EduCoreApp` |
| `create_reports_tab()` | Build reports tab | `EduCoreApp` |
| `create_analytics_tab()` | Build analytics tab | `EduCoreApp` |
| `add_student()` | Add new student via API | `EduCoreApp` |
| `update_student_course()` | Update student's course | `EduCoreApp` |
| `delete_student()` | Delete selected student | `EduCoreApp` |
| `refresh_students()` | Reload student list | `EduCoreApp` |
| `get()` | Send GET request | `APIClient` |
| `post()` | Send POST request | `APIClient` |
| `put()` | Send PUT request | `APIClient` |
| `delete()` | Send DELETE request | `APIClient` |

---

## Project Architecture

```
EduCore System v2.0
├── Backend (FastAPI)
│   ├── Database Layer (SQLAlchemy ORM)
│   ├── Models (User, Student, Course, Grade)
│   ├── Schemas (Pydantic validation)
│   ├── Authentication (Passlib + Bcrypt)
│   └── API Endpoints (REST)
│
└── Frontend (CustomTkinter)
    ├── Login System (LoginWindow class)
    ├── API Client (HTTP communication)
    ├── QR Code Generator (qrcode library)
    ├── QR Code Scanner (OpenCV + pyzbar)
    ├── GUI Components (Custom widgets)
    └── Application Logic (Event handlers)
```

---

## Technologies Used

### Core Technologies
- **Python 3.13**: Main programming language
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **CustomTkinter**: Modern GUI framework
- **Requests**: HTTP library for API calls
- **Uvicorn**: ASGI server for FastAPI
- **MySQL**: Relational database (via SQLAlchemy)

### Authentication & Security 🔐
- **Passlib**: Password hashing library
- **Bcrypt**: Secure password encryption algorithm

### QR Code Features 📱
- **qrcode**: QR code generation
- **OpenCV (cv2)**: Camera access and image processing
- **pyzbar**: QR code scanning and decoding
- **Pillow (PIL)**: Image manipulation
- **NumPy**: Array operations for image processing

---

---

## New Features in v2.0

### 🔐 Authentication System
- **Password Hashing**: Uses bcrypt for secure password storage
- **Login Validation**: Server-side credential verification
- **Session Management**: User data passed to main application
- **Role-Based Access**: Admin/user roles (extensible)

**Key Concepts:**
- **Cryptography**: Password hashing with bcrypt
- **Security**: Never store plain text passwords
- **Context Manager**: Password context for hash verification

### 📱 QR Code System
- **QR Generation**: Automatic creation on student registration
- **QR Scanning**: Real-time camera-based scanning
- **Image Processing**: OpenCV for video capture and processing
- **Data Encoding**: Student codes embedded in QR codes

**Key Concepts:**
- **Computer Vision**: OpenCV for camera handling
- **Image Processing**: Frame manipulation and QR detection
- **File I/O**: Saving/loading QR code images
- **Threading**: Background processing for camera operations

---

## Conclusion

This project demonstrates comprehensive use of:
- **Core OOP principles** (inheritance, encapsulation, polymorphism)
- **Advanced Python features** (decorators, type hints, async/await, threading)
- **Database patterns** (ORM, relationships, constraints)
- **Security practices** (password hashing, authentication)
- **Computer vision** (QR code generation and scanning)
- **Modern GUI design** (custom widgets, dark theme, responsive layouts)
- **API design** (RESTful endpoints, validation, error handling)
- **GUI development** (custom widgets, event handling, layout)

The codebase follows modern Python best practices and design patterns, making it maintainable, scalable, and well-structured.
