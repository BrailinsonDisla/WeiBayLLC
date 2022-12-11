from mysql.connector import *
from flask_login import current_user
from accountManagement import anonymous
from DBConnection import *

class Banking:
    try:
        connection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)
        cursor = connection.cursor()
        print("\n~~~~~~~~~~~~\nConnection Established\n~~~~~~~~~~~~\n")
    except Exception as e:
        print("Error: Unable to connect to the database:", e)
        
    def __init__(self):
        if not anonymous():
            try:
                # Checks which user is login in.
                self.user = current_user.username
                self.id = current_user.user_id
                self.first_timer()
            
                #Query for the Username
                self.cursor.execute("SELECT * FROM BankAccounts WHERE Owner = %s", (self.user, ))
                
                # Gets Username and Balance from the database.
                self.balance = self.cursor.fetchone()[2]
            except:
                print("Error: Unable to connect to the database In __INIT__.\n")
        else:
            print("Anonymous User")  
            
    def first_timer(self):
        self.cursor.execute("SELECT Owner FROM BankAccounts WHERE Owner = %s", (self.user,))
        
        if self.cursor.fetchone() == None:
            print(self.user + " is a first timer.\n")
            query = "INSERT INTO BankAccounts (`Account Number`,Owner, `Account Balance`) VALUES (%s, %s, %s)"% (self.id,self.user, 0.0)
            print(query)
            self.cursor.execute(query)
    
    def deposit(self, amount):
        # Checks if the user has a pending application.
        self.balance += amount
        
        # Updates the user's balance in the database.
        self.cursor.execute("UPDATE BankAccounts SET `Account Balance` = %d WHERE Owner = %s", (self.balance, self.user))
        return self.balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            return "Error: Insufficient funds."
        else:
            try:
                # Remove Money from the User's Balance
                self.balance -= amount
                
                #Update the Database with the current Balance
                self.cursor.execute("UPDATE BankAccounts SET `Account Balance` = %d WHERE Owner = %s", (self.balance, self.user))
                return self.balance
            except:
                return "Error: Unable to connect to the database."
            
    def send(self, amount, receiver):
        if amount > self.balance:
            return "Error: Insufficient funds."
        else:
            try:
                # Remove Money from the User's Balance and Update Database
                self.balance -= amount
                self.cursor.execute("UPDATE BankAccounts SET `Account Balance` = %d WHERE Owner = %s", (self.balance, self.user))
                
                # Add Money to the Receiver's Balance and Update Database
                self.cursor.execute("SELECT `Account Balance`FROM BankAccounts WHERE Owner = %s", (receiver,))
                receiver_balance = self.cursor.fetchone()[0]
                receiver_balance += amount
            
                self.cursor.execute("UPDATE BankAccounts SET `Account Balance` = %d WHERE Owner = %s", (receiver_balance, receiver))
            except:
                return "Error: Unable to connect to the database."
    
    def show_balance(self):
        self.cursor.execute("SELECT `Account Balance` FROM BankAccounts WHERE Owner = %s and `Account Number` = %s", (current_user.username,self.id))
        temp_balance = self.cursor.fetchone()
        print(temp_balance)
        # print("Show Balance: ", temp_balance)
        return temp_balance
