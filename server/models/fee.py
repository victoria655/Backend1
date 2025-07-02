from .database import db
from datetime import datetime

class Fee(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    student = db.relationship('Student', back_populates='fees')
    
    def __repr__(self):
        return f'<Payment {self.id} for Student {self.student_id}>'