# EduCore: Academic Management System v2.0

A modernized academic management system built with Python, FastAPI, MySQL, and CustomTkinter. This system manages students, courses, and grades with automatic GWA (General Weighted Average) calculation.

## 🚀 Features

- **🔐 Secure Login System**: User authentication with encrypted passwords
  - Default admin account (username: admin, password: admin123)
  - Bcrypt password hashing
  - Role-based access (admin/user)
- **Student Management**: Add, update, delete, and view student records
- **QR Code Integration**: 📱 Automatic QR code generation for students
  - Generate QR codes when adding students
  - Scan QR codes for instant student lookup
  - View and print student QR codes
- **Course Management**: Predefined courses (BSIT, BSCS, BSBA) with their subjects
- **Grade Management**: Record grades for subjects and automatically calculate GWA
- **GWA Reports**: Generate comprehensive reports showing all students' academic performance
- **Modern GUI**: Beautiful desktop interface built with CustomTkinter
- **REST API**: FastAPI backend with full CRUD operations
- **Database Persistence**: MySQL database with SQLAlchemy ORM

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7+ or 8.0+
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
cd educoreGUI
```

### 2. Create Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Setup MySQL Database

Open MySQL and create the database:

```sql
CREATE DATABASE educore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env` and update with your MySQL credentials:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=educore_db
DB_USER=root
DB_PASSWORD=your_password_here
```

### 6. Initialize Database Tables

The database tables will be automatically created when you start the FastAPI server for the first time. The system will also populate predefined courses and subjects.

## 🚀 Running the Application

### Start the Backend Server (Terminal 1)

```powershell
cd backend
python main.py
```

