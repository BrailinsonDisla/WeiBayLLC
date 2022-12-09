# Imports the tools required from flask_login for Permission Management.
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded

# Imports the hashing functionalities from werkzeug.security for authentication.
from werkzeug.security import generate_password_hash, check_password_hash

# Imports the regular expression module (as regEx) for pattern matching.
import re as regEx

# Imports the tools required from flask_login for Login Management.
from flask_login import LoginManager, login_user, current_user

# Imports the flask website application.
from WeiBayLLC import WeiBayLLC_App

# Imports user-defined exceptions.
from UD_Exceptions import *

# Imports required DB model.
from DBModels import User

# Imports the API for MySQL.
from mysql.connector import *

# Defines the admin role.
default_admin_role = 'ADMIN'

# Defines the registered user role.
default_registered_role = 'RUSER'

# Defines the guest user role.
default_gest_role = 'GUEST'

# Defines the default database admin
default_admin = 'db-admin'

# Defines the default host.
default_host = '34.95.20.62'

# Defines the default database.
default_db = 'Test_WeiBayLLC'

# Defines the default password.
default_pswd = 'ABCMT!322'

# Checks if the given email is valid.
def validEmail(email : str):
    # Checks if the given email matches an email's format.
    if regEx.search('^[a-zA-Z]+[a-zA-Z0-9.\-_]*@[a-zA-Z]+(\.[a-zA-Z]{2,3})+$', email):
        return True

    # Returns false if the format does not match.
    return False

