from DBConnection import dbCursor ,dbConnection
import os
from WeiBayLLC import WeiBayLLC_App 
def submit_listing(seller:int, name: str, description:str, condition:str, qty:int, price:float, img:str):
   try: 
        # @param Product_ID, Seller, Product_Name, Description, Condition, Quantity, Price, Rating, Image
        # !Find out how the add Images
        
        dbCursor.execute("INSERT INTO PendingApprovalProducts (`Seller`, `Product Name`, `Description`, `Condition`, `Quantity`, `Price`,`Image`)"
                         "VALUES (%s,%s,%s,%s,%s,%s,%s)",(seller, name, description, condition, qty, price, img))
        
        dbConnection.commit()
        
        print("Pending Approval Products")
   except Exception as e:
       return e
  
def img_grab(prod_id:int):
     dbCursor.execute("SELECT `Image` FROM PendingApprovalProducts WHERE `Product ID` = %s", (prod_id,))
     img_path = dbCursor.fetchone()[0]
     img_path_list = img_path.split('|')
     
     UPLOAD_FOLDER = 'static/img/items/'
     WeiBayLLC_App.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
     
     locations = []
     for paths in img_path_list:
          locations.append(os.path.join(WeiBayLLC_App.config['UPLOAD_FOLDER'],paths))
     
     return locations