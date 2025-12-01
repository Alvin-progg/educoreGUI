from pydantic import BaseModel, Field, validator, field_validator
from typing import List, Optional
from datetime import datetime
import re


class StudentBase(BaseModel):
    student_code: str = Field(..., min_length=1, max_length=20, description="Unique student code")
    name: str = Field(..., min_length=1, max_length=100, description="Student full name")
    course_code: str = Field(..., min_length=1, max_length=20, description="Course code")


class StudentCreate(StudentBase):
    teacher_id: Optional[int] = Field(None, description="Teacher ID")


class StudentUpdate(BaseModel):
    course_code: str = Field(..., min_length=1, max_length=20, description="New course code")


class StudentResponse(StudentBase):
    id: int
    teacher_id: Optional[int] = None
    gwa: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SubjectInfo(BaseModel):
    subject_code: str
    subject_name: str
    
    class Config:
        from_attributes = True


class CourseResponse(BaseModel):
    id: int
    code: str
    name: str
    subjects: List[SubjectInfo] = []
    
    class Config:
        from_attributes = True


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
        from_attributes = True


class GWAReportResponse(BaseModel):
    student_code: str
    name: str
    course_code: str
    gwa: float
    description: str
    formatted_gwa: str


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=8, description="Password")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError('Username can only contain letters, numbers, dots, hyphens, and underscores')
        if v.startswith('.') or v.startswith('-'):
            raise ValueError('Username cannot start with dot or hyphen')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


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
    student_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default="teacher")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError('Username can only contain letters, numbers, dots, hyphens, and underscores')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