# Submits the RU application for approval.
def submitRUApplication(f_name: str, l_name: str, email: str, pswd: str, confirm_pswd, role: str = 'RUSER'):
    # Cleans up the inputs for the first name, last name and email fields.
    f_name = f_name.strip(); l_name = l_name.strip(); email = email.strip().lower()

    # Defines invalid values for application fields.
    invalid_values = [None, '']

    # Checks if the first name is invalid.
    if f_name in invalid_values:
        # Raise an InvalidFirstName exception.
        raise InvalidFirstName

    # Checks if the last name is invalid.
    if l_name in invalid_values:
        # Raise an InvalidLastName exception.
        raise InvalidLastName

    # Checks if the email is invalid.
    if email in invalid_values or not validEmail(email):
        # Raise an InvalidEmail exception.
        raise InvalidEmail

    # Tracks validity of both pswd and confirm_pswd.
    pswd_validity = True

    # Stores the hashed password.
    pswd_hash = ''

    # Checks if the pswd field is invalid.
    if pswd in invalid_values or confirm_pswd in invalid_values:
        # Sets password validity to false.
        pswd_validity = False

        # Raise an InvalidPassword exception.
        raise InvalidPassword

    # Checks if pswd and confirm_pswd match.
    if pswd_validity:
        if pswd != confirm_pswd:
            # Raise an InvalidPassword exception.
            raise PasswordMismatch
        else:
            # Hashes the password using SHA-256.
            pswd_hash = generate_password_hash(pswd, method='sha-256')

    # Extracts the username from the email.
    username = email.split(sep='@')[0]

    # Stores the applicant's information.
    application_data = ''

    try:
        # Connects to the WeiBay LLC database.
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

        # Creates a cursor to execute application submission query.
        cursor = connection.cursor()

        # Checks if the user has a pending application.
        cursor.execute("SELECT Username FROM PendingRUApplications WHERE Username = %s", (username, ))

        # Fetches the first result of the query.
        cursor.fetchone()

        # Checks if the username exists in PendingRUApplications.
        if cursor.rowcount == 1:
            # Raise a PendingApplication exception.
            raise PendingApplicant

        # Checks if the user is already registered.
        cursor.execute("SELECT Username FROM RegisteredUsers WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        cursor.fetchone()

        # Checks if the username exists in RegisteredUsers.
        if cursor.rowcount == 1:
            # Raise AlreadyRegistered exception.
            raise AlreadyRegistered

        # Checks if the user is banned.
        cursor.execute("SELECT Username FROM BannedUsers WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        cursor.fetchone()

        # Checks if the username exists in BannedUsers.
        if cursor.rowcount == 1:
            # Raise BannedApplicant exception.
            raise BannedApplicant

        # Creates a tuple with the values to insert.
        application_data = (f_name, l_name, username, email, pswd_hash, role)

        # Submits the user's application to the pending approval queue.
        cursor.execute( "INSERT INTO PendingRUApplications (First_Name, Last_Name, Username, Email, Password, Role) "
                        "VALUES (%s, %s, %s, %s, %s, %s)", application_data)

        # Commits the changes to the database.
        connection.commit()

        # TODO: Inform the applicant that their application was submitted.

    # Re-throw exception for system-specific exceptions.
    except PendingApplicant:
        raise PendingApplicant
    except AlreadyRegistered:
        raise AlreadyRegistered
    except BannedApplicant:
        raise BannedApplicant

    # Catches other, system unrelated, exception.
    except Exception as e:
        # TODO: Inform the applicant that their application was not submitted.
        print('FAILED TO SUBMIT APPLICATION FOR:', application_data, flush=True)

# Approves RU application from 'PendingRUApplications'.
def approveRUApplication(username : str):
    # Cleans up the input for username.
    username = username.lower()

    # Stores pending application information.
    pending_application_data = ''

    try:
        # Connects to the WeiBay LLC database.
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

        # Creates a cursor to execute application approval query.
        cursor = connection.cursor()

        # Gets the information for the user from the 'PendingRUApplications' table.
        cursor.execute("SELECT * FROM PendingRUApplications WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        pending_application_data = cursor.fetchone()

        # Checks if the username exists in PendingRUApplications.
        if cursor.rowcount == 1:
            # Approves the user's application -- add to the RegisteredUsers table.
            cursor.execute("INSERT INTO RegisteredUsers VALUES (%s, %s, %s, %s, %s, %s, %s)", pending_application_data)

            # Approves the user's application -- delete from the PendingRUApplications table.
            cursor.execute("DELETE FROM PendingRUApplications WHERE Username = %s", (username, ))

            # Commits the changes to the database.
            connection.commit()

            # TODO: Inform the applicant that their application has been approved.
    except Exception as e:
        # TODO: Inform the database admin that application was not approved.
        print('FAILED TO APPROVE APPLICATION FOR:', pending_application_data, flush=True)

# Denies RU application from 'PendingRUApplications'.
def denyRUApplication(username : str):
    # Cleans up the input for username.
    username = username.lower()

    # Stores pending application information.
    pending_application_data = ''

    try:
        # Connects to the WeiBay LLC database.
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

        # Creates a cursor to execute application denial query.
        cursor = connection.cursor()

        # Gets the information for the user from the 'PendingRUApplications' table.
        cursor.execute("SELECT * FROM PendingRUApplications WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        pending_application_data = cursor.fetchone()

        # Checks if the username exists in PendingRUApplications.
        if cursor.rowcount == 1:
            # Denies the user's application -- delete from the PendingRUApplications table.
            cursor.execute("DELETE FROM PendingRUApplications WHERE Username = %s", (username, ))

            # Commit the changes to the database.
            connection.commit()

            # TODO: Inform the applicant that their application has been denied.

    except Exception as e:
        # TODO: Inform the database admin that application was not denied.
        print('FAILED TO DENY APPLICATION FOR:', pending_application_data, flush=True)

# Bans a user from 'RegisteredUsers'.
def banRegisteredUser(username : str):
    # Cleans up the input for username.
    username = username.lower()

    # Stores registered user information.
    user_data = ''

    try:
        # Connects to the WeiBay LLC database.
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

        # Creates a cursor to execute user ban query.
        cursor = connection.cursor()

        # Gets the information for the user from the 'RegisteredUsers' table.
        cursor.execute("SELECT * FROM RegisteredUsers WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        user_data = cursor.fetchone()[1:5]

        # Checks if the username exists in RegisteredUsers.
        if cursor.rowcount == 1:
            # Bans the user -- delete from the RegisteredUsers table.
            cursor.execute("DELETE FROM RegisteredUsers WHERE Username = %s", (username, ))

            # Bans the user -- add to the BannedUsers table.
            cursor.execute("INSERT INTO BannedUsers VALUES (%s, %s, %s, %s)", user_data)

            # Commit the changes to the database.
            connection.commit()

            # TODO: Inform the user that they have been banned from the system.
    except Exception as e:
        # TODO: Inform the database admin that the user has not been banned.
        print('FAILED TO BAN USER:', user_data, flush=True)

# Authenticates a user into the application system.
def authenticate(username : str, pswd : str):
    # Cleans up the input for username.
    username = username.lower()

    try:
        # Connects to the WeiBay LLC database.
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

        # Creates a cursor to execute user login query.
        cursor = connection.cursor()

        # Gets the information to authenticate the user.
        cursor.execute("SELECT First_Name, Last_Name, Username, Email, Password, Role "
                       "FROM RegisteredUsers WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        user_data = cursor.fetchone()

        # Checks if the username is a registered user.
        if cursor.rowcount == 1:
            # Checks if the password is correct.
            if check_password_hash(user_data[4], pswd):
                # Gets the user in the context of the User model.
                user = get_user(username)

                # Logs the user in - sets up session variables for 'current_user'.
                login_user(user)

                # Signals the principal for the identity change.
                identity_changed.send(WeiBayLLC_App, identity=Identity(user.user_id))

                # Indicate successful authentication.
                return True
            else:
                # Raise an IncorrectPassword exception.
                raise IncorrectPassword
        # Checks if the user is pending approval.
        else:
            # Checks if the user is pending approval.
            cursor.execute("SELECT * FROM PendingRUApplications WHERE Username = %s", (username,))

            # Fetches the first result of the query.
            user_data = cursor.fetchone()

            # Checks if the username is a user pending approval.
            if cursor.rowcount == 1:
                # Raise an IncorrectPassword exception.
                raise PendingApproval
            # Checks if the user is banned.
            else:
                # Checks if the user is banned.
                cursor.execute("SELECT * FROM BannedUsers WHERE Username = %s", (username,))

                # Fetches the first result of the query.
                user_data = cursor.fetchone()

                # Checks if the username is a banned user.
                if cursor.rowcount == 1:
                    # Raise a BannedUser exception.
                    raise BannedUser
                else:
                    # Raise a user does not exist exception.
                    raise UserDNE

    # Re-throw exception for system-specific exceptions.
    except IncorrectPassword:
        raise IncorrectPassword
    except PendingApproval:
        raise PendingApproval
    except BannedUser:
        raise BannedUser
    except UserDNE:
        raise UserDNE

    # Catch other, system unrelated, exception.
    except Exception as e:
        print('FAILED TO AUTHENTICATE:', username, flush=True)

# Creates an instance of the Login Manager.
login_manager = LoginManager()

# Sets the default login page for the Login Manager.
login_manager.login_view = '_default.login'

# Initializes the Login Manager for the website application.
login_manager.init_app(WeiBayLLC_App)

# Gets the user in the context of the User model.
def get_user(username : str):
    # Cleans up the input for username.
    username = username.lower()

    try:
        # Connects to the WeiBay LLC database.
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

        # Creates a cursor to execute the user loader query.
        cursor = connection.cursor()

        # Gets the information for the registered user.
        cursor.execute("SELECT UserID, First_Name, Last_Name, Username, Email, Role "
                       "FROM RegisteredUsers WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        user_data = cursor.fetchone()

        # Checks
        if cursor.rowcount == 1:
            # Defines a user using the User model.
            user = User()

            # Sets the user ID.
            user.user_id = user_data[0]

            # Sets the first name.
            user.f_name = user_data[1]

            # Sets the last name.
            user.l_name = user_data[2]

            # Sets the username.
            user.username = user_data[3]

            # Sets the email.
            user.email = user_data[4]

            # Sets the role.
            user.role = user_data[5]

            # Sets the authentication status.
            user.authenticated = True

            # Returns the user.
            return user

    except Exception as e:
        print('FAILED TO GET USER:', username, flush=True)

@login_manager.user_loader
def load_user(username : str): # Defines the user loader for the login manager.
    return get_user(username)

# Creates an instance of the Principal.
principal = Principal()

# Initializes the Principal for the website application.
principal.init_app(WeiBayLLC_App)

# Create an admin permission.
admin_perm = Permission(RoleNeed(default_admin_role))

# Create a reg user permission.
registered_perm = Permission(RoleNeed(default_registered_role))

# Create an anonymous permission.
guest_perm = Permission(RoleNeed(default_gest_role))

@identity_loaded.connect_via(WeiBayLLC_App)
def on_identity_loaded(sender, identity):
    # Sets the identity of the user.
    identity.user = current_user

    # Checks if the current user is not anonymous.
    if not anonymous():
        # Sets the role of the user.
        identity.provides.add(RoleNeed(current_user.role))

# Checks if the current user is anonymous.
def anonymous():
    return current_user == None or not hasattr(current_user, 'authenticated')

# submitRUApplication('Andy', 'Zheng', 'Andy.Zheng@gmail.com', 'password', 'password')
# submitRUApplication('Cristian', 'Statescu', 'Cristian.Statescu@gmail.com', 'password', 'password')
# submitRUApplication('Brailinson', 'Disla', 'Brailinson.Disla@gmail.com', 'password', 'password', 'ADMIN')
# submitRUApplication('Manuel', 'Pohl', 'Manuel.Pohl@gmail.com', 'password', 'password')
# submitRUApplication('Talike', 'Bennett', 'Talike.Bennett@gmail.com', 'password', 'password')
#
# approveRUApplication('Brailinson.Disla')
# denyRUApplication('Cristian.Statescu')
# approveRUApplication('Andy.Zheng')
# banRegisteredUser('Andy.Zheng')