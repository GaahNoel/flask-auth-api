import bcrypt
from flask import Blueprint, jsonify, render_template, abort, request
from flask_login import login_required, login_user, logout_user
from jinja2 import TemplateNotFound
from services.login_manager import login_manager

from models.user import User

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@auth.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password: 
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)): 
        login_user(user)
        return jsonify({"message": "Authenticated"})

  return jsonify({"message": "Invalid credentials"})

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout successfully executed"})