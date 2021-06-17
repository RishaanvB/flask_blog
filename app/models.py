from app import db, login_manager
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default="default.jpg")
    password = Column(String(60), nullable=False)
    posts = relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User: {self.username}, {self.email}, {self.image_file}"


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date_posted = Column(DateTime(120), default=datetime.utcnow, nullable=False)
    content = Column(
        Text(20),
        nullable=False,
    )
    password = Column(String(60), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post: {self.title}, {self.date_posted}"
