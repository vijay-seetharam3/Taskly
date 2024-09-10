from . import db
from datetime import datetime
from flask_login import UserMixin

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f'<Todo {self.content}>'

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    bio = db.Column(db.String(150))
    birthday = db.Column(db.String(150))
    phone_no = db.Column(db.String(150))
    profile_image = db.Column(db.LargeBinary)
    Todos = db.relationship('Todo')
