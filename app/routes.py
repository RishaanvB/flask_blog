from flask import render_template, url_for, flash, redirect
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user

from app.forms import RegistrationForm, LoginForm
from app import app, db
from app.models import User


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
        password = form.password.data
        hashed_pw = generate_password_hash(password)
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!!!!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            flash(f"You have been logged in as {user.username}!", "success")
            return redirect(url_for("home"))

        else:
            flash(
                "Login failed, please check if your password matches with your email!",
                "danger",
            )

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bye!!! You have been successfully logged out!", "success")
    return redirect(url_for("home"))
