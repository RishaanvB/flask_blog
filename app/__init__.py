from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


_SECRET_KEY = os.urandom(16).hex()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = _SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You need to be logged in to view this page."
login_manager.login_message_category = "info"
db = SQLAlchemy(app)

from app import routes


# user = User(username="John", email="John@demo.com", password="1234")