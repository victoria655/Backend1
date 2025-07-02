from flask import Blueprint, jsonify, request
from server.models.student import Student
from server.models.database import db
import os
import sys

# Add server directory to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

add_student_bp = Blueprint('add_student', __name__, url_prefix='/students/add')

@add_student_bp.route('/', methods=['POST'])
def add_student():
    data = request.get_json()
    firstname = data.get('firstname')
    middlename = data.get('middlename')
    lastname = data.get('lastname')
    admission_number = data.get('admission_number')
    grade = data.get('grade')

    if not all([firstname, middlename, lastname, admission_number, grade]):
        return jsonify({"error": "All fields (firstname, middlename, lastname, admission_number, grade) are required"}), 400

    # Check if admission_number is unique
    existing_student = Student.query.filter_by(admission_number=admission_number).first()
    if existing_student:
        return jsonify({"error": "Admission number already exists"}), 400

    try:
        new_student = Student(
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            admission_number=admission_number,
            grade=grade
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({
            "message": "Student added successfully",
            "firstname": new_student.firstname,
            "middlename": new_student.middlename,
            "lastname": new_student.lastname,
            "admission_number": new_student.admission_number,
            "grade": new_student.grade
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500