import bcrypt
from flask import Flask, jsonify, request
from models.user import User
from repositories.connection import db
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from routes.user import user
from routes.auth import auth
from services.login_manager import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# SQLite connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

# MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost:3306/flask-auth-crud'

login_manager.init_app(app)
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(user)

login_manager.login_view = 'login'

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
  return jsonify({"message": "Working correctly"})

if __name__ == '__main__':
  app.run(debug=True)