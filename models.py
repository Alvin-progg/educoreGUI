from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Student:
    student_code: str
    name: str
    course_code: str
    gwa: float = 0.0
    id: Optional[int] = None

    def to_dict(self):
        return {
            'id': self.id,
            'student_code': self.student_code,
            'name': self.name,
            'course_code': self.course_code,
            'gwa': self.gwa
        }

@dataclass
class Course:
    code: str
    name: str
    subjects: List[Dict] = None
    id: Optional[int] = None

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'subjects': self.subjects or []
        }

@dataclass
class Grade:
    student_code: str
    subject_code: str
    subject_name: str
    grade: float
    id: Optional[int] = None

    def to_dict(self):
        return {
            'id': self.id,
            'student_code': self.student_code,
            'subject_code': self.subject_code,
            'subject_name': self.subject_name,
            'grade': self.grade
        }

class GradeSystem:
    @staticmethod
    def get_description(grade: float) -> str:
        """Convert numeric grade to description based on Philippine grading system"""
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

    @staticmethod
    def format_grade(grade: float) -> str:
        """Format grade to show 2 decimal places"""
        if grade == 0:
            return "N/A"
        return f"{grade:.2f}"