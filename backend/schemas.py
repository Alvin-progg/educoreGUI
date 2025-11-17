"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


# ==================== Student Schemas ====================

class StudentBase(BaseModel):
    student_code: str = Field(..., min_length=1, max_length=20, description="Unique student code")
    name: str = Field(..., min_length=1, max_length=100, description="Student full name")
    course_code: str = Field(..., min_length=1, max_length=20, description="Course code")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    course_code: str = Field(..., min_length=1, max_length=20, description="New course code")


class StudentResponse(StudentBase):
    id: int
    gwa: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # Pydantic v2


# ==================== Course Schemas ====================

class SubjectInfo(BaseModel):
    subject_code: str
    subject_name: str
    
    class Config:
        from_attributes = True  # Pydantic v2


class CourseResponse(BaseModel):
    id: int
    code: str
    name: str
    subjects: List[SubjectInfo] = []
    
    class Config:
        from_attributes = True  # Pydantic v2


# ==================== Grade Schemas ====================

class GradeCreate(BaseModel):
    student_code: str = Field(..., description="Student code")
    subject_code: str = Field(..., min_length=1, max_length=20, description="Subject code")
    subject_name: str = Field(..., min_length=1, max_length=200, description="Subject name")
    grade: float = Field(..., ge=1.0, le=5.0, description="Grade between 1.0 and 5.0")
    
    @validator('grade')
    def validate_grade(cls, v):
        if v < 1.0 or v > 5.0:
            raise ValueError('Grade must be between 1.0 and 5.0')
        return round(v, 2)


class GradeResponse(BaseModel):
    id: int
    student_code: str
    subject_code: str
    subject_name: str
    grade: float
    description: str
    formatted_grade: str
    
    class Config:
        from_attributes = True  # Pydantic v2


# ==================== Report Schemas ====================

class GWAReportResponse(BaseModel):
    student_code: str
    name: str
    course_code: str
    gwa: float
    description: str
    formatted_gwa: str


# ==================== Auth Schemas ====================

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=4, description="Password")


class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: Optional[datetime]
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
