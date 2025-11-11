# db.py
from flask_sqlalchemy import SQLAlchemy
from utility import this_time

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=this_time(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
