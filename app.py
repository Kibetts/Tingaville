from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import *
import bcrypt

session = Session()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

CORS(app)

# Home
class Home(Resource):
    def get(self):
        return 'Welcome to Tinga Springs Schools'

# User Register
class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        role = 'student'  # Default role is 'student'

        if not email or not username or not password:
            return {'error': 'Email, username, and password are required'}, 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Check if the user is a teacher
        if Teacher.query.filter_by(email=email).first():
            role = 'teacher'  # Assign the role of "teacher" to the user
        else:
            return {'error': 'Only teachers can be registered'}, 400

        user = User(email=email, username=username, password=hashed_password.decode('utf-8'), role=role)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created'}, 201
    
    # User Login
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not (email or username):
            return {'error': 'Either email or username is required for login'}, 400

        user = find_user(email, username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
            return {'access_token': access_token}

        return {'error': 'Invalid credentials'}, 401
    
# Class Resource
class ClassResource(Resource):
    @jwt_required()
    def get(self):
        classes = Class.query.all()
        return [c.to_dict() for c in classes]

    @role_required(['admin', 'teacher'])
    def post(self):
        data = request.get_json()
        new_class = Class(**data)
        db.session.add(new_class)
        db.session.commit()
        return new_class.to_dict(), 201

    @role_required(['admin', 'teacher'])
    def patch(self, class_id):
        data = request.get_json()
        class_obj = Class.query.get(class_id)
        if class_obj:
            for key, value in data.items():
                setattr(class_obj, key, value)
            db.session.commit()
            return class_obj.to_dict(), 200
        return {'error': 'Class not found'}, 404

    @role_required(['admin'])
    def delete(self, class_id):
        class_obj = Class.query.get(class_id)
        if class_obj:
            db.session.delete(class_obj)
            db.session.commit()
            return {'message': 'Class deleted'}, 200
        return {'error': 'Class not found'}, 404
    
# Subject Resource
class SubjectResource(Resource):
    @jwt_required()
    def get(self):
        subjects = Subject.query.all()
        return [subject.to_dict() for subject in subjects]

    @role_required(['admin'])
    def post(self):
        data = request.get_json()
        new_subject = Subject(**data)
        db.session.add(new_subject)
        db.session.commit()
        return new_subject.to_dict(), 201

    @role_required(['admin'])
    def patch(self, subject_id):
        data = request.get_json()
        subject_obj = Subject.query.get(subject_id)
        if subject_obj:
            for key, value in data.items():
                setattr(subject_obj, key, value)
            db.session.commit()
            return subject_obj.to_dict(), 200
        return {'error': 'Subject not found'}, 404

    @role_required(['admin'])
    def delete(self, subject_id):
        subject_obj = Subject.query.get(subject_id)
        if subject_obj:
            db.session.delete(subject_obj)
            db.session.commit()
            return {'message': 'Subject deleted'}, 200
        return {'error': 'Subject not found'}, 404

