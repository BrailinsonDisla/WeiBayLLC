# Imports the MySQL APT for DB connections.
from mysql.connector import connect

# Defines the default database admin username.
default_admin = 'db-admin'

# Defines the default host IP.
default_host = '34.95.20.62'

# Defines the default database name.
default_db = 'WeiBayLLC'

# Defines the default password for the default admin.
default_pswd = 'ABCMT!322'

# Creates a connection to the database for the WieBayLLC website application.
try:
    # Connects to the WeiBay LLC main database.
    dbConnection = connect(user=default_admin, host=default_host, database=default_db, password=default_pswd)

    # Creates a cursor to execute database queries.
    dbCursor = dbConnection.cursor()
except:
    # Informs the admin that the connection attempt failed.
    print('FAILED TO CONNECT TO THE DATABASE')
