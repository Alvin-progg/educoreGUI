"""
EduCore Academic Management System - Backend API
FastAPI server for managing students, courses, and grades
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import engine, get_db
from models import Base, Student, Course, Grade, CourseSubject
from schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    GradeCreate, GradeResponse,
    CourseResponse, GWAReportResponse
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduCore API",
    description="Academic Management System REST API",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database with predefined courses"""
    db = next(get_db())
    
    # Check if courses already exist
    existing_courses = db.query(Course).count()
    if existing_courses == 0:
        # BSIT Course and Subjects
        bsit = Course(code="BSIT", name="Bachelor of Science in Information Technology")
        db.add(bsit)
        db.flush()
        
        bsit_subjects = [
            CourseSubject(course_code="BSIT", subject_code="CS 131", subject_name="Computer Programming 1"),
            CourseSubject(course_code="BSIT", subject_code="GEd 109", subject_name="Purposive Communication"),
            CourseSubject(course_code="BSIT", subject_code="MATH 111", subject_name="Mathematics in the Modern World"),
            CourseSubject(course_code="BSIT", subject_code="PE 101", subject_name="Physical Education 1"),
            CourseSubject(course_code="BSIT", subject_code="NSTP 101", subject_name="National Service Training Program 1"),
            CourseSubject(course_code="BSIT", subject_code="CS 132", subject_name="Computer Programming 2"),
            CourseSubject(course_code="BSIT", subject_code="GEd 106", subject_name="Understanding the Self"),
        ]
        
        # BSCS Course and Subjects
        bscs = Course(code="BSCS", name="Bachelor of Science in Computer Science")
        db.add(bscs)
        db.flush()
        
        bscs_subjects = [
            CourseSubject(course_code="BSCS", subject_code="CS 101", subject_name="Introduction to Computing"),
            CourseSubject(course_code="BSCS", subject_code="CS 102", subject_name="Fundamentals of Programming"),
            CourseSubject(course_code="BSCS", subject_code="MATH 101", subject_name="Calculus 1"),
            CourseSubject(course_code="BSCS", subject_code="PHYS 101", subject_name="Physics for Computer Science"),
            CourseSubject(course_code="BSCS", subject_code="ENG 101", subject_name="Communication Skills"),
            CourseSubject(course_code="BSCS", subject_code="CS 201", subject_name="Data Structures and Algorithms"),
            CourseSubject(course_code="BSCS", subject_code="CS 202", subject_name="Object-Oriented Programming"),
        ]
        
        # BSBA Course and Subjects
        bsba = Course(code="BSBA", name="Bachelor of Science in Business Administration")
        db.add(bsba)
        db.flush()
        
        bsba_subjects = [
            CourseSubject(course_code="BSBA", subject_code="ACCT 101", subject_name="Fundamentals of Accounting"),
            CourseSubject(course_code="BSBA", subject_code="ECON 101", subject_name="Microeconomics"),
            CourseSubject(course_code="BSBA", subject_code="MGT 101", subject_name="Principles of Management"),
            CourseSubject(course_code="BSBA", subject_code="MKT 101", subject_name="Principles of Marketing"),
            CourseSubject(course_code="BSBA", subject_code="FIN 101", subject_name="Business Finance"),
        ]
        
        db.add_all(bsit_subjects + bscs_subjects + bsba_subjects)
        db.commit()
    
    db.close()


# ==================== Student Endpoints ====================

