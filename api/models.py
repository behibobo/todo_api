"""
models.py
- Data classes for the surveyapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

shared_stories = db.Table('shared_stories',
    db.Column('story_id', db.Integer, db.ForeignKey('stories.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120),  nullable=False)
    last_name = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(255), nullable=False)
    items = db.relationship('Story', backref="creator", lazy=False)

    def __init__(self, username, first_name, last_name, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password, method='sha256')

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        
        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, full_name=self.full_name())



class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    users = db.relationship('User', secondary=shared_stories, lazy='subquery',
        backref=db.backref('stories', lazy=True))

    def to_dict(self):
      return dict(id=self.id,
                  title=self.title,
                  body=self.body,
                  by=self.creator.full_name(),
                  created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                  users=[user.full_name() for user in self.users])

