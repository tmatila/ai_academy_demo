import os
import pyodbc
import pandas as pd
import uuid

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

cursor = cnxn.cursor()

# PROMPT for copilot
# This is my csv-file of tennis rackets. I would like to create a 
# table in my database that has same columns as this csv-file. 
# Also, create me python script to populate the tables using values 
# from this csv-file.  

# Notes after ChatGPT
# - Wanted to ID as an extra (which needs "import uuid") 
# - Fixed formats for some items e.g. to INT

# ==============================================
# Create table (See create_table.py)
# ==============================================

# cursor.execute("""
#     CREATE TABLE TennisRackets (
#         ID UNIQUEIDENTIFIER PRIMARY KEY,       
#         Mold VARCHAR(255),
#         HeadSize INT,
#         Pattern VARCHAR(50),
#         ThroatMains INT,
#         Beam VARCHAR(50),
#         Manufacturer VARCHAR(255),
#         Name VARCHAR(255),
#         Owned_by_Tommi INT,
#         Tommi_wants_this INT,
#         Year INT,
#         DescriptionTommi TEXT,
#         Description TEXT,
#         Layup VARCHAR(255),
#         Made_in_Austria INT,
#         Designed_in_Austria INT,
#         Info_from VARCHAR(255),
#         Image VARCHAR(255)
#     )
# """)
# cnxn.commit()
# ==============================================
# Populate table (See create_table.py)
# ==============================================
# Load the CSV data
df = pd.read_csv('tennis/doc/FischerList_cleaned2.csv')
# Replace NaN values with None (which pyodbc will convert to SQL NULL)
df = df.where(pd.notnull(df), None)


# Insert data into the database
for index, row in df.iterrows():
    insert_stmt = """INSERT INTO TennisRackets (ID, Mold, HeadSize, Pattern, ThroatMains, Beam, Manufacturer, 
                     Name, Owned_by_Tommi, Tommi_wants_this, Year, DescriptionTommi, Description, Layup, 
                     Made_in_Austria, Designed_in_Austria, Info_from, Image) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    print(index)
    print("-----------")
    print(row)
    cursor.execute(insert_stmt, [str(uuid.uuid4()), row['Mold'], row['Head'], row['Pattern'], row['Throat'], 
                                 row['Beam'], row['Manufacturer'], row['Name'], row['Owned by Tommi'], 
                                 row['Tommi wants this'], row['Year'], row['DescriptionTommi'], 
                                 row['Description'], row['Layup'], row['Made in Austria'], 
                                 row['Designed in Austria'], row['Info from'], row['Image']])

cnxn.commit()
cnxn.close()


