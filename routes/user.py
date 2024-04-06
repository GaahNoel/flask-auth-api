import bcrypt
from flask import Blueprint, jsonify, render_template, abort, request
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound
from repositories.connection import db

from models.user import User

user = Blueprint('user', __name__)

@user.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password: 
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    user = User(username=username, password=hashed_password, role='user')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"})

  return jsonify({"message": "Invalid credentials"})

@user.route('/user/<string:id>', methods=['GET'])
def read_user(id):
  user = User.query.get(id)
  if user: 
    return jsonify(user.to_dictionary())

  return jsonify({"message": "Invalid credentials"}) 

@user.route('/user/<string:id>', methods=['PATCH'])
@login_required
def update_user(id):
  data = request.json
  password = data.get('password')
  user = User.query.get(id)

  if id != current_user.id and current_user.role != 'admin':
    return jsonify({"message": "Operation not permitted"}), 403
  
  if user and password:
     user.password = password
     db.session.commit()
     return jsonify({"message": "User updated successfully"})
  
  return jsonify({"message": "Invalid credentials"})

@user.route('/user/<string:id>', methods=['DELETE'])
@login_required
def delete_user(id):
  user = User.query.get(id)
  
  if current_user.role != 'admin':
    return jsonify({"message": "Operation not permitted"}), 403 

  if user:
     db.session.delete(user)
     db.session.commit()
     return jsonify({"message": "User deleted successfully"})
  
  return jsonify({"message": "Invalid credentials"})
    