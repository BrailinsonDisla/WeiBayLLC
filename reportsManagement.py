# Imports the connection from the DB Connection module.
from DBConnection import dbConnection, dbCursor

# Imports user-defined exceptions.
from UD_Exceptions import *

# Imports generic functions.
from generic import paragraphCase

# Submits a report for approval.
def submitReport(prod_id: int, seller_id: int, reporter_id: int, subject: str, reason: str):
    #! Checks if the product id is invalid.
    #// if prod_id <= 0:
    #//     # Raise an InvalidProductID exception.
    #//     raise InvalidProductID

    #// # Checks if the seller id is invalid.
    #// if seller_id <= 0:
    #//     # Raise an InvalidSellerID exception.
    #//     raise InvalidSellerID

    #// # Checks if the reporter id is invalid.
    #// if reporter_id <= 0:
    #//     # Raise an InvalidReporterID exception.
    #//     raise InvalidReporterID
    #!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
    # Cleans up the reason.
    reason = paragraphCase(reason)

    # Defines invalid values for report fields.
    invalid_values = [None, '']

    # Checks if the reason field is invalid.
    if reason in invalid_values:
        # Raise an InvalidReason exception.
        raise InvalidReason
    
    # Checks if the subject field is invalid.
    if subject in invalid_values:
        # Raise an InvalidSubject exception.
        raise InvalidSubject

    # Stores report information.
    report_data = ''

    try:
        # Checks if the report has a pending approval.
        dbCursor.execute("SELECT * FROM PendingApprovalReports "
                         "WHERE `Product ID` = %s AND `Seller ID` = %s "
                                "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the report exists in PendingApprovalReports.
        if dbCursor.rowcount == 1:
            # Raise a PendingReportApproval exception.
            raise PendingReportApproval

        # Checks if the report has been approved.
        dbCursor.execute("SELECT * FROM ApprovedReports "
                         "WHERE `Product ID` = %s AND `Seller ID` = %s "
                                "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the report exists in ApprovedReports.
        if dbCursor.rowcount == 1:
            # Raise ApprovedReport exception.
            raise ApprovedReport

        # Checks if the report is denied.
        dbCursor.execute("SELECT * FROM DeniedReports "
                         "WHERE `Product ID` = %s AND `Seller ID` = %s "
                                "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the report exists in DeniedReports.
        if dbCursor.rowcount == 1:
            # Raise DeniedReport exception.
            raise DeniedReport

        # Creates a tuple with the values to insert.
        report_data = (prod_id, seller_id, reporter_id, subject, reason)

        # Submits the report to the pending approval queue.
        dbCursor.execute("INSERT INTO PendingApprovalReports (`Product ID`, `Seller ID`, `Reporter ID`, `Subject`, `Reason`) "
                         "VALUES (%s, %s, %s, %s,%s)", report_data)

        # Commits the changes to the database.
        dbConnection.commit()

        # TODO: Inform the applicant that their report has been submitted for approval.

    # Re-throw exception for system-specific exceptions.
    except PendingReportApproval:
        raise PendingReportApproval
    except ApprovedReport:
        raise ApprovedReport
    except DeniedReport:
        raise DeniedReport

    # Catches other, system unrelated, exception.
    except Exception as e:
        # TODO: Inform the user that their report was not submitted.
        print('FAILED TO SUBMIT REPORT FOR:', report_data, flush=True)

# Approves the report.
def approveReport(prod_id: int, seller_id: int, reporter_id: int):
    # Stores report information.
    report_data = ''

    try:
        # Gets the information for the report from the 'PendingApprovalReports' table.
        dbCursor.execute("SELECT `Report ID`, `Product ID`, `Seller ID`, `Reporter ID`, `Subject`, `Reason` "
                         "FROM PendingApprovalReports WHERE `Product ID` = %s AND `Seller ID` = %s "
                                                    "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

        # Fetches the first result of the query.
        report_data = dbCursor.fetchone()

        # Checks if the report exists in PendingApprovalReports.
        if dbCursor.rowcount == 1:
            # Approves the report -- add to the ApprovedReports table.
            dbCursor.execute("INSERT INTO ApprovedReports (`Report ID`, `Product ID`, `Seller ID`, `Reporter ID`, `Subject`, `Reason`) "
                             "VALUES (%s, %s, %s, %s, %s, %s)", report_data)

            # Approves the report -- delete from the PendingApprovalReports table.
            dbCursor.execute("DELETE FROM PendingApprovalReports WHERE `Product ID` = %s AND `Seller ID` = %s "
                                                    "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

            # Commits the changes to the database.
            dbConnection.commit()

            # TODO: Inform the admin that the report was approved.
    except Exception as e:
        # TODO: Inform the database admin that report was not approved.
        print('FAILED TO APPROVE REPORT FOR:', report_data, flush=True)

# Denies the report.
def denyReport(prod_id: int, seller_id: int, reporter_id: int):
    # Stores report information.
    report_data = ''

    try:
        # Gets the information for the report from the 'PendingApprovalReports' table.
        dbCursor.execute("SELECT `Report ID`, `Product ID`, `Seller ID`, `Reporter ID`, `Subject`, `Reason` "
                         "FROM PendingApprovalReports WHERE `Product ID` = %s AND `Seller ID` = %s "
                         "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

        # Fetches the first result of the query.
        report_data = dbCursor.fetchone()

        # Checks if the report exists in PendingApprovalReports.
        if dbCursor.rowcount == 1:
            # Denies the report -- add to the DeniedReports table.
            dbCursor.execute(
                "INSERT INTO DeniedReports (`Report ID`, `Product ID`, `Seller ID`, `Reporter ID`, `Subject`, `Reason`) "
                "VALUES (%s, %s, %s, %s, %s, %s)", report_data)

            # Denies the report -- delete from the PendingApprovalReports table.
            dbCursor.execute("DELETE FROM PendingApprovalReports WHERE `Product ID` = %s AND `Seller ID` = %s "
                             "AND `Reporter ID` = %s", (prod_id, seller_id, reporter_id))

            # Commits the changes to the database.
            dbConnection.commit()

            # TODO: Inform the admin that the report was denied.
    except Exception as e:
        # TODO: Inform the database admin that report was not denied.
        print('FAILED TO DENY REPORT FOR:', report_data, flush=True)