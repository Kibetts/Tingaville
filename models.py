from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import validates
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref
from flask_migrate import Migrate
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='student')  # Default role is 'student'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    role = db.Column(db.String, default='student')
    grade = db.Column(db.Integer)    