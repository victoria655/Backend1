from .database import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    middlename = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    admission_number = db.Column(db.String(50), unique=True, nullable=False)
    grade = db.Column(db.String(50), nullable=False)

    fees = db.relationship('Fee', back_populates='student', cascade='all, delete-orphan')
    activities = db.relationship('StudentActivity', back_populates='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.firstname} {self.lastname}, {self.admission_number}>'

    @property
    def total_fee_paid(self):
        return sum(fee.amount for fee in self.fees)
    
    @property
    def fee_required(self):
        return 10000
    
    @property
    def fee_deficit(self):
        return max(self.fee_required - self.total_fee_paid, 0)
    
    @property
    def overpayment(self):
        return max(self.total_fee_paid - self.fee_required, 0)
    
    @property
    def activity_payments(self):
        activity_data = []
        for link in self.activities:
            fee_required = link.activity.fee
            amount_paid = link.amount_paid
            amount_pending = max(fee_required - amount_paid, 0)
            overpayment = max(amount_paid - fee_required, 0)
            activity_data.append({
                "activity_name": link.activity.name,
                "fee": fee_required,
                "amount_paid": amount_paid,
                "amount_pending": amount_pending,
                "overpayment": overpayment,
            })
        return activity_data