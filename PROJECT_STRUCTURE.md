# EduCore v2.0 - Project Structure

```
educoreGUI/
│
├── 📄 START_HERE.txt          ← Read this first!
├── 📄 README.md               ← Full documentation
├── 📄 INSTALL.md              ← Installation guide
├── 📄 requirements.txt        ← Python dependencies
├── 📄 .env                    ← Your config (edit with MySQL credentials)
├── 📄 .env.example            ← Template for .env
├── 📄 .gitignore              ← Git ignore rules
│
├── 🔧 quickstart.ps1          ← One-click setup (run first time)
├── 🔧 setup_database.py       ← Database initialization
├── 🔧 start_backend.ps1       ← Start API server
├── 🔧 start_frontend.ps1      ← Start GUI app
│
├── 📁 backend/                ← FastAPI REST API
│   ├── main.py                   → API endpoints & logic
│   ├── database.py               → Database connection
│   ├── database_alternative.py   → Alternative DB config
│   ├── models.py                 → SQLAlchemy ORM models
│   ├── schemas.py                → Pydantic validation
│   └── __init__.py
│
├── 📁 frontend/               ← CustomTkinter GUI
│   ├── gui.py                    → Main application
│   └── __init__.py
│
└── 📁 OLD_*.py                ← Deprecated files (reference only)
```

## 🚀 Quick Start Commands

### First Time Setup:
```powershell
.\quickstart.ps1
```

### Start Application:
```powershell
# Terminal 1
.\start_backend.ps1

# Terminal 2
.\start_frontend.ps1
```

### Manual Commands:
```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python setup_database.py

# Run
cd backend && python main.py
cd frontend && python gui.py
```

## 📋 File Purposes

### Configuration Files
- `.env` - Your database credentials (KEEP SECRET!)
- `.env.example` - Template for .env file
- `requirements.txt` - Python packages needed

### Backend Files
- `main.py` - API routes, business logic, startup events
- `database.py` - SQLAlchemy connection setup
- `models.py` - Database table definitions (Student, Course, Grade)
- `schemas.py` - Request/response validation with Pydantic

### Frontend Files
- `gui.py` - Complete GUI application with CustomTkinter

### Utility Scripts
- `setup_database.py` - Creates database and tests connection
- `start_backend.ps1` - Convenient backend startup
- `start_frontend.ps1` - Convenient GUI startup
- `quickstart.ps1` - One-command setup for first time

## 🔑 Key Features by File

### backend/main.py
- Student CRUD operations
- Grade management
- GWA calculation
- Course & subject management
- API documentation (FastAPI)

### frontend/gui.py
- Modern tabbed interface
- Student management forms
- Grade recording
- GWA reports with statistics
- Course reference viewer

### backend/models.py
- Student table (with GWA)
- Course table
- CourseSubject table
- Grade table
- Automatic timestamps

## 🎯 What Each Component Does

```
┌─────────────┐         ┌──────────────┐         ┌──────────┐
│   GUI       │ HTTP    │   FastAPI    │  SQL    │  MySQL   │
│ (frontend/) │◄───────►│  (backend/)  │◄───────►│ Database │
│             │ Requests│              │ Queries │          │
└─────────────┘         └──────────────┘         └──────────┘
```

### Data Flow Example: Adding a Student
1. User fills form in `frontend/gui.py`
2. GUI sends POST request to `http://localhost:8000/api/students`
3. `backend/main.py` receives request
4. Validates with `schemas.py`
5. Creates Student using `models.py`
6. Saves to MySQL via `database.py`
7. Returns success to GUI
8. GUI refreshes student list

## 📊 Database Tables Created

When you run the backend for the first time:

1. **students** - Student records with GWA
2. **courses** - BSIT, BSCS, BSBA
3. **course_subjects** - All subjects per course
4. **grades** - Student grades per subject

## 🔗 Important URLs

- Frontend GUI: Desktop application (no URL)
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- API JSON: http://localhost:8000/openapi.json

## 📱 Tab Structure in GUI

```
EduCore Application
├── 👥 Students Tab
│   ├── Add Student Form
│   ├── Update Course Form
│   └── Students List (Treeview)
│
├── 📝 Grades Tab
│   ├── Add Grade Form
│   ├── Search Student Form
│   └── Grades List (Treeview)
│
├── 📊 Reports Tab
│   ├── Statistics Cards
│   └── GWA Report (Treeview)
│
└── 📚 Courses Tab
    └── Course & Subject Reference
```

## 🎓 Default Courses Loaded

The system comes with:
- **BSIT** (7 subjects)
- **BSCS** (7 subjects)
- **BSBA** (5 subjects)

All automatically loaded on first backend start!

## 💡 Tips

1. Always start backend BEFORE frontend
2. Keep both terminals open while using the app
3. Check http://localhost:8000/docs for API testing
4. `.env` file must have correct MySQL password
5. Virtual environment should be activated

## 🐛 Common Issues

| Problem | File to Check |
|---------|--------------|
| Can't connect to MySQL | `.env` |
| API not starting | `backend/main.py` |
| GUI not opening | `frontend/gui.py` |
| Database errors | `backend/database.py` |
| Missing tables | Run `python setup_database.py` |

---

**Ready to start?** Open START_HERE.txt for quick commands!
