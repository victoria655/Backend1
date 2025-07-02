import os
import sys
from datetime import datetime

# Add project_root to Python path (parent of server/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import create_app
from server.models.database import db
from server.models.student import Student
from server.models.fee import Fee
from server.models.activity import Activity
from server.models.studentactivity import StudentActivity

app = create_app()

with app.app_context():
    # Step 1: Clear existing data
    StudentActivity.query.delete()
    Fee.query.delete()
    Student.query.delete()
    Activity.query.delete()
    db.session.commit()

    # Step 2: Create Activities (IDs 4–10)
    activity_data = [
        (4, "Drama Club", 1000),
        (5, "Music Club", 1200),
        (6, "Football Club", 800),
        (7, "Chess Club", 600),
        (8, "Debate Club", 700),
        (9, "Badminton", 900),
        (10, "Swimming", 1500),
    ]
    activities = [Activity(id=aid, name=name, fee=fee) for aid, name, fee in activity_data]
    db.session.add_all(activities)
    db.session.commit()

    # Step 3: Create Students
    student_records = [
        {
            "firstname": "Alice",
            "middlename": "Wangui",
            "lastname": "Njeri",
            "admission_number": "ADM001",
            "grade": "Grade 1",
            "activities": [4, 5],
        },
        {
            "firstname": "Brian",
            "middlename": "Mothokoi",
            "lastname": "Otieno",
            "admission_number": "ADM002",
            "grade": "Grade 2",
            "activities": [6, 7],
        },
        {
            "firstname": "Carol",
            "middlename": "Kipchirchir",
            "lastname": "Mutiso",
            "admission_number": "ADM003",
            "grade": "Grade 3",
            "activities": [8, 9],
        },
    ]

    for record in student_records:
        student = Student(
            firstname=record["firstname"],
            middlename=record["middlename"],
            lastname=record["lastname"],
            admission_number=record["admission_number"],
            grade=record["grade"],
        )
        db.session.add(student)
        db.session.flush()

        # Add fees
        db.session.add(Fee(student_id=student.id, amount=4000, date=datetime.utcnow()))
        db.session.add(Fee(student_id=student.id, amount=2000, date=datetime.utcnow()))

        # Add activities
        for activity_id in record["activities"]:
            activity = Activity.query.get(activity_id)
            db.session.add(StudentActivity(
                student_id=student.id,
                activity_id=activity_id,
                amount_paid=activity.fee // 2,
                payment_status="partial"
            ))

    db.session.commit()
    print("✅ Students, fees, and activities successfully seeded.")