@app.get("/api/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    """Get all students with their GWA"""
    students = db.query(Student).order_by(Student.name).all()
    return students


@app.post("/api/students", response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Add a new student"""
    # Check if student code already exists
    existing = db.query(Student).filter(Student.student_code == student.student_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student code already exists")
    
    # Check if course exists
    course = db.query(Course).filter(Course.code == student.course_code).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    
    new_student = Student(
        student_code=student.student_code,
        name=student.name,
        course_code=student.course_code
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get("/api/students/{student_code}", response_model=StudentResponse)
def get_student(student_code: str, db: Session = Depends(get_db)):
    """Get a specific student by code"""
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/api/students/{student_code}", response_model=StudentResponse)
def update_student(student_code: str, student_update: StudentUpdate, db: Session = Depends(get_db)):
    """Update student's course"""
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = db.query(Course).filter(Course.code == student_update.course_code).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    
    student.course_code = student_update.course_code
    db.commit()
    db.refresh(student)
    return student


@app.delete("/api/students/{student_code}")
def delete_student(student_code: str, db: Session = Depends(get_db)):
    """Delete a student and all their grades"""
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete all grades for this student
    db.query(Grade).filter(Grade.student_code == student_code).delete()
    
    # Delete student
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


# ==================== Course Endpoints ====================

@app.get("/api/courses", response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    """Get all courses with their subjects"""
    courses = db.query(Course).order_by(Course.code).all()
    return courses


@app.get("/api/courses/{course_code}/subjects")
def get_course_subjects(course_code: str, db: Session = Depends(get_db)):
    """Get all subjects for a specific course"""
    subjects = db.query(CourseSubject).filter(
        CourseSubject.course_code == course_code
    ).order_by(CourseSubject.subject_code).all()
    return subjects


# ==================== Grade Endpoints ====================

@app.get("/api/grades/{student_code}", response_model=List[GradeResponse])
def get_student_grades(student_code: str, db: Session = Depends(get_db)):
    """Get all grades for a specific student"""
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    grades = db.query(Grade).filter(
        Grade.student_code == student_code
    ).order_by(Grade.subject_code).all()
    
    # Add formatted data
    result = []
    for grade in grades:
        result.append({
            "id": grade.id,
            "student_code": grade.student_code,
            "subject_code": grade.subject_code,
            "subject_name": grade.subject_name,
            "grade": grade.grade,
            "description": get_grade_description(grade.grade),
            "formatted_grade": format_grade(grade.grade)
        })
    
    return result


@app.post("/api/grades", response_model=GradeResponse)
def add_grade(grade_data: GradeCreate, db: Session = Depends(get_db)):
    """Add or update a grade for a student"""
    # Verify student exists
    student = db.query(Student).filter(Student.student_code == grade_data.student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate grade range
    if grade_data.grade < 1.0 or grade_data.grade > 5.0:
        raise HTTPException(status_code=400, detail="Grade must be between 1.0 and 5.0")
    
    # Check if grade already exists for this student and subject
    existing_grade = db.query(Grade).filter(
        Grade.student_code == grade_data.student_code,
        Grade.subject_code == grade_data.subject_code
    ).first()
    
    if existing_grade:
        # Update existing grade
        existing_grade.grade = grade_data.grade
        existing_grade.subject_name = grade_data.subject_name
        db.commit()
        db.refresh(existing_grade)
        grade_obj = existing_grade
    else:
        # Create new grade
        new_grade = Grade(
            student_code=grade_data.student_code,
            subject_code=grade_data.subject_code,
            subject_name=grade_data.subject_name,
            grade=grade_data.grade
        )
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        grade_obj = new_grade
    
    # Update student's GWA
    update_student_gwa(grade_data.student_code, db)
    
    return {
        "id": grade_obj.id,
        "student_code": grade_obj.student_code,
        "subject_code": grade_obj.subject_code,
        "subject_name": grade_obj.subject_name,
        "grade": grade_obj.grade,
        "description": get_grade_description(grade_obj.grade),
        "formatted_grade": format_grade(grade_obj.grade)
    }


# ==================== Report Endpoints ====================

@app.get("/api/gwa-report", response_model=List[GWAReportResponse])
def get_gwa_report(db: Session = Depends(get_db)):
    """Get GWA report for all students"""
    students = db.query(Student).order_by(Student.name).all()
    
    result = []
    for student in students:
        result.append({
            "student_code": student.student_code,
            "name": student.name,
            "course_code": student.course_code,
            "gwa": student.gwa,
            "description": get_grade_description(student.gwa),
            "formatted_gwa": format_grade(student.gwa)
        })
    
    return result


# ==================== Helper Functions ====================

def update_student_gwa(student_code: str, db: Session):
    """Calculate and update GWA for a student"""
    from sqlalchemy import func
    
    avg_grade = db.query(func.avg(Grade.grade)).filter(
        Grade.student_code == student_code
    ).scalar()
    
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if student:
        student.gwa = round(float(avg_grade), 2) if avg_grade else 0.0
        db.commit()


def get_grade_description(grade: float) -> str:
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


def format_grade(grade: float) -> str:
    """Format grade for display"""
    if grade == 0:
        return "N/A"
    return f"{grade:.2f}"


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "EduCore Academic Management System API",
        "version": "2.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
