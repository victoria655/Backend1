from flask import Blueprint, jsonify, request
from server.models.student import Student
from server.models.database import db
from server.models.activity import Activity
from server.models.studentactivity import StudentActivity
import os
import sys

# Add server directory to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

students_activities_bp = Blueprint('students_activities', __name__, url_prefix='/students/activities')

@students_activities_bp.route('/', methods=['GET'])
def list_students_with_activities():
    students = Student.query.all()
    data = []
    for student in students:
        for sa in student.activities:
            activity_fee = sa.activity.fee
            amount_paid = sa.amount_paid
            amount_pending = max(activity_fee - amount_paid, 0)

            data.append({
                "id": student.id,
                "firstname": student.firstname,
                "middlename": student.middlename,
                "lastname": student.lastname,
                "admission_number": student.admission_number,
                "grade": student.grade,
                "activity_name": sa.activity.name,
                "activity_fee": activity_fee,
                "amount_paid": amount_paid,
                "amount_pending": amount_pending,
            })
    return jsonify(data)

@students_activities_bp.route('/student/<string:admission_number>', methods=['GET'])
def get_student_activities(admission_number):
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    data = []
    for sa in student.activities:
        activity_fee = sa.activity.fee
        amount_paid = sa.amount_paid
        amount_pending = max(activity_fee - amount_paid, 0)

        data.append({
            "activity_name": sa.activity.name,
            "activity_fee": activity_fee,
            "amount_paid": amount_paid,
            "amount_pending": amount_pending,
        })

    return jsonify({
        "firstname": student.firstname,
        "middlename": student.middlename,
        "lastname": student.lastname,
        "admission_number": student.admission_number,
        "grade": student.grade,
        "activities": data
    })

@students_activities_bp.route('/student/<string:admission_number>/update_payment', methods=['PATCH'])
def update_payment_status(admission_number):
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    data = request.get_json()
    activity_name = data.get('activity_name')
    amount_paid = data.get('amount_paid')

    if not activity_name or amount_paid is None:
        return jsonify({"error": "Activity name and amount_paid are required"}), 400

    student_activity = next(
        (sa for sa in student.activities if sa.activity.name == activity_name),
        None
    )

    if not student_activity:
        return jsonify({"error": "Activity not found for this student"}), 404

    try:
        student_activity.amount_paid = amount_paid
        student_activity.payment_status = 'paid' if amount_paid >= student_activity.activity.fee else 'partial'
        db.session.commit()
        return jsonify({
            "message": "Payment status updated successfully",
            "activity_name": student_activity.activity.name,
            "amount_paid": student_activity.amount_paid,
            "payment_status": student_activity.payment_status
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@students_activities_bp.route('/student/<string:admission_number>/activities', methods=['POST'])
def add_student_activity(admission_number):
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    data = request.get_json()
    activity_id = data.get('activity_id')
    amount_paid = data.get('amount_paid', 0)

    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    try:
        student_activity = StudentActivity(
            student_id=student.id,
            activity_id=activity_id,
            amount_paid=amount_paid,
            payment_status='paid' if amount_paid >= activity.fee else 'partial'
        )
        db.session.add(student_activity)
        db.session.commit()
        return jsonify({
            "message": "Student activity added successfully",
            "activity_name": activity.name,
            "amount_paid": student_activity.amount_paid,
            "payment_status": student_activity.payment_status
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@students_activities_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_all_student_activities(student_id):
    activities = StudentActivity.query.filter_by(student_id=student_id).all()
    if not activities:
        return jsonify({"error": "No activities found for this student"}), 404

    try:
        for activity in activities:
            db.session.delete(activity)
        db.session.commit()
        return jsonify({"message": f"All activities for student {student_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500