# Imports the connection from the DB Connection module.
from DBConnection import dbConnection, dbCursor

# Imports user-defined exceptions.
from UD_Exceptions import *

# Imports generic functions.
from generic import titleCase, paragraphCase

# Submits a product listing for approval.
def submitProduct(selled_id: int, prod_name: str, desc: str, cond: str, quantity: int, price: float):
    # Checks if the selled_id id is invalid.
    if selled_id <= 0:
        # Raise an InvalidSellerID exception.
        raise InvalidSellerID

    # Cleans up the product name.
    prod_name = titleCase(prod_name)

    # Formats the product condition.
    cond = cond.upper()

    # Checks for valid product condition.
    cond = cond if cond in ['NEW', 'USED'] else 'NEW'

    # Defines invalid values for application fields.
    invalid_values = [None, '']

    # Checks if the product name is invalid.
    if prod_name in invalid_values:
        # Raise an InvalidProductName exception.
        raise InvalidProductName

    # Checks if the description is invalid.
    if desc in invalid_values:
        # Raise an InvalidDescription exception.
        raise InvalidDescription

    # Checks for valid quantity.
    quantity = 1 if quantity <= 0 else quantity;

    # Checks if the price is invalid.
    if price <= 0:
        # Raise an InvalidPrice exception.
        raise InvalidPrice

    # Stores product information.
    product_data = ''

    try:
        # Checks if the product has a pending approval.
        dbCursor.execute("SELECT * FROM PendingApprovalProducts "
                         "WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the product exists in PendingApprovalProducts.
        if dbCursor.rowcount == 1:
            # Raise a PendingProductApproval exception.
            raise PendingProductApproval

        # Checks if the product is listed.
        dbCursor.execute("SELECT * FROM ListedProducts "
                         "WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the product exists in ListedProducts.
        if dbCursor.rowcount == 1:
            # Raise ListedProduct exception.
            raise ListedProduct

        # Checks if the product is denied.
        dbCursor.execute("SELECT * FROM DeniedProducts "
                         "WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the product exists in DeniedProducts.
        if dbCursor.rowcount == 1:
            # Raise DeniedProduct exception.
            raise DeniedProduct

        # Checks if the product is banned.
        dbCursor.execute("SELECT * FROM BannedProducts "
                         "WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

        # Fetches the first result of the query.
        dbCursor.fetchone()

        # Checks if the product exists in BannedProducts.
        if dbCursor.rowcount == 1:
            # Raise BannedProduct exception.
            raise BannedProduct

        # Creates a tuple with the values to insert.
        product_data = (selled_id, prod_name, desc, cond, quantity, price)

        # Submits the product to the pending approval queue.
        dbCursor.execute("INSERT INTO PendingApprovalProducts (`Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`) "
                         "VALUES (%s, %s, %s, %s, %s, %s)", product_data)

        # Commits the changes to the database.
        dbConnection.commit()

        # TODO: Inform the applicant that their product listing has been submitted for approval.

    # Re-throw exception for system-specific exceptions.
    except PendingProductApproval:
        raise PendingProductApproval
    except ListedProduct:
        raise ListedProduct
    except DeniedProduct:
        raise DeniedProduct
    except BannedProduct:
        raise BannedProduct

    # Catches other, system unrelated, exception.
    except Exception as e:
        # TODO: Inform the user that their product was not submitted.
        print('FAILED TO SUBMIT PRODUCT FOR:', product_data, flush=True)

# Approves the product listing.
def approveProductListing(selled_id: int, prod_name: str):
    # Cleans up the product name.
    prod_name = titleCase(prod_name)

    # Stores pending product listing information.
    product_data = ''

    try:
        # Gets the information for the listing from the 'PendingApprovalProducts' table.
        dbCursor.execute("SELECT `Product ID`, `Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`, `Rating` "
                         "FROM PendingApprovalProducts WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id,))

        # Fetches the first result of the query.
        product_data = dbCursor.fetchone()

        # Checks if the product listing exists in PendingApprovalProducts.
        if dbCursor.rowcount == 1:
            # Approves the product listing -- add to the ListedProducts table.
            dbCursor.execute("INSERT INTO ListedProducts (`Product ID`, `Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`, `Rating`) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", product_data)

            # Approves the product listing -- delete from the PendingApprovalProducts table.
            dbCursor.execute("DELETE FROM PendingApprovalProducts WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

            # Commits the changes to the database.
            dbConnection.commit()

            # TODO: Inform the admin that the product was listed.
    except Exception as e:
        # TODO: Inform the database admin that product was not approved.
        print('FAILED TO APPROVE LISTING FOR:', product_data, flush=True)

# Denies the product listing.
def denyProductListing(selled_id: int, prod_name: str):
    # Cleans up the product name.
    prod_name = titleCase(prod_name)

    # Stores denied information.
    product_data = ''

    try:
        # Gets the information for the listing from the 'PendingApprovalProducts' table.
        dbCursor.execute("SELECT `Product ID`, `Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`, `Rating` "
                         "FROM PendingApprovalProducts WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id,))

        # Fetches the first result of the query.
        product_data = dbCursor.fetchone()

        # Checks if the product listing exists in PendingApprovalProducts.
        if dbCursor.rowcount == 1:
            # Denies the product listing -- add to the DeniedProducts table.
            dbCursor.execute("INSERT INTO DeniedProducts (`Product ID`, `Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`, `Rating`) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", product_data)

            # Denies the product listing -- delete from the PendingApprovalProducts table.
            dbCursor.execute("DELETE FROM PendingApprovalProducts WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

            # Commits the changes to the database.
            dbConnection.commit()

            # TODO: Inform the admin that the product was denied.
    except Exception as e:
        # TODO: Inform the database admin that product was not denied.
        print('FAILED TO DENY LISTING FOR:', product_data, flush=True)

# Bans the product listing.
def banProductListing(selled_id: int, prod_name: str):
    # Cleans up the product name.
    prod_name = titleCase(prod_name)

    # Stores banned product information.
    product_data = ''

    try:
        # Gets the information for the listing from the 'ListedProducts' table.
        dbCursor.execute("SELECT `Product ID`, `Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`, `Rating` "
                         "FROM ListedProducts WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id,))

        # Fetches the first result of the query.
        product_data = dbCursor.fetchone()

        # Checks if the product listing exists in ListedProducts.
        if dbCursor.rowcount == 1:
            # Bans the product listing -- add to the BannedProducts table.
            dbCursor.execute("INSERT INTO BannedProducts (`Product ID`, `Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`, `Rating`) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", product_data)

            # Bans the product listing -- delete from the ListedProducts table.
            dbCursor.execute("DELETE FROM ListedProducts WHERE `Product Name` = %s AND `Seller` = %s", (prod_name, selled_id))

            # Commits the changes to the database.
            dbConnection.commit()

            # TODO: Inform the admin that the product was banned.
    except Exception as e:
        # TODO: Inform the database admin that product was not banned.
        print('FAILED TO BAN LISTING FOR:', product_data, flush=True)