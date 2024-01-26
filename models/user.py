from database import db
from uuid import uuid4
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id = db.Column(db.String(40), primary_key=True, default=str(uuid4()))
  username = db.Column(db.String(40), unique=True, nullable=False)
  password = db.Column(db.String(40), nullable=False)

  def __repr__(self):
    return '<User %r>' % self.username
  
  def to_dictionary(self):
    return {
      'id': self.id,
      'username': self.username
    }