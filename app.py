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

# News Resource
class NewsResource(Resource):
    @jwt_required()
    def get(self):
        news_items = News.query.all()
        return [news.to_dict() for news in news_items]

    @role_required(['admin', 'teacher'])
    def post(self):
        data = request.get_json()
        new_news = News(**data)
        db.session.add(new_news)
        db.session.commit()
        return new_news.to_dict(), 201

    @role_required(['admin', 'teacher'])
    def patch(self, news_id):
        data = request.get_json()
        news_obj = News.query.get(news_id)
        if news_obj:
            for key, value in data.items():
                setattr(news_obj, key, value)
            db.session.commit()
            return news_obj.to_dict(), 200
        return {'error': 'News not found'}, 404

    @role_required(['admin'])
    def delete(self, news_id):
        news_obj = News.query.get(news_id)
        if news_obj:
            db.session.delete(news_obj)
            db.session.commit()
            return {'message': 'News deleted'}, 200
        return {'error': 'News not found'}, 404

# Event Resource
class EventResource(Resource):
    @jwt_required()
    def get(self):
        events = Event.query.all()
        return [event.to_dict() for event in events]

    @role_required(['admin', 'teacher'])
    def post(self):
        data = request.get_json()
        new_event = Event(**data)
        db.session.add(new_event)
        db.session.commit()
        return new_event.to_dict(), 201

    @role_required(['admin', 'teacher'])
    def patch(self, event_id):
        data = request.get_json()
        event_obj = Event.query.get(event_id)
        if event_obj:
            for key, value in data.items():
                setattr(event_obj, key, value)
            db.session.commit()
            return event_obj.to_dict(), 200
        return {'error': 'Event not found'}, 404

    @role_required(['admin'])
    def delete(self, event_id):
        event_obj = Event.query.get(event_id)
        if event_obj:
            db.session.delete(event_obj)
            db.session.commit()
            return {'message': 'Event deleted'}, 200
        return {'error': 'Event not found'}, 404

# File Resource
class FileResource(Resource):
    @jwt_required()
    def get(self):
        files = File.query.all()
        return [file.to_dict() for file in files]

    @role_required(['admin', 'teacher'])
    def post(self):
        data = request.get_json()
        new_file = File(**data)
        db.session.add(new_file)
        db.session.commit()
        return new_file.to_dict(), 201

    @role_required(['admin', 'teacher'])
    def patch(self, file_id):
        data = request.get_json()
        file_obj = File.query.get(file_id)
        if file_obj:
            for key, value in data.items():
                setattr(file_obj, key, value)
            db.session.commit()
            return file_obj.to_dict(), 200
        return {'error': 'File not found'}, 404

    @role_required(['admin'])
    def delete(self, file_id):
        file_obj = File.query.get(file_id)
        if file_obj:
            db.session.delete(file_obj)
            db.session.commit()
            return {'message': 'File deleted'}, 200
        return {'error': 'File not found'}, 404
    
# Link Resource
class LinkResource(Resource):
    @jwt_required()
    def get(self):
        links = Link.query.all()
        return [link.to_dict() for link in links]

    @role_required(['admin', 'teacher'])
    def post(self):
        data = request.get_json()
        new_link = Link(**data)
        db.session.add(new_link)
        db.session.commit()
        return new_link.to_dict(), 201

    @role_required(['admin', 'teacher'])
    def patch(self, link_id):
        data = request.get_json()
        link_obj = Link.query.get(link_id)
        if link_obj:
            for key, value in data.items():
                setattr(link_obj, key, value)
            db.session.commit()
            return link_obj.to_dict(), 200
        return {'error': 'Link not found'}, 404

    @role_required(['admin'])
    def delete(self, link_id):
        link_obj = Link.query.get(link_id)
        if link_obj:
            db.session.delete(link_obj)
            db.session.commit()
            return {'message': 'Link deleted'}, 200
        return {'error': 'Link not found'}, 404
    
# MessageResource
class MessageResource(Resource):
    @jwt_required()
    def get(self):
        messages = Message.query.all()
        return [message.to_dict() for message in messages]

    @role_required(['admin', 'teacher', 'student'])
    def post(self):
        data = request.get_json()
        new_message = Message(**data)
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

    @role_required(['admin'])
    def delete(self, message_id):
        message_obj = Message.query.get(message_id)
        if message_obj:
            db.session.delete(message_obj)
            db.session.commit()
            return {'message': 'Message deleted'}, 200
        return {'error': 'Message not found'}, 404

