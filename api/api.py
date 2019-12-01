"""
api.py
- provides the API endpoints for consuming and producing 
  REST requests and responses
"""

from flask import Blueprint, jsonify, request, current_app
import datetime
from .models import db, Story, User
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity)

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify("welcome to frontend class"), 200
@api.route('/register', methods=('POST',))
def register():
    data = request.get_json()

    existing_user = User.query.filter_by(username= data["username"]).first()
    if(existing_user):
        return jsonify({"error": "username alreay in use"}), 406
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    expires = datetime.timedelta(days=7)
    token = access_token = create_access_token(identity=user.id, expires_delta=expires)
    return jsonify({ 'token': token })

@api.route('/users', methods=('GET',))
@jwt_required
def fetch_users():
    users = User.query.all()
    return jsonify([i.to_dict() for i in users])

@api.route('/stories', methods=('POST',))
@jwt_required
def create_story():
    data = request.get_json()
    print(data)
    story = Story(body=data['body'], title=data['title'])
    if 'users' in data:
        for user_id in data['users']:
            user = User.query.get(int(user_id))
            story.users.append(user)
            db.session.commit()

    story.creator = User.query.get(get_jwt_identity())
    db.session.add(story)
    db.session.commit()
    return jsonify(story.to_dict()), 201


@api.route('/stories', methods=('GET',))
@jwt_required
def fetch_stories():
    stories = Story.query.filter_by(creator_id=get_jwt_identity())
    user = User.query.get(get_jwt_identity())
    shared_stories = user.stories
    result = {"storeis": [i.to_dict() for i in stories], "shared_stories": [s.to_dict() for s in shared_stories] }
    return jsonify(result)


@api.route('/stories/<int:id>', methods=('GET', 'PUT'))
@jwt_required
def story(id):
    if request.method == 'GET':
        story = Story.query.get(id)
        return jsonify(story.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        db.session.commit()
        story = Story.query.get(data['id'])
        return jsonify(story.to_dict()), 201
