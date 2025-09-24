from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from models import Student, Course, Grade, GradeSystem

load_dotenv()

app = Flask(__name__)
CORS(app)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'educore'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                autocommit=True
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

db_manager = DatabaseManager()

# Student Routes
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY name")
        students = cursor.fetchall()
        cursor.close()
        return jsonify(students)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    try:
        data = request.json
        student_code = data['student_code']
        name = data['name']
        course_code = data['course_code']

        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        # Check if student code already exists
        cursor.execute("SELECT student_code FROM students WHERE student_code = %s", (student_code,))
        if cursor.fetchone():
            cursor.close()
            return jsonify({'error': 'Student code already exists'}), 400

        query = "INSERT INTO students (student_code, name, course_code) VALUES (%s, %s, %s)"
        cursor.execute(query, (student_code, name, course_code))
        cursor.close()
        
        return jsonify({'message': 'Student added successfully', 'student_code': student_code})
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<student_code>', methods=['DELETE'])
def delete_student(student_code):
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_code = %s", (student_code,))
        
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({'error': 'Student not found'}), 404
            
        cursor.close()
        return jsonify({'message': 'Student deleted successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<student_code>', methods=['PUT'])
def update_student(student_code):
    try:
        data = request.json
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        query = "UPDATE students SET course_code = %s WHERE student_code = %s"
        cursor.execute(query, (data['course_code'], student_code))
        
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({'error': 'Student not found'}), 404
            
        cursor.close()
        return jsonify({'message': 'Student updated successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Course Routes
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get courses with their subjects
        query = """
        SELECT c.code, c.name, cs.subject_code, cs.subject_name
        FROM courses c
        LEFT JOIN course_subjects cs ON c.code = cs.course_code
        ORDER BY c.code, cs.subject_code
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Group subjects by course
        courses_dict = {}
        for row in results:
            course_code = row['code']
            if course_code not in courses_dict:
                courses_dict[course_code] = {
                    'code': course_code,
                    'name': row['name'],
                    'subjects': []
                }
            
            if row['subject_code']:  # If course has subjects
                courses_dict[course_code]['subjects'].append({
                    'subject_code': row['subject_code'],
                    'subject_name': row['subject_name']
                })
        
        cursor.close()
        return jsonify(list(courses_dict.values()))
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Grade Routes
@app.route('/api/grades/<student_code>', methods=['GET'])
def get_student_grades(student_code):
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT g.*, s.name as student_name, s.course_code
        FROM grades g
        JOIN students s ON g.student_code = s.student_code
        WHERE g.student_code = %s
        ORDER BY g.subject_code
        """
        cursor.execute(query, (student_code,))
        grades = cursor.fetchall()
        cursor.close()
        
        # Add grade descriptions
        for grade in grades:
            grade['description'] = GradeSystem.get_description(grade['grade'])
            grade['formatted_grade'] = GradeSystem.format_grade(grade['grade'])
        
        return jsonify(grades)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/grades', methods=['POST'])
def add_grade():
    try:
        data = request.json
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        # Insert or update grade
        query = """
        INSERT INTO grades (student_code, subject_code, subject_name, grade)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE grade = VALUES(grade), updated_at = CURRENT_TIMESTAMP
        """
        cursor.execute(query, (data['student_code'], data['subject_code'], 
                             data['subject_name'], data['grade']))
        
        # Update student's GWA
        update_gwa(data['student_code'])
        cursor.close()
        
        return jsonify({'message': 'Grade added successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gwa-report', methods=['GET'])
def get_gwa_report():
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT student_code, name, course_code, gwa
        FROM students
        ORDER BY name
        """
        cursor.execute(query)
        students = cursor.fetchall()
        
        # Add grade descriptions
        for student in students:
            student['description'] = GradeSystem.get_description(student['gwa'])
            student['formatted_gwa'] = GradeSystem.format_grade(student['gwa'])
        
        cursor.close()
        return jsonify(students)
    except Error as e:
        return jsonify({'error': str(e)}), 500

def update_gwa(student_code):
    """Update the GWA for a specific student"""
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        # Calculate average grade
        cursor.execute("""
            SELECT AVG(grade) as avg_grade 
            FROM grades 
            WHERE student_code = %s
        """, (student_code,))
        
        result = cursor.fetchone()
        avg_grade = result[0] if result[0] else 0.0
        
        # Update student's GWA
        cursor.execute("""
            UPDATE students 
            SET gwa = %s 
            WHERE student_code = %s
        """, (avg_grade, student_code))
        
        cursor.close()
    except Error as e:
        print(f"Error updating GWA: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)