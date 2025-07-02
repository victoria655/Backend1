from flask import Blueprint, jsonify, request
from server.models.database import db
from server.models.fee import Fee
from server.models.student import Student
from datetime import datetime
import os
import sys

# Add server directory to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

students_fees_bp = Blueprint('students_fees', __name__, url_prefix='/students/fees')

@students_fees_bp.route('/')
def list_students_with_fees():
    students = Student.query.all()
    result = []
    for student in students:
        total_paid = sum(f.amount for f in student.fees)
        required = 10000
        overpayment = max(total_paid - required, 0)
        deficit = max(required - total_paid, 0)
        
        result.append({
            "id": student.id,
            "firstname": student.firstname,
            "middlename": student.middlename,
            "lastname": student.lastname,
            "admission_number": student.admission_number,
            "grade": student.grade,
            "amount": total_paid,
            "overpayment": overpayment,
            "deficit": deficit,
        })
    return jsonify(result)

@students_fees_bp.route('/<string:admission_number>')
def get_student_fees(admission_number):
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    total_paid = sum(f.amount for f in student.fees)
    required = 10000
    overpayment = max(total_paid - required, 0)
    deficit = max(required - total_paid, 0)
    
    return jsonify({
        "id": student.id,
        "firstname": student.firstname,
        "middlename": student.middlename,
        "lastname": student.lastname,
        "admission_number": student.admission_number,
        "grade": student.grade,
        "amount": total_paid,
        "overpayment": overpayment,
        "deficit": deficit,
    })

@students_fees_bp.route('/<string:admission_number>/update_payment', methods=['PATCH'])
def update_payment_status(admission_number):
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    data = request.get_json()
    amount = data.get('amount')
    date_str = data.get('date')

    if not amount or not date_str:
        return jsonify({"error": "Amount and date are required"}), 400

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    new_fee = Fee(
        student_id=student.id,
        amount=amount,
        date=date
    )

    try:
        db.session.add(new_fee)
        db.session.commit()
        db.session.refresh(student)
        return jsonify({
            "message": "Payment status updated successfully",
            "admission_number": admission_number,
            "amount": student.total_fee_paid,
            "date": date.isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@students_fees_bp.route('/<string:admission_number>/fees', methods=['POST'])
def add_student_fee(admission_number):
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    data = request.get_json()
    amount = data.get('amount')
    date_str = data.get('date')

    if not amount or not date_str:
        return jsonify({"error": "Amount and date are required"}), 400

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    new_fee = Fee(amount=amount, date=date, student_id=student.id)

    try:
        db.session.add(new_fee)
        db.session.commit()
        return jsonify({
            "message": "Fee added successfully",
            "admission_number": student.admission_number,
            "student_firstname": student.firstname,
            "student_middlename": student.middlename,
            "student_lastname": student.lastname,
            "amount": new_fee.amount,
            "date": new_fee.date.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@students_fees_bp.route('/delete_fee_by_student_id/<int:student_id>', methods=['DELETE'])
def delete_fee_by_student_id(student_id):
    fee = Fee.query.filter_by(student_id=student_id).first()
    if not fee:
        return jsonify({"error": "Fee record not found for this student"}), 404

    try:
        db.session.delete(fee)
        db.session.commit()
        return jsonify({"message": "Fee deleted successfully", "student_id": student_id, "fee_id": fee.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500