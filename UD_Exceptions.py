## APPLICATION-RELATED ##
# Exception for an invalid first name.
class InvalidFirstName(Exception):
    pass

# Exception for an invalid last name.
class InvalidLastName(Exception):
    pass

# Exception for an invalid email.
class InvalidEmail(Exception):
    pass

# Exception for an invalid Password.
class InvalidPassword(Exception):
    pass

# Exception for password mismatch.
class PasswordMismatch(Exception):
    pass

# Exception for pending applicants.
class PendingApplicant(Exception):
    pass

# Exception for already registered applicants.
class AlreadyRegistered(Exception):
    pass

# Exception for banned applicants.
class BannedApplicant(Exception):
    pass

## AUTHENTICATION-RELATED ##
# Exception for incorrect password.
class IncorrectPassword(Exception):
    pass

# Exception for pending approval.
class PendingApproval(Exception):
    pass

# Exception for banned user.
class BannedUser(Exception):
    pass

# Exception for non-existent user.
class UserDNE(Exception):
    pass