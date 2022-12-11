from mysql.connector import *
from flask_login import current_user
from accountManagement import anonymous
from DBConnection import *
from flask import Flask, redirect
from  reportsManagement import submitReport

class Rating:
    dbCursor
    def __init__(self):
        self.user = current_user.username
        self.id = current_user.user_id
        self.product = "Product" # TODO: Check the its reviewing
        
    def rate_trans(self, grade : int):
        # !function to check if the user purchase the product 
        dbCursor.execute("SELECT * FROM ORDERS WHERE `Buyer ID`=? AND product_id=?", self.id, self.product)

    # Fetch the result of the query
        result = dbCursor.fetchone()

        # Check if the user has purchased the product
        if result is None:
            print("Sorry, you cannot make a review for this product because you have not purchased it.")
        else:
            dbCursor.execute("INSERT INTO REVIEWS VALUES(%s, %s, %s)", (self.user, self.product, grade))
            # Check if the current user wrote too many extreme reviews
            self.sus_rate()
    
    def  sus_rate(self):
        dbCursor.execute("SELECT * FROM REVIEWS WHERE grade = '1' GROUP BY user_id HAVING COUNT(*) = 3"
        "UNION SELECT * FROM REVIEWS WHERE grade = '5' GROUP BY user_id HAVING COUNT(*) = 3")
        
        results = dbCursor.fetchall()
        if len(results):
            reason = "User has made more then at least 3 negative reviews or  3 positive reviews."
            #!check seller_id by checking the product seller OR make a new submitReport
            submitReport(self.product,seller_id,self.id,reason)
        