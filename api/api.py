"""
api.py
- provides the API endpoints for consuming and producing 
  REST requests and responses
"""

from flask import Blueprint, jsonify, request, current_app

from .models import db, Item, User
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

    token = access_token = create_access_token(identity=user.id)
    return jsonify({ 'token': token })


@api.route('/items', methods=('POST',))
@jwt_required
def create_item():
    data = request.get_json()
    item = Item(name=data['name'], details=data['details'])
    item.creator = User.query.get(get_jwt_identity())
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@api.route('/items', methods=('GET',))
@jwt_required
def fetch_items():
    items = Item.query.filter_by(creator_id=get_jwt_identity())
    return jsonify([i.to_dict() for i in items])


@api.route('/items/<int:id>', methods=('GET', 'PUT'))
@jwt_required
def item(id):
    if request.method == 'GET':
        item = Item.query.get(id)
        return jsonify(item.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        db.session.commit()
        item = Item.query.get(data['id'])
        return jsonify(item.to_dict()), 201
