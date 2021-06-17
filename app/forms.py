from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import EqualTo, InputRequired, Length, Email, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=25)],
    )

    email = StringField(
        "Email", validators=[InputRequired(), Length(min=5, max=25), Email()]
    )
    password = PasswordField(
        "Set Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password_confirm", message="Password must be identical in both inputs"
            ),
        ],
    )
    password_confirm = PasswordField("Confirm Password")
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken. Please choose another username")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("A user with this email already exists.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Length(min=5, max=25, message=None),
            Email(message="That is not an email address :("),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )
    remember = BooleanField("Remember Me")
    login = SubmitField("Login")
