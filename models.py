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

    clubs = db.relationship('Club', secondary='club_member', backref=db.backref('members', lazy='dynamic'),
                            primaryjoin="User.id == club_member.c.user_id")

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

    classes = db.relationship('Class', secondary='student_class', back_populates='students')

student_class = db.Table('student_class',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
) 

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    role = db.Column(db.String, default='teacher')
    subjects = db.relationship('Subject', secondary='teacher_subject', back_populates='teachers')

teacher_subject = db.Table(
    'teacher_subject',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    grade_level = db.Column(db.Integer)
    students = db.relationship('Student', secondary='student_class', back_populates='classes')
    schedule = db.relationship('Schedule', backref='class')

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    teachers = db.relationship('Teacher', secondary='teacher_subject', back_populates='subjects')

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    class_time = db.Column(db.DateTime)
    location = db.Column(db.String)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', backref=backref('schedules', lazy='dynamic'))

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    grade = db.Column(db.Float)

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location = db.Column(db.String)
    description = db.Column(db.Text)

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    file_path = db.Column(db.String)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject', backref=backref('files', lazy='dynamic'))

class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject', backref=backref('links', lazy='dynamic'))

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    sender = db.relationship('User', foreign_keys=[sender_id], primaryjoin='Message.sender_id == User.id', backref=backref('sent_messages', lazy='dynamic'))

class Forum(db.Model):
    __tablename__ = 'forums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject', backref=backref('forums', lazy='dynamic'))

club_member = db.Table(
    'club_member',
    db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),  
    db.ForeignKeyConstraint(['club_id'], ['clubs.id']),
    db.ForeignKeyConstraint(['user_id'], ['users.id']),  
    info={'extend_existing': True}
)

class Club(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)


class Sports(db.Model):
    __tablename__ = 'sports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)

class SportsEvent(db.Model):
    __tablename__ = 'sports_events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location = db.Column(db.String)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'))

class Library(db.Model):
    __tablename__ = 'libraries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'))
    checkout_records = db.relationship('CheckoutRecord', backref='book')

class CheckoutRecord(db.Model):
    __tablename__ = 'checkout_records'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    checkout_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
