import os
import pyodbc

# Assuming other connection details are not sensitive or are okay to hard code
server = 'localhost,1495'
database = 'AI2024'
username = 'sa'
password = os.environ.get('SQL_SERVER_PASSWORD')  # Retrieve password from environment variable

# Connection string using environment variable for password
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                      ';DATABASE=' + database +
                      ';UID=' + username +
                      ';PWD=' + password)

# Your database operations here

cnxn.close()
