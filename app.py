from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

import os


_SECRET_KEY = os.urandom(16).hex()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = _SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

posts = [
    {
        "author": "R. van Beveren",
        "title": "Blog post 1 Title",
        "content": "First post content",
        "date_posted": "April 20 2010",
    },
    {
        "author": "S. ome Onelse",
        "title": "Blog post 2 Title",
        "content": "Second post content",
        "date_posted": "April 20 2020",
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!!!!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data and form.password.data == "1234":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash(
                "Login failed, please check if your password matches with your email!",
                "danger",
            )

    return render_template("login.html", title="Login", form=form)
