from .database import db
from sqlalchemy.orm import validates

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Float, nullable=False)

    student_link = db.relationship('StudentActivity', back_populates='activity', cascade='all, delete-orphan')

    ALLOWED_ACTIVITIES = {
        'Drama Club', 'Music Club', 'Football Club', 'Chess Club', 'Debate Club',
        'Badminton', 'Swimming', 'Science Club', 'Math Club', 'Art Club'
    }

    @validates('name')
    def validate_name(self, key, value):
        formatted_value = value.strip().title()
        if formatted_value not in self.ALLOWED_ACTIVITIES:
            raise ValueError(f"'{value}' is not an allowed activity. Choose from: {', '.join(self.ALLOWED_ACTIVITIES)}")
        return formatted_value
    
    def __repr__(self):
        return f'<Activity {self.name}>'