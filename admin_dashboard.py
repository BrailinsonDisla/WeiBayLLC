# Imports the connection from the DB Connection module.
from DBConnection import dbConnection, dbCursor

################################################# USER MANAGEMENT TAB ##################################################
# Queries the database for a list of users pending approval.
def getPendingApplicants():
    try:
        # Gets users pending approval from the database.
        dbCursor.execute("SELECT * FROM PendingApprovalUsers WHERE Role = 'RUSER'")

        # Fetches the results of the query.
        user_list = dbCursor.fetchall()

        # Returns a list of users pending approval.
        return user_list
    except:
        # TODO: Inform the admin that users pending approval could not be loaded.
        print('FAILED TO LOAD USERS PENDING APPROVAL', flush=True)

# Queries the database for a list of registered users.
def getRegisteredUsers():
    try:
        # Gets registered users from the database.
        dbCursor.execute("SELECT * FROM RegisteredUsers WHERE Role = 'RUSER'")

        # Fetches the results of the query.
        user_list = dbCursor.fetchall()

        # Returns a list of registered users.
        return user_list
    except:
        # TODO: Inform the admin that registered users could not be loaded.
        print('FAILED TO LOAD REGISTERED USERS', flush=True)

# Queries the database for a list of denied users.
def getDeniedUsers():
    try:
        # Gets denied users from the database.
        dbCursor.execute("SELECT * FROM DeniedUsers WHERE Role = 'RUSER'")

        # Fetches the results of the query.
        user_list = dbCursor.fetchall()

        # Returns a list of denied users.
        return user_list
    except:
        # TODO: Inform the admin that denied users could not be loaded.
        print('FAILED TO LOAD DENIED USERS', flush=True)

# Queries the database for a list of banned users.
def getBannedUsers():
    try:
        # Gets banned users from the database.
        dbCursor.execute("SELECT * FROM BannedUsers")

        # Fetches the results of the query.
        user_list = dbCursor.fetchall()

        # Returns a list of banned users.
        return user_list
    except:
        # TODO: Inform the admin that banned users could not be loaded.
        print('FAILED TO LOAD BANNED USERS', flush=True)

############################################### PRODUCT MANAGEMENT TAB #################################################
# Queries the database for products pending approval.
def getPendingProducts():
    try:
        # Gets products pending approval from the database.
        dbCursor.execute("SELECT * FROM PendingApprovalProducts")

        # Fetches the results of the query.
        product_list = dbCursor.fetchall()

        # Returns a list of products pending approval.
        return product_list
    except:
        # TODO: Inform the admin that products pending approval could not be loaded.
        print('FAILED TO LOAD PRODUCTS PENDING APPROVAL', flush=True)

# Queries the database for the products pending approval.
def getListedProducts():
    try:
        # Gets listed products from the database.
        dbCursor.execute("SELECT * FROM ListedProducts")

        # Fetches the results of the query.
        product_list = dbCursor.fetchall()

        # Returns a list of listed products.
        return product_list
    except:
        # TODO: Inform the admin that listed products could not be loaded.
        print('FAILED TO LOAD LISTED PRODUCTS', flush=True)

# Queries the database for the denied products.
def getDeniedProducts():
    try:
        # Gets denied products from the database.
        dbCursor.execute("SELECT * FROM DeniedProducts")

        # Fetches the results of the query.
        product_list = dbCursor.fetchall()

        # Returns a list of denied products.
        return product_list
    except:
        # TODO: Inform the admin that denied products could not be loaded.
        print('FAILED TO LOAD DENIED PRODUCTS', flush=True)

# Queries the database for the banned products.
def getBannedProducts():
    try:
        # Gets banned products from the database.
        dbCursor.execute("SELECT * FROM BannedProducts")

        # Fetches the results of the query.
        product_list = dbCursor.fetchall()

        # Returns a list of banned products.
        return product_list
    except:
        # TODO: Inform the admin that banned products could not be loaded.
        print('FAILED TO LOAD BANNED PRODUCTS', flush=True)

############################################### REPORT MANAGEMENT TAB ##################################################
# Queries the database for a list of reports pending approval.
def getPendingReports():
    try:
        # Gets reports pending approval from the database.
        dbCursor.execute("SELECT * FROM PendingApprovalReports")

        # Fetches the results of the query.
        report_list = dbCursor.fetchall()

        # Returns a list of reports pending approval.
        return report_list
    except:
        # TODO: Inform the admin that reports pending approval could not be loaded.
        print('FAILED TO LOAD REPORTS PENDING APPROVAL', flush=True)

# Queries the database for a list of approved reports.
def getApprovedReports():
    try:
        # Gets approved reports from the database.
        dbCursor.execute("SELECT * FROM ApprovedReports")

        # Fetches the results of the query.
        report_list = dbCursor.fetchall()

        # Returns a list of approved reports.
        return report_list
    except:
        # TODO: Inform the admin that approved reports could not be loaded.
        print('FAILED TO LOAD APPROVED REPORTS', flush=True)

# Queries the database for a list of denied reports.
def getDeniedReports():
    try:
        # Gets denied reports from the database.
        dbCursor.execute("SELECT * FROM DeniedReports")

        # Fetches the results of the query.
        report_list = dbCursor.fetchall()

        # Returns a list of denied reports.
        return report_list
    except:
        # TODO: Inform the admin that denied reports could not be loaded.
        print('FAILED TO LOAD DENIED REPORTS', flush=True)