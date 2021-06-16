from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

# from wtforms import StringField
from wtforms.validators import EqualTo, InputRequired, Length, Email

# import email_validator


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
            EqualTo("password_confirm", message="Password must be identical in both inputs"),
        ],
    )
    password_confirm = PasswordField("Confirm Password")
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[InputRequired(), Length(min=5, max=25, message=None), Email(message="That is not an email address :("), ]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )
    remember = BooleanField("Remember Me")
    login = SubmitField("Login")
