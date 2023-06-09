from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.String(20),nullable=False,unique=True,primary_key=True)
    password = db.Column(db.String,nullable=False)
    email= db.Column(db.String(50),nullable=False)
    first_name= db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/ hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name,last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user."""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False
        
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

class Feedback(db.Model):
    """Feedback"""
    
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )