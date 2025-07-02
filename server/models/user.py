from .database import db
from sqlalchemy.ext.hybrid import hybrid_property
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    @hybrid_property
    def password(self):
        raise AttributeError("Password is not accessible directly")

    @password.setter
    def password(self, plain_text):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, plain_text):
            raise ValueError(
                "Password must be at least 8 characters long, contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character."
            )
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')

    def check_password(self, plain_text):
        return bcrypt.check_password_hash(self.password_hash, plain_text)

    def __repr__(self):
        return f'<User {self.role}, {self.email}>'