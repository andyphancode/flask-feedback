from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    """Form for adding a user"""


    username = StringField("Username",
                           validators=[InputRequired(),Length(min=5,max=20)])
    password = PasswordField("Password",
                             validators=[InputRequired(),Length(min=5,max=50)])
    email = StringField("Email",
                        validators=[InputRequired(),Email(),Length(max=50)])
    first_name = StringField("First Name",
                             validators=[InputRequired(),Length(max=30)])
    last_name = StringField("Last Name",
                            validators=[InputRequired(),Length(max=30)])

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username",
                           validators=[InputRequired(),Length(min=5,max=20)])
    password = PasswordField("Password",
                             validators=[InputRequired(),Length(min=5,max=50)])
    
class FeedbackForm(FlaskForm):
    """Form for giving feedback"""

    title = StringField("Title",
                           validators=[InputRequired(), Length(max=100)])
    content = StringField("Feedback",
                           validators=[InputRequired(), Length(max=500)])
