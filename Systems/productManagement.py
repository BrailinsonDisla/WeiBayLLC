from DBConnection import dbCursor ,dbConnection

def submit_listing(seller:int, name: str, description:str, condition:str, qty:int, price:float,img):
   try: 
        # @param Product_ID, Seller, Product_Name, Description, Condition, Quantity, Price, Rating, Image
        # !Find out how the add Images
        
        dbCursor.execute("INSERT INTO PendingApprovalProducts (`Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`)"
                         "VALUES (%s,%s,%s,%s,%s,%s)",(seller, name, description, condition, qty, price))
        dbConnection.commit()
        
        print("Pending Approval Products")
   except Exception as e:
       return e