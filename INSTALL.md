# EduCore Installation and Setup Guide

## Quick Installation Steps

### 1. Prerequisites Check
Make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ MySQL Server running
- ✅ pip package manager

### 2. Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt
```

### 3. MySQL Setup

#### Option A: Using MySQL Command Line
```sql
CREATE DATABASE educore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Click "Create new schema" icon
4. Name it: `educore_db`
5. Character set: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click Apply

### 4. Configure Environment Variables

```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env file with your MySQL credentials
notepad .env
```

Update these values in `.env`:
```env
DB_HOST=localhost          # Your MySQL host
DB_PORT=3306              # MySQL port (usually 3306)
DB_NAME=educore_db        # Database name
DB_USER=root              # Your MySQL username
DB_PASSWORD=your_password # Your MySQL password
```

### 5. Setup Database

Run the database setup script:
```powershell
python setup_database.py
```

This will:
- Create the database if it doesn't exist
- Test the connection
- Confirm everything is ready

### 6. Start the Application

#### Option A: Using PowerShell Scripts (Recommended)

**Terminal 1 - Backend:**
```powershell
.\start_backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\start_frontend.ps1
```

#### Option B: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
python main.py
```
Wait for message: "Uvicorn running on http://0.0.0.0:8000"

**Terminal 2 - Frontend:**
```powershell
cd frontend
python gui.py
```

### 7. Verify Installation

1. Backend API: Open http://localhost:8000/docs in your browser
2. GUI Application: The desktop app should open automatically
3. Test by adding a student and recording grades

## Common Issues and Solutions

### Issue: "mysqlclient" installation fails

**Solution for Windows:**
```powershell
pip install mysqlclient==2.2.1
```

If that fails, install MySQL Connector instead:
```powershell
pip uninstall mysqlclient
pip install mysql-connector-python
```

Then update `backend/database.py`, line 16:
```python
# Change this:
DATABASE_URL = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# To this:
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

### Issue: "Can't connect to MySQL server"

**Solutions:**
1. Check if MySQL is running:
   ```powershell
   Get-Service -Name "MySQL*"
   ```
2. Verify credentials in `.env`
3. Test connection:
   ```powershell
   mysql -u root -p
   ```

### Issue: Port 8000 already in use

**Solution:**
Change the port in `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Changed from 8000
        reload=True
    )
```

Also update `frontend/gui.py`:
```python
def __init__(self, base_url="http://localhost:8001/api"):  # Changed from 8000
```

### Issue: CustomTkinter not rendering properly

**Solution:**
```powershell
pip uninstall customtkinter
pip install customtkinter==5.2.1
```

### Issue: Virtual environment activation restricted

**Solution:**
Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Testing the Installation

### Test 1: Add a Student
1. Open GUI
2. Go to "Students" tab
3. Add student:
   - Code: 24-49051
   - Name: John Doe
   - Course: BSIT
4. Click "Add Student"

### Test 2: Record Grades
1. Go to "Grades" tab
2. Add grade:
   - Student Code: 24-49051
   - Subject Code: CS 131
   - Subject Name: Computer Programming 1
   - Grade: 1.25
3. Click "Submit Grade"

### Test 3: View Reports
1. Go to "Reports" tab
2. Click "Refresh Report"
3. You should see John Doe with GWA of 1.25

### Test 4: API Endpoints
Open browser and test:
- http://localhost:8000 - Root endpoint
- http://localhost:8000/docs - API documentation
- http://localhost:8000/api/students - Students list (JSON)
- http://localhost:8000/api/courses - Courses list (JSON)

## Development Tips

### Debugging Backend
Enable SQL query logging in `backend/database.py`:
```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True  # Change to True to see SQL queries
)
```

### Debugging Frontend
Add print statements in `frontend/gui.py`:
```python
def add_student(self):
    print(f"Adding student: {student_code}, {name}, {course}")
    # ... rest of code
```

### Reset Database
To start fresh:
```sql
DROP DATABASE educore_db;
CREATE DATABASE educore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Then restart the backend server.

## Next Steps

After successful installation:
1. ✅ Read the README.md for usage guide
2. ✅ Explore the API docs at http://localhost:8000/docs
3. ✅ Check the "Courses" tab to see predefined courses
4. ✅ Try all features: Add students, record grades, view reports
5. ✅ Customize courses in `backend/main.py` if needed

## Support Resources

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Project Structure**: See README.md
- **Grade Scale**: See README.md section "Grading System"
- **Database Schema**: See README.md section "Database Schema"

---

**Installation complete!** 🎉 You're ready to use EduCore!