Or using uvicorn directly:
```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Start the GUI Application (Terminal 2)

```powershell
cd frontend
python gui.py
```

**🔐 Login Required:** A login window will appear. Use default credentials:
- **Username:** `admin`
- **Password:** `admin123`

For detailed login instructions, see [LOGIN_GUIDE.md](LOGIN_GUIDE.md)

## 📁 Project Structure

```
educoreGUI/
├── backend/
│   ├── main.py           # FastAPI application and endpoints
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy ORM models (includes User)
│   └── schemas.py        # Pydantic schemas for validation
├── frontend/
│   ├── gui.py           # CustomTkinter GUI with login
│   ├── generate_qr_for_existing.py  # QR code generator script
│   └── test_qr.py       # QR code test script
├── qr_codes/            # Generated QR codes
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Example environment configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LOGIN_GUIDE.md      # Login system documentation
├── QR_QUICK_START.md   # QR code feature guide
└── QR_CODE_FEATURE.md  # Detailed QR documentation
```

## 📚 Database Schema

### Tables

1. **users** 🔐 NEW!
   - id (Primary Key)
   - username (Unique)
   - password_hash (Encrypted)
   - full_name
   - role (admin/user)
   - is_active (Boolean)
   - created_at, last_login

2. **students**
   - id (Primary Key)
   - student_code (Unique)
   - name
   - course_code (Foreign Key to courses)
   - gwa (Calculated automatically)
   - created_at, updated_at

2. **courses**
   - id (Primary Key)
   - code (Unique)
   - name
   - created_at

3. **course_subjects**
   - id (Primary Key)
   - course_code (Foreign Key to courses)
   - subject_code
   - subject_name
   - created_at

4. **grades**
   - id (Primary Key)
   - student_code (Foreign Key to students)
   - subject_code
   - subject_name
   - grade (1.0 to 5.0)
   - created_at, updated_at

## 🎓 Grading System

The system uses the Philippine grading scale:

- **1.0** = Excellent (97-100%)
- **1.25-1.75** = Very Good (90-96%)
- **2.0-2.5** = Good (83-89%)
- **2.75-3.0** = Satisfactory (75-82%)
- **3.0+** = Failed

## 🔌 API Endpoints

### Students
- `GET /api/students` - Get all students
- `POST /api/students` - Add new student
- `GET /api/students/{code}` - Get specific student
- `PUT /api/students/{code}` - Update student course
- `DELETE /api/students/{code}` - Delete student

### Courses
- `GET /api/courses` - Get all courses with subjects
- `GET /api/courses/{code}/subjects` - Get subjects for a course

### Grades
- `GET /api/grades/{student_code}` - Get all grades for a student
- `POST /api/grades` - Add or update a grade

### Reports
- `GET /api/gwa-report` - Get GWA report for all students

## 💡 Usage Guide

### Adding a Student
1. Go to "Students" tab
2. Fill in Student Code, Full Name, and Course
3. Click "Add Student"

### Recording Grades
1. Go to "Grades" tab
2. Enter Student Code, Subject Code, Subject Name, and Grade (1.0-5.0)
3. Click "Submit Grade"
4. GWA is automatically calculated

### Viewing Reports
1. Go to "Reports" tab
2. Click "Refresh Report" to see all students with their GWA
3. View statistics: Total Students, Average GWA, and Excellent performers

### Updating Student Course
1. Go to "Students" tab
2. In the "Update Student Course" section, enter Student Code
3. Select new course
4. Click "Update Course"

## 🎨 Predefined Courses

### BSIT - Bachelor of Science in Information Technology
- CS 131 - Computer Programming 1
- GEd 109 - Purposive Communication
- MATH 111 - Mathematics in the Modern World
- PE 101 - Physical Education 1
- NSTP 101 - National Service Training Program 1
- CS 132 - Computer Programming 2
- GEd 106 - Understanding the Self

### BSCS - Bachelor of Science in Computer Science
- CS 101 - Introduction to Computing
- CS 102 - Fundamentals of Programming
- MATH 101 - Calculus 1
- PHYS 101 - Physics for Computer Science
- ENG 101 - Communication Skills
- CS 201 - Data Structures and Algorithms
- CS 202 - Object-Oriented Programming

### BSBA - Bachelor of Science in Business Administration
- ACCT 101 - Fundamentals of Accounting
- ECON 101 - Microeconomics
- MGT 101 - Principles of Management
- MKT 101 - Principles of Marketing
- FIN 101 - Business Finance

## 🔧 Troubleshooting

### Database Connection Error
- Ensure MySQL server is running
- Check credentials in `.env` file
- Verify database `educore_db` exists

### Port Already in Use
- Change port in `backend/main.py` (default: 8000)
- Or stop the process using the port

### GUI Not Connecting to Backend
- Ensure backend server is running on port 8000
- Check `frontend/gui.py` API_URL configuration

### Module Not Found Errors
- Activate virtual environment
- Run `pip install -r requirements.txt`

## 📱 QR Code Features (NEW!)

EduCore now includes comprehensive QR code functionality:

### Automatic QR Code Generation
- QR codes are automatically generated when adding new students
- QR codes stored in `qr_codes/` directory
- Each QR code contains the student's unique code

### QR Code Scanner
- **Location**: Grades tab → "📷 Scan QR" button
- Scan student QR codes with your camera
- Auto-fills student code for instant lookup
- Press ESC to cancel scanning

### View QR Codes
- **Location**: Students tab → "📱 View QR" button
- View any student's QR code
- Print QR codes for student ID cards
- Auto-generates missing QR codes

### Generate QR Codes for Existing Students
```powershell
cd frontend
python generate_qr_for_existing.py
```

**For detailed QR code documentation, see:**
- `QR_QUICK_START.md` - Quick start guide
- `QR_CODE_FEATURE.md` - Detailed feature documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details

## 🆕 What's New in v2.0

- **🔐 Secure Login System**: User authentication with bcrypt password hashing
- **QR Code Integration**: Automatic generation and scanning of student QR codes 📱
- **FastAPI Backend**: Upgraded from Flask to FastAPI
- **SQLAlchemy ORM**: Proper database models and relationships
- **Modern GUI**: Enhanced CustomTkinter interface with better UX
- **Multiple Courses**: Support for BSIT, BSCS, and BSBA
- **Automatic GWA**: Real-time GWA calculation
- **Better Error Handling**: Comprehensive validation and error messages
- **Statistics Dashboard**: Visual reports with key metrics
- **Course Reference**: Built-in course catalog with all subjects

## 📝 License

This project is for educational purposes.

## 👨‍💻 Development

### Adding New Courses
Edit `backend/main.py` in the `startup_event()` function to add more courses and subjects.

### Customizing the GUI
Modify `frontend/gui.py` to customize colors, fonts, and layout.

### API Documentation
Visit http://localhost:8000/docs when the backend is running for interactive API documentation.

## 🤝 Support

For issues or questions, please check:
1. Database is running and accessible
2. All dependencies are installed
3. Environment variables are configured
4. Both backend and frontend are running

---

**EduCore v2.0** - Modern Academic Management Made Easy 🎓
