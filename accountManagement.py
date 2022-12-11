# Imports the tools required from flask_login for Permission Management.
from flask_principal import Principal, Permission, RoleNeed, Identity, AnonymousIdentity

# Imports the hashing functionalities from werkzeug.security for authentication.
from werkzeug.security import generate_password_hash, check_password_hash

# Imports the tools required from flask_login for Login Management.
from flask_login import LoginManager, login_user, current_user, login_required

# Imports the regular expression module (as regEx) for pattern matching.
import re as regEx

# Imports the flask website application and required tools.
from WeiBayLLC import WeiBayLLC_App

# Imports the connection from the DB Connection module.
from DBConnection import dbConnection, dbCursor

# Imports user-defined exceptions.
from UD_Exceptions import *

# Imports required DB model.
from DBModels import User, Anonymous

# Defines the admin role.
default_admin_role = 'ADMIN'

# Defines the registered user role.
default_registered_role = 'RUSER'

# Defines the guest user role.
default_gest_role = 'GUEST'

# Checks if the given email is valid.
def validEmail(email: str):
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
            pswd_hash = generate_password_hash(pswd, method='sha256')

    # Extracts the username from the email.
    username = email.split(sep='@')[0]

    # Stores the applicant's information.
    application_data = ''

    try:
        # Checks if the user has a pending application.
        dbCursor.execute("SELECT `Username` FROM PendingApprovalUsers WHERE `Username` = %s", (username, ))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the username exists in PendingApprovalUsers.
        if dbCursor.rowcount == 1:
            # Raise a PendingApplication exception.
            raise PendingApplicant

        # TODO: HANDLE FOR DeniedUsers

        # Checks if the user is already registered.
        dbCursor.execute("SELECT `Username` FROM RegisteredUsers WHERE `Username` = %s", (username,))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the username exists in RegisteredUsers.
        if dbCursor.rowcount == 1:
            # Raise AlreadyRegistered exception.
            raise AlreadyRegistered

        # Checks if the user is banned.
        dbCursor.execute("SELECT `Username` FROM BannedUsers WHERE `Username` = %s", (username,))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the username exists in BannedUsers.
        if dbCursor.rowcount == 1:
            # Raise BannedApplicant exception.
            raise BannedApplicant

        # Creates a tuple with the values to insert.
        application_data = (f_name, l_name, username, email, pswd_hash, role)

        # Submits the user's application to the pending approval queue.
        dbCursor.execute("INSERT INTO PendingApprovalUsers (`First Name`, `Last Name`, `Username`, `Email`, `Password`, `Role`) "
                        "VALUES (%s, %s, %s, %s, %s, %s)", application_data)

        # Commits the changes to the database.
        dbConnection.commit()

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

# Approves RU application from 'PendingApprovalUsers'.
def approveRUApplication(username: str):
    # Cleans up the input for username.
    username = username.lower()

    # Stores pending application information.
    pending_application_data = ''

    try:
        # Gets the information for the user from the 'PendingApprovalUsers' table.
        dbCursor.execute("SELECT `User ID`, `First Name`, `Last Name`, Username, Email, Password, `Role` "
                         "FROM PendingApprovalUsers WHERE Username = %s", (username,))

        # Fetches the first result of the query.
        pending_application_data = dbCursor.fetchone()

        # Checks if the username exists in PendingApprovalUsers.
        if dbCursor.rowcount == 1:
            # Approves the user's application -- add to the RegisteredUsers table.
            dbCursor.execute("INSERT INTO RegisteredUsers(`User ID`, `First Name`, `Last Name`, Username, Email, Password, `Role`) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s)", pending_application_data)

            # Approves the user's application -- delete from the PendingApprovalUsers table.
            dbCursor.execute("DELETE FROM PendingApprovalUsers WHERE Username = %s", (username, ))

            # Commits the changes to the database.
            dbConnection.commit()

            # TODO: Inform the applicant that their application has been approved.
    except Exception as e:
        # TODO: Inform the database admin that application was not approved.
        print('FAILED TO APPROVE APPLICATION FOR:', pending_application_data, flush=True)

# Denies RU application from 'PendingApprovalUsers'.
def denyRUApplication(username: str):
    # Cleans up the input for username.
    username = username.lower()

    # Stores pending application information.
    pending_application_data = ''

    try:
        # Gets the information for the user from the 'PendingApprovalUsers' table.
        dbCursor.execute("SELECT `User ID`, `First Name`, `Last Name`, `Username`, `Email`, `Password`, `Role` "
                         "FROM PendingApprovalUsers WHERE `Username` = %s", (username,))

        # Fetches the first result of the query.
        pending_application_data = dbCursor.fetchone()

        # Checks if the username exists in PendingApprovalUsers.
        if dbCursor.rowcount == 1:
            # Denies the user's application -- add to the DeniedUsers table.
            dbCursor.execute("INSERT INTO DeniedUsers(`User ID`, `First Name`, `Last Name`, `Username`, `Email`, `Password`, `Role`) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s)", pending_application_data)

            # Denies the user's application -- delete from the PendingApprovalUsers table.
            dbCursor.execute("DELETE FROM PendingApprovalUsers WHERE `Username` = %s", (username, ))

            # Commit the changes to the database.
            dbConnection.commit()

            # TODO: Inform the applicant that their application has been denied.

    except Exception as e:
        # TODO: Inform the database admin that application was not denied.
        print('FAILED TO DENY APPLICATION FOR:', pending_application_data, flush=True)

