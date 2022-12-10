## USER-APPLICATION-RELATED ##
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

## USER-AUTHENTICATION-RELATED ##
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

## PRODUCT-APPLICATION-RELATED ##
# Exception for invalid user id.
class InvalidSellerID(Exception):
    pass

# Exception for invalid product name.
class InvalidProductName(Exception):
    pass

# Exception for invalid product description.
class InvalidDescription(Exception):
    pass

# Exception for invalid price.
class InvalidPrice(Exception):
    pass

# Exception for products pending approval.
class PendingProductApproval(Exception):
    pass

# Exception for listed products.
class ListedProduct(Exception):
    pass

# Exception for denied products.
class DeniedProduct(Exception):
    pass

# Exception for banned products.
class BannedProduct(Exception):
    pass

## REPORT-SUBMISSION-RELATED ##
# Exception for invalid product id.
class InvalidProductID(Exception):
    pass

# Exception for invalid reporter id.
class InvalidReporterID(Exception):
    pass

# Exception for invalid reason.
class InvalidReason(Exception):
    pass

# Exception for report pending approval.
class PendingReportApproval(Exception):
    pass

# Exception for approved report.
class ApprovedReport(Exception):
    pass

# Except for denied report.
class DeniedReport(Exception):
    pass
