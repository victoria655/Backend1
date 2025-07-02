from .database import db

class StudentActivity(db.Model):
    __tablename__ = 'student_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False, default=0.0)
    payment_status = db.Column(db.String(50), nullable=False, default='pending')
    
    student = db.relationship('Student', back_populates='activities')
    activity = db.relationship('Activity', back_populates='student_link')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'activity_id', name='unique_student_activity'),
    )
    
    def __repr__(self):
        return f'<StudentActivity {self.student_id} - {self.activity_id}>'