# Bans a user from 'RegisteredUsers'.
def banRegisteredUser(username: str):
    # Cleans up the input for username.
    username = username.lower()

    # Stores registered user information.
    user_data = ''

    try:
        # Gets the information for the user from the 'RegisteredUsers' table.
        dbCursor.execute("SELECT * FROM RegisteredUsers WHERE `Username` = %s", (username,))

        # Fetches the first result of the query.
        user_data = dbCursor.fetchone()

        # Checks if the username exists in RegisteredUsers.
        if dbCursor.rowcount == 1:
            # Bans the user -- delete from the RegisteredUsers table.
            dbCursor.execute("DELETE FROM RegisteredUsers WHERE `Username` = %s", (username, ))

            # Bans the user -- add to the BannedUsers table.
            dbCursor.execute("INSERT INTO BannedUsers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", user_data)

            # Commit the changes to the database.
            dbConnection.commit()

            # TODO: Inform the user that they have been banned from the system.
    except Exception as e:
        # TODO: Inform the database admin that the user has not been banned.
        print('FAILED TO BAN USER:', user_data, flush=True)

# Creates an instance of Principal.
principal = Principal()

# Creates an instance of the Login Manager.
login_manager = LoginManager()

# Initializes the Principal for the website application.
principal.init_app(WeiBayLLC_App)

# Initializes the Login Manager for the website application.
login_manager.init_app(WeiBayLLC_App)

# Sets the default login page for the Login Manager.
login_manager.login_view = '_default.login'

# Sets the default anonymous user for the Login Manager.
login_manager.anonymous_user = Anonymous

# Gets the user in the context of the User model.
def get_user(username: str):
    # Cleans up the input for username.
    username = username.lower()

    try:
        # Gets the information for the registered user.
        dbCursor.execute("SELECT * FROM RegisteredUsers WHERE `Username` = %s", (username,))

        # Fetches the first result of the query.
        user_data = dbCursor.fetchone()

        # Checks if a user exists.
        if dbCursor.rowcount == 1:
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

            # Sets the password.
            # user.password = user_data[5]

            # Sets the role.
            user.role = user_data[6]

            # Sets the phone number.
            user.phone = user_data[7]

            # Sets the address FK.
            user.addressFK = user_data[8]

            # Sets the bank account FK.
            user.bankAccountFK = user_data[9]

            # Returns the user.
            return user

    except Exception as e:
        print('FAILED TO GET USER:', username, flush=True)

# Authenticates a user into the application system.
def authenticate(username: str, pswd: str):
    # Cleans up the input for username.
    username = username.lower()

    try:
        # Gets the information to authenticate the user.
        dbCursor.execute("SELECT * FROM RegisteredUsers WHERE `Username` = %s", (username,))

        # Fetches the first result of the query.
        user_data = dbCursor.fetchone()

        # Checks if the username is a registered user.
        if dbCursor.rowcount == 1:
            # Checks if the password is correct.
            if check_password_hash(user_data[5], pswd):

                # Checks if the current user is anonymous.
                if anonymous():
                    # Gets the user in the context of the User model.
                    user = get_user(username)

                    # Logs the user in - sets up session variables for 'current_user'.
                    login_user(user)

                    # Sets the identity for the user logged in.
                    setGlobalIdentity(user)

                    # # Sets the identity of the user logged in.
                    # principal.set_identity(g.identity)

                    # Indicate successful authentication.
                    return True
            else:
                # Raise an IncorrectPassword exception.
                raise IncorrectPassword
        # Checks if the user is pending approval.
        else:
            # Checks if the user is pending approval.
            dbCursor.execute("SELECT * FROM PendingApprovalUsers WHERE `Username` = %s", (username,))

            # Fetches the first result of the query.
            user_data = dbCursor.fetchone()

            # Checks if the username is a user pending approval.
            if dbCursor.rowcount == 1:
                # Raise an IncorrectPassword exception.
                raise PendingApproval
            # Checks if the user is banned.
            else:
                # Checks if the user is banned.
                dbCursor.execute("SELECT * FROM BannedUsers WHERE `Username` = %s", (username,))

                # Fetches the first result of the query.
                user_data = dbCursor.fetchone()

                # Checks if the username is a banned user.
                if dbCursor.rowcount == 1:
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

# Create an admin role.
admin_role = RoleNeed(default_admin_role)

# Create an admin permission.
admin_perm = Permission(RoleNeed(default_admin_role))

# Create a reg user role.
registered_role = RoleNeed(default_registered_role)

# Create a reg user permission.
registered_perm = RoleNeed(default_registered_role)

# Create an anonymous role.
guest_role = RoleNeed(default_gest_role)

# Create an anonymous permission.
guest_perm = Permission(RoleNeed(default_gest_role))

@login_manager.user_loader
def load_user(username: str): # Defines the user loader for the login manager.

    # Gets the user logged in.
    user = get_user(username)


    # Sets the identity of the user logged in.
    setGlobalIdentity(user)

    # Returns the loaded user.
    return user

# Sets the identity and its permissions for the user.
def setGlobalIdentity(user: User):
    # Gets the role of the user logged in.
    role = user.role

    # Creates an identity for the user logged in.
    identity = Identity(user.username)


    # Sets the user for the identity.
    identity.user = user

    # Grant permissions based on role.
    if role == default_admin_role:
        identity.provides.add(admin_role)
    elif role == default_registered_role:
        identity.provides.add(registered_role)
    else:
        identity.provides.add(guest_role)

    # Returns the identity.
    g.identity = identity

# Checks if the current user is anonymous.
def anonymous():
    return current_user == None or not hasattr(current_user, 'authenticated')

# Checks if the current identity is anonymous.
def anonymousIdentity():
    return g.identity == None or not hasattr(g.identity, 'id')