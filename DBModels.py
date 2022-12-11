# Imports the tools required from flask for DB User model.
from flask_login import UserMixin, AnonymousUserMixin

# Imports the SQLAlchemy module for the DB model.
from flask_sqlalchemy import SQLAlchemy

# Initializes an instance of SQLAlchemy.
database = SQLAlchemy()

# Creates the 'User' model for the Login Manager.
class User(UserMixin):
    # Defines the username.
    username = database.Column(database.String(45), primary_key=True)

    # Defines the user ID.
    user_id = database.Column(database.Integer, unique=True)

    # Defines the first name.
    f_name = database.Column(database.String(45))

    # Defines the last name.
    l_name = database.Column(database.String(45))

    # Defines the email.
    email = database.Column(database.String(45), unique=True)

    # Defines the role.
    role = database.Column(database.String(5))

    # Defines the password.
    # password = database.Column(database.String(255))

    # Defines the phone number.
    phone = database.Column(database.String(12))

    # Defines the address foreign key.
    addressFK = database.Column(database.Integer)

    # Defines the bank account foreign key.
    bankAccountFK = database.Column(database.Integer)

    # Defines the authentication status.
    authenticated = database.Column(database.Boolean, default=False)

    # Defines the get_id() function.
    def get_id(self):
        return self.username

    # Defines the is_active() function.
    def is_active(self):
        return True

    # Defines the is_authenticated() function.
    def is_authenticated(self):
        return True

    # Defines the is_anonymous() function.
    def is_anonymous(self):
        return False

# Creates the 'Anonymous' model for the Login Manager.
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        pass