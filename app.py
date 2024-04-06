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