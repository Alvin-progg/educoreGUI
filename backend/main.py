from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import engine, get_db
from models import Base, Student, Course, Grade, CourseSubject, User
from schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    GradeCreate, GradeResponse,
    CourseResponse, GWAReportResponse,
    LoginRequest, LoginResponse, UserResponse
)
from passlib.context import CryptContext
from datetime import datetime

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="EduCore API",
    description="Academic Management System REST API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    
    existing_courses = db.query(Course).count()
    if existing_courses == 0:
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
    
    existing_users = db.query(User).count()
    if existing_users == 0:
        default_admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            full_name="System Administrator",
            role="admin",
            is_active=True
        )
        db.add(default_admin)
        db.commit()
        print("=" * 60)
        print("DEFAULT ADMIN USER CREATED")
        print("Username: admin")
        print("Password: admin123")
        print("PLEASE CHANGE THE PASSWORD AFTER FIRST LOGIN!")
        print("=" * 60)
    
    db.close()


@app.post("/api/auth/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        return LoginResponse(
            success=False,
            message="Invalid username or password"
        )
    
    if not user.is_active:
        return LoginResponse(
            success=False,
            message="Account is deactivated"
        )
    
    if not verify_password(credentials.password, user.password_hash):
        return LoginResponse(
            success=False,
            message="Invalid username or password"
        )
    
    user.last_login = datetime.now()
    db.commit()
    
    return LoginResponse(
        success=True,
        message="Login successful",
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role
        }
    )


@app.get("/api/auth/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.username).all()
    return users


@app.get("/api/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.name).all()
    return students


@app.post("/api/students", response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.student_code == student.student_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student code already exists")
    
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
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/api/students/{student_code}", response_model=StudentResponse)
def update_student(student_code: str, student_update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    course = db.query(Course).filter(Course.code == student_update.course_code).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    
    student.course_code = student_update.course_code
    db.commit()
    db.refresh(student)
    return student


@app.delete("/api/students/{student_code}")
def delete_student(student_code: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.query(Grade).filter(Grade.student_code == student_code).delete()
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


@app.get("/api/courses", response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).order_by(Course.code).all()
    return courses


@app.get("/api/courses/{course_code}/subjects")
def get_course_subjects(course_code: str, db: Session = Depends(get_db)):
    subjects = db.query(CourseSubject).filter(
        CourseSubject.course_code == course_code
    ).order_by(CourseSubject.subject_code).all()
    return subjects


@app.get("/api/grades/{student_code}", response_model=List[GradeResponse])
def get_student_grades(student_code: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    grades = db.query(Grade).filter(
        Grade.student_code == student_code
    ).order_by(Grade.subject_code).all()
    
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
    student = db.query(Student).filter(Student.student_code == grade_data.student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if grade_data.grade < 1.0 or grade_data.grade > 5.0:
        raise HTTPException(status_code=400, detail="Grade must be between 1.0 and 5.0")
    
    existing_grade = db.query(Grade).filter(
        Grade.student_code == grade_data.student_code,
        Grade.subject_code == grade_data.subject_code
    ).first()
    
    if existing_grade:
        existing_grade.grade = grade_data.grade
        existing_grade.subject_name = grade_data.subject_name
        db.commit()
        db.refresh(existing_grade)
        grade_obj = existing_grade
    else:
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


@app.get("/api/gwa-report", response_model=List[GWAReportResponse])
def get_gwa_report(db: Session = Depends(get_db)):
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


def update_student_gwa(student_code: str, db: Session):
    from sqlalchemy import func
    
    avg_grade = db.query(func.avg(Grade.grade)).filter(
        Grade.student_code == student_code
    ).scalar()
    
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if student:
        student.gwa = round(float(avg_grade), 2) if avg_grade else 0.0
        db.commit()


def get_grade_description(grade: float) -> str:
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
    if grade == 0:
        return "N/A"
    return f"{grade:.2f}"


@app.get("/api/analytics/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    from sqlalchemy import func
    
    total_students = db.query(Student).count()
    total_courses = db.query(Course).count()
    total_grades = db.query(Grade).count()
    
    avg_gwa = db.query(func.avg(Student.gwa)).filter(Student.gwa > 0).scalar()
    avg_gwa = round(float(avg_gwa), 2) if avg_gwa else 0.0
    
    students_per_course = db.query(
        Student.course_code,
        func.count(Student.id).label('count')
    ).group_by(Student.course_code).all()
    
    course_distribution = [
        {"course": course, "count": count}
        for course, count in students_per_course
    ]
    
    grade_ranges = [
        {"range": "1.0 (Excellent)", "min": 1.0, "max": 1.0},
        {"range": "1.25-1.75 (Very Good)", "min": 1.25, "max": 1.75},
        {"range": "2.0-2.5 (Good)", "min": 2.0, "max": 2.5},
        {"range": "2.75-3.0 (Satisfactory)", "min": 2.75, "max": 3.0},
        {"range": "3.0+ (Failed)", "min": 3.0, "max": 5.0}
    ]
    
    grade_distribution = []
    for grade_range in grade_ranges:
        count = db.query(Grade).filter(
            Grade.grade >= grade_range["min"],
            Grade.grade <= grade_range["max"]
        ).count()
        grade_distribution.append({
            "range": grade_range["range"],
            "count": count
        })
    
    top_performers = db.query(Student).filter(
        Student.gwa > 0,
        Student.gwa <= 1.75
    ).order_by(Student.gwa).limit(10).all()
    
    top_students = [
        {
            "student_code": s.student_code,
            "name": s.name,
            "course_code": s.course_code,
            "gwa": round(s.gwa, 2)
        }
        for s in top_performers
    ]
    
    gwa_per_course = db.query(
        Student.course_code,
        func.avg(Student.gwa).label('avg_gwa')
    ).filter(Student.gwa > 0).group_by(Student.course_code).all()
    
    course_performance = [
        {"course": course, "avg_gwa": round(float(avg), 2)}
        for course, avg in gwa_per_course
    ]
    
    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_grades": total_grades,
        "overall_avg_gwa": avg_gwa,
        "course_distribution": course_distribution,
        "grade_distribution": grade_distribution,
        "top_students": top_students,
        "course_performance": course_performance
    }


@app.get("/")
def root():
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
