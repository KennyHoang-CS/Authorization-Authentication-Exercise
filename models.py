from flask_sqlalchemy import SQLAlchemy  
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Users. """

    __tablename__ = 'users'

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register a user w/ hashed password and return user. """
        hashed = bcrypt.generate_password_hash(password)

        # Turn byte string into normal (unicode utf8) string.
        hashed_utf8 = hashed.decode('utf8')

        # return instance of user w/ username and hashed password. 
        return cls(username=username, 
            password=hashed_utf8, 
            email=email, 
            first_name=first_name, 
            last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """ Validate that the user exists and password is correct.
        
        Return user if valid; else return False. 
        """
        u = User.query.filter_by(username=username).first()

        #if u and bcrypt.check_password_hash(u.password, password):
        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

    user_feedbacks = db.relationship('Feedback', backref='users', cascade="all, delete-orphan")

    username = db.Column(
        db.String(20),
        primary_key=True,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    
    last_name = db.Column(
        db.String(30),
        nullable=False
    )

class Feedback(db.Model):
    """ Feedbacks. """

    __tablename__ = 'feedbacks'

    db.relationship('User', backref='feedbacks')

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username')
    )
    