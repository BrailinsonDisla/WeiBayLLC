from mysql.connector import *
from mysql.connector import connect
from flask_login import LoginManager, login_user, current_user
from WeiBayLLC import WeiBayLLC_App
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded
from accountManagement import anonymous
from id import *

def connector():
    try:
        # Try to connect to the database
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)
        
        # If the connection is successful, create a cursor and return it
        query = connection.cursor()
        print("\n~~~~~~~~~~~~\nConnection Established\n~~~~~~~~~~~~\n")
        return query
    
    except:
        print("Error: Unable to connect to the database:", e)

connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)
query = connection.cursor()

if anonymous():
    print("\n~~~Anonymous User.~~~\n")
    print("Current User: ",current_user)
else:
    user = current_user.username
    print("Logged in as: ",user)

def show_balance():
    print("Current User: ",current_user.username)

    query.execute("SELECT Balance FROM Bank WHERE Username = %s", (current_user.username,))
    bal = query.fetchone()[0]
    print("Current Balance on %s is %d." % (current_user.username, bal))
    return bal

# def first_timer(cursor):
#     query = connector()
#     query.execute("SELECT Username FROM Bank WHERE Username = %s", (user,))

#     if query.fetchone() == None:
#         print("\n",user," is a first timer.\n")
#         cursor.execute("INSERT INTO Bank (Username, Balance) VALUES (%s, %s)", (user, 0.0))

# def deposit(amount):
#     # Checks if the user has a pending application.
#     balance += amount

#     # Updates the user's balance in the database.
#     query.execute("UPDATE Bank SET Balance = %d WHERE Username = %s", (balance, user))
#     return balance

# def withdraw(amount):
#     query = connector()

#     if amount > self.balance:
#         return "Error: Insufficient funds."
#     else:
#         try:
#             # Remove Money from the User's Balance
#             self.balance -= amount
        
#             #Update the Database with the current Balance
#             self.curs.execute("UPDATE Bank SET Balance = %d WHERE Username = %s", (self.balance, self.user))
#             return self.balance
#         except:
#             return "Error: Unable to connect to the database."
    
# def send(amount, receiver):
#     query = connector()
#     if amount > self.balance:
#         return "Error: Insufficient funds."
#     else:
#         try:
#             # Remove Money from the User's Balance and Update Database
#             self.balance -= amount
#             self.curs.execute("UPDATE Bank SET Balance = %d WHERE Username = %s", (self.balance, self.user))
        
#             # Add Money to the Receiver's Balance and Update Database
#             self.curs.execute("SELECT Balance FROM Bank WHERE Username = %s", (receiver,))
#             receiver_balance = self.curs.fetchone()[0]
#             receiver_balance += amount
    
#             self.curs.execute("UPDATE Bank SET Balance = %d WHERE Username = %s", (receiver_balance, receiver))
#         except:
#             return "Error: Unable to connect to the database."

