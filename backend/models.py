"""
SQLAlchemy ORM Models for EduCore System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    course_code = Column(String(20), ForeignKey("courses.code"), nullable=False)
    gwa = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(code='{self.student_code}', name='{self.name}', course='{self.course_code}')>"


class Course(Base):
    """Course model"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    students = relationship("Student", back_populates="course")
    subjects = relationship("CourseSubject", back_populates="course", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Course(code='{self.code}', name='{self.name}')>"


class CourseSubject(Base):
    """Course subjects mapping"""
    __tablename__ = "course_subjects"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_code = Column(String(20), ForeignKey("courses.code"), nullable=False)
    subject_code = Column(String(20), nullable=False)
    subject_name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for course_code and subject_code combination
    __table_args__ = (
        UniqueConstraint('course_code', 'subject_code', name='uq_course_subject'),
    )
    
    # Relationships
    course = relationship("Course", back_populates="subjects")
    
    def __repr__(self):
        return f"<CourseSubject(course='{self.course_code}', subject='{self.subject_code}')>"


class Grade(Base):
    """Grade model"""
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_code = Column(String(20), ForeignKey("students.student_code"), nullable=False)
    subject_code = Column(String(20), nullable=False)
    subject_name = Column(String(200), nullable=False)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Unique constraint for student and subject combination
    __table_args__ = (
        UniqueConstraint('student_code', 'subject_code', name='uq_student_subject'),
    )
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    
    def __repr__(self):
        return f"<Grade(student='{self.student_code}', subject='{self.subject_code}', grade={self.grade})>"


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), default="user")  # admin, user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
