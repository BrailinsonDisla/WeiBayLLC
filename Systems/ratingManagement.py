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
        dbCursor.execute("SELECT * FROM ORDERS WHERE `Buyer ID`=? AND `Product ID`=?", (self.id, self.product))

    # Fetch the result of the query
        result = dbCursor.fetchone()
        # Check if the user has purchased the product
        if result is None:
            print("Sorry, you cannot make a review for this product because you have not purchased it.")
        else:
            seller_id = self.get_seller_id()
            dbCursor.execute("INSERT INTO RATINGS VALUES(%s, %s, %s, %s)", (self.product, seller_id , self.user, grade))
            # Check if the current user wrote too many extreme reviews
            self.sus_rate()
    
    # Get the Seller ID base on the product ID
    def get_seller_id(self):
        dbCursor.execute("SELECT `Seller` FROM ListedProducts WHERE `Product ID` = %s", (self.product)) 
        
        #Get the Seller Id for the sold product 
        seller_id = dbCursor.fetchone()[0]
        return seller_id
        
    def  sus_rate(self):
        dbCursor.execute("SELECT * FROM RATINGS WHERE GRADE = '1' GROUP BY BUYER_ID HAVING COUNT(*) = 3"
        "UNION SELECT * FROM RATINGS WHERE GRADE = '5' GROUP BY BUYER_ID HAVING COUNT(*) = 3")
        
        results = dbCursor.fetchall()
        if len(results):
            reason = "User has made more then at least 3 negative reviews or  3 positive reviews."
            seller_id = self.get_seller_id()
            submitReport(self.product,seller_id,self.id,reason)
        