# ForumResource 
class ForumResource(Resource):
    @jwt_required()
    def get(self):
        forums = Forum.query.all()
        return [forum.to_dict() for forum in forums]

    @role_required(['admin', 'teacher', 'student'])
    def post(self):
        data = request.get_json()
        new_forum = Forum(**data)
        db.session.add(new_forum)
        db.session.commit()
        return new_forum.to_dict(), 201

    @role_required(['admin'])
    def delete(self, forum_id):
        forum_obj = Forum.query.get(forum_id)
        if forum_obj:
            db.session.delete(forum_obj)
            db.session.commit()
            return {'message': 'Forum deleted'}, 200
        return {'error': 'Forum not found'}, 404
    
# ClubResource 
class ClubResource(Resource):
    @jwt_required()
    def get(self):
        clubs = Club.query.all()
        return [club.to_dict() for club in clubs]

    @role_required(['admin', 'teacher', 'student'])
    def post(self):
        data = request.get_json()
        new_club = Club(**data)
        db.session.add(new_club)
        db.session.commit()
        return new_club.to_dict(), 201

    @role_required(['admin'])
    def delete(self, club_id):
        club_obj = Club.query.get(club_id)
        if club_obj:
            db.session.delete(club_obj)
            db.session.commit()
            return {'message': 'Club deleted'}, 200
        return {'error': 'Club not found'}, 404
    
# Sports Resource
class SportsResource(Resource):
    @jwt_required()
    def get(self):
        sports = Sports.query.all()
        return [s.to_dict() for s in sports]

    @role_required(['admin'])
    def post(self):
        data = request.get_json()
        new_sport = Sports(**data)
        db.session.add(new_sport)
        db.session.commit()
        return new_sport.to_dict(), 201

    @role_required(['admin'])
    def patch(self, sport_id):
        data = request.get_json()
        sport_obj = Sports.query.get(sport_id)
        if sport_obj:
            for key, value in data.items():
                setattr(sport_obj, key, value)
            db.session.commit()
            return sport_obj.to_dict(), 200
        return {'error': 'Sport not found'}, 404

    @role_required(['admin'])
    def delete(self, sport_id):
        sport_obj = Sports.query.get(sport_id)
        if sport_obj:
            db.session.delete(sport_obj)
            db.session.commit()
            return {'message': 'Sport deleted'}, 200
        return {'error': 'Sport not found'}, 404
    
# Library Resource
class LibraryResource(Resource):
    @jwt_required()
    def get(self):
        libraries = Library.query.all()
        return [l.to_dict() for l in libraries]

    @role_required(['admin'])
    def post(self):
        data = request.get_json()
        new_library = Library(**data)
        db.session.add(new_library)
        db.session.commit()
        return new_library.to_dict(), 201

    @role_required(['admin'])
    def patch(self, library_id):
        data = request.get_json()
        library_obj = Library.query.get(library_id)
        if library_obj:
            for key, value in data.items():
                setattr(library_obj, key, value)
            db.session.commit()
            return library_obj.to_dict(), 200
        return {'error': 'Library not found'}, 404

    @role_required(['admin'])
    def delete(self, library_id):
        library_obj = Library.query.get(library_id)
        if library_obj:
            db.session.delete(library_obj)
            db.session.commit()
            return {'message': 'Library deleted'}, 200
        return {'error': 'Library not found'}, 404
    
# Book Resource
class BookResource(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.all()
        return [b.to_dict() for b in books]

    @role_required(['admin'])
    def post(self):
        data = request.get_json()
        new_book = Book(**data)
        db.session.add(new_book)
        db.session.commit()
        return new_book.to_dict(), 201

    @role_required(['admin'])
    def patch(self, book_id):
        data = request.get_json()
        book_obj = Book.query.get(book_id)
        if book_obj:
            for key, value in data.items():
                setattr(book_obj, key, value)
            db.session.commit()
            return book_obj.to_dict(), 200
        return {'error': 'Book not found'}, 404

    @role_required(['admin'])
    def delete(self, book_id):
        book_obj = Book.query.get(book_id)
        if book_obj:
            db.session.delete(book_obj)
            db.session.commit()
            return {'message': 'Book deleted'}, 200
        return {'error': 'Book not found'}, 404
