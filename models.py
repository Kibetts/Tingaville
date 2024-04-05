from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import validates
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref
from flask_migrate import Migrate
db = SQLAlchemy()