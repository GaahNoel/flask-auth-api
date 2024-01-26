from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password: 
    user = User.query.filter_by(username=username).first()

    if user and user.password == password: 
        login_user(user)
        print(current_user.is_authenticated)
        return jsonify({"message": "Authenticated"})

  return jsonify({"message": "Invalid credentials"})

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout successfully executed"})

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password: 
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"})

  return jsonify({"message": "Invalid credentials"})

@app.route('/user/<string:id>', methods=['GET'])
def read_user(id):
  user = User.query.get(id)
  if user: 
    return jsonify(user.to_dictionary())

  return jsonify({"message": "Invalid credentials"}) 

@app.route('/user/<string:id>', methods=['PATCH'])
@login_required
def update_user(id):
  data = request.json
  password = data.get('password')
  user = User.query.get(id)

  if user and password:
     user.password = password
     db.session.commit()
     return jsonify({"message": "User updated successfully"})
  
  return jsonify({"message": "Invalid credentials"})

@app.route('/user/<string:id>', methods=['DELETE'])
@login_required
def delete_user(id):
  user = User.query.get(id)
  
  if user:
     db.session.delete(user)
     db.session.commit()
     return jsonify({"message": "User deleted successfully"})
  
  return jsonify({"message": "Invalid credentials"})
    

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
  return jsonify({"message": "Working correctly"})


if __name__ == '__main__':
  app.run(debug=True)