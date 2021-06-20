import secrets
import os

from flask import render_template, url_for, flash, redirect, request, abort
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user

# from sqlalchemy.orm.query import Query

from app.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from app import app, db
from app.models import User, Post


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    posts = Post.query.all()
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
            next_page = request.args.get("next")
            flash(f"You have been logged in as {user.username}!", "success")
            return redirect(next_page) if next_page else redirect(url_for("account"))

        else:
            flash(
                "Login failed, please check if your password matches with your email!",
                "danger",
            )
            return render_template(
                "login.html", title="Login", form=form, is_login_failed=True
            )

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bye!!! You have been successfully logged out!", "success")
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/pics", picture_filename)
    form_picture.save(picture_path)
    return picture_filename


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    image = url_for("static", filename=f"pics/{current_user.image_file}")

    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(
            "Your account has been updated!",
            "info",
        )
        return redirect(url_for("account"))
    return render_template(
        "account.html", title=f"{current_user.username}", profile_img=image, form=form
    )


@app.route("/posts/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.content.data
        new_post = Post(
            title=post_title,
            content=post_content,
            user_id=current_user.id,
            password="1",
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))

    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/posts/<int:post_id>")
def new_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        flash("Your post has been updated!", "success")

        db.session.commit()
        return redirect(url_for("new_post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/posts/<int:post_id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    message = "Page does not exist"
    return render_template("error.html", title="No such thing", message=message), 404


@app.errorhandler(403)
def access_denied(error):
    message = "You do not have access to this page"
    return render_template("error.html", title="access denied", message=message), 403
