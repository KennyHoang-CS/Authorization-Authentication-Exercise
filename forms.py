from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email

class UserRegisterForm(FlaskForm):
    """ Form for adding users. """

#This form should accept a username, password, email, first_name, and last_name.

    username = StringField(
        "Username", 
        validators=[InputRequired(), 
            Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)]
    )

class UserLoginForm(FlaskForm):
    """ Form handling user logins. """

    username = StringField(
        "Username", 
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

class EditFeedbackForm(FlaskForm):
    """ Form to edit feedbacks. """ 
    title = StringField(
        "Title"
    )

    content = TextAreaField(
        "Edit Content"
    )

class AddFeedbackForm(FlaskForm):
    """ Form to add feedbacks. """
    title = StringField(
        "Title"
    )

    content = TextAreaField(
        "Content"
    )