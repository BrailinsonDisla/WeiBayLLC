# Imports the tools required from the Account Management module.
from accountManagement import anonymous, current_user

# Imports the connection from the DB Connection module.
import time

# Imports the connection from the DB Connection module.
from DBConnection import dbConnection, dbCursor

# Imports user-defined exceptions.
from UD_Exceptions import *

# Submits an order.
def submitOrder(cart : dict, bid = False, bidder_id = None, bid_amount = None):
    # Stores the order's information.
    order_data = ''

    # Checks if the user is anonymous.
    if not anonymous():
        # Gets the product list from the cart.
        prod_list = cart.keys()
        print(prod_list)
        # TODO: CHECK IF QUANTITY IF OK.

        # Sets the buyer's id.
        buyer_id = current_user.user_id

        # Creates an order ID based on user ID and time.
        order_id = buyer_id + int(time.time() % 100000)

        try:
            # Checks if the user has an address on file.
            if current_user.addressFK is None:
                raise NoAddressOnFile

            # Calculates the sum of prices for the product list.
            dbCursor.execute("SELECT SUM(Price) FROM ListedProducts WHERE `Product ID` IN {}".format(prod_list))

            # Fetches the first result of the query.
            total = dbCursor.fetchone()

            # Checks if total exists.
            if dbCursor.rowcount == 1:
                # Gets the order total.
                total = total[0]

                # TODO: CHECKS IF THE USER HAS MONEY.

                # Gets te date in SQL format.
                date = time.strftime('%Y-%m-%d %H:%M:%S')

                # Checks if the order is a bid approval.
                if bid:
                    # Checks if the bid amount  is equal or more than the price.
                    if bid_amount < total:
                        raise BidLessThanPrice

                    # Sets the total to the bid amount.
                    total = bid_amount

                    # Sets the buyer to the bidder's id.
                    buyer_id = bidder_id

                # Creates a tuple with the values to insert.
                order_data = (order_id, buyer_id, total, date, current_user.addressFX)

                # Submits the user's order.
                dbCursor.execute("INSERT INTO Orders (`Order ID`, `Buyer ID`, `Total`, `Order Date`, `Shipping Address`) "
                                "VALUES (%s, %s, %s, %s, %s)", order_data)

                # Goes through each product ID.
                for prod_id in prod_list:
                    # Adds the order ID to product ID mapping into the ProductsInOrder table.
                    dbCursor.execute("INSERT INTO ProductsInOrder (`Order ID`, `Product ID`) "
                                     "VALUES (%s, %s)", (order_id, prod_id))

                # Commits the changes to the database.
                dbConnection.commit()
        # Re-throw exception for system-specific exceptions.
        except NoAddressOnFile:
            raise NoAddressOnFile
        except BidLessThanPrice:
            raise BidLessThanPrice
        # Catches other, system unrelated, exception.
        except Exception as e:
            # TODO: Inform the admin that their order was not submitted..
            print('FAILED TO PLACE ORDER FOR:', order_data, flush=True)

# Submits a bid.
def submitBid(prod_id : int, bid_amount: float, quantity = 1, uid = 1):
    # Stores the bid's information.
    bid_data = ''

    # Checks if the user is anonymous.
    if not anonymous():
        # Sets the bidder ID.
        bidder_id = uid#current_user.user_id bidder_id + int(time() % 100000)

        # Creates a bid ID based on user ID and time.
        bid_id = '1' + str(bidder_id + int(time.time() % 10000))

        # Formats the bid ID.
        bid_id = int(bid_id)

        try:
            # Gets the product price.
            dbCursor.execute("SELECT Price FROM ListedProducts WHERE `Product ID` = %s", (prod_id,))

            # Fetches the first result of the query.
            price = dbCursor.fetchone()

            # Checks if price exists.
            if dbCursor.rowcount == 1:
                # Gets the product's price.
                price = price[0]

                # Checks if bid amount is less than price.
                if bid_amount < price:
                    raise InvalidBidAmount

                # TODO: CHECK IF THE USER HAS ENOUGH MONEY.

                # Gets te date in SQL format.
                date = time.strftime('%Y-%m-%d %H:%M:%S')

                # Creates a tuple with the values to insert.
                bid_data = (bid_id, bidder_id, prod_id, quantity, bid_amount, date)

                # Submits the user's bid.
                dbCursor.execute("INSERT INTO Bids (`Bid ID`, `Bidder ID`, `Product ID`, `Quantity`, `Bid Amount`, `Bid Date`) "
                                 "VALUES (%s, %s, %s, %s, %s, %s)", bid_data)

                # Commits the changes to the database.
                dbConnection.commit()

        # Re-throw exception for system-specific exceptions.
        except InvalidBidAmount:
            raise InvalidBidAmount
        # TODO: CATCH WHEN NOT ENOUGH MONEY

        # Catches other, system unrelated, exception.
        except Exception as e:
            raise e
            # TODO: Inform the applicant that their bid was not submitted.
            print('FAILED TO PLACE BID FOR:', bid_data, flush=True)

# Approves a bid.
def approveBid(bid_id: int):
    # Stores the bid information.
    bid_data = ''

    # Checks if the user is anonymous.
    if not anonymous():
        try:
            # Gets the information for bid.
            dbCursor.execute("SELECT * FROM Bids WHERE `Bid ID` = %s", (bid_id,))

            # Checks if price exists.
            if dbCursor.rowcount == 1:
                # Fetches the first result of the query.
                bid_data = dbCursor.fetchone()

                # Sets the bidder ID.
                bidder_id = bid_data[1]

                # Sets the product ID.
                prod_id = bid_data[2]

                # Gets the quantity of products.
                quantity = bid_data[3]

                # Sets the bid amount.
                bid_amount = quantity * bid_data[4]

                # Submits the bid as an order.
                submitOrder({prod_id : quantity}, bid=True, bidder_id=bidder_id, bid_amount=bid_amount)

                # Approves the bid -- delete from the Bids table.
                dbCursor.execute("DELETE FROM Bids WHERE `Bid ID` = %s", (bid_id,))

                # Approves the bid -- add to the ApprovedBids table.
                dbCursor.execute("INSERT INTO ApprovedBids (`Bid ID`, `Bidder ID`, `Product ID`, `Quantity`, `Bid Amount`, `Bid Date`) "
                                 "VALUES (%s, %s, %s, %s, %s, %s)", bid_data)

                # Commit the changes to the database.
                dbConnection.commit()
        # Re-throw exception for system-specific exceptions.
        except BidLessThanPrice:
            raise BidLessThanPrice

        # Catches other, system unrelated, exception.
        except Exception as e:
            raise e
            # TODO: Inform the seller that the bid was not processed.
            print('FAILED TO APPROVE BID FOR:', bid_data, flush=True)

























