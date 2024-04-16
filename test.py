import mysql.connector

import pyodbc,datetime
from flask import jsonify

# Database connection
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.28.6,1433;DATABASE=UNIO 2020;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')



# Database connection details
SeverName = "159.8.122.152"
UserName = "datad02n_userpneu"
Password = "6A3AKayzuukD&j9eusK^"
DBName = "datad02n_data"

# Get a new database connection
def get_connection():
    return mysql.connector.connect(
        host=SeverName,
        user=UserName,
        password=Password,
        database=DBName
    )



# CREATE TABLE devis_draft (
#     devis_draft_number INT AUTO_INCREMENT PRIMARY KEY,
#     client VARCHAR(255) NOT NULL,
#     date DATE NOT NULL,
#     ref VARCHAR(255),
#     userid INT NOT NULL,
# );

def create_devis_draft():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE devis_draft (devis_draft_number INT AUTO_INCREMENT PRIMARY KEY, client VARCHAR(255) NOT NULL, date DATE NOT NULL, ref VARCHAR(255), userid INT NOT NULL)")
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Table created"
    except mysql.connector.Error as error:
        print(error)
        return None
    
def remove_devis_draft():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("DROP TABLE devis_draft")
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Table removed"
    except mysql.connector.Error as error:
        print(error)
        return None
    
def add_devis_draft(client, date, ref):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO devis_draft (client, date, ref) VALUES (%s, %s, %s)", (client, date, ref))
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Data added"
    except mysql.connector.Error as error:
        print(error)
        return None
    
# add_devis_draft("client", datetime.datetime.now(), "ref")

def get_devis_draft():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM devis_draft")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return data
    except mysql.connector.Error as error:
        print(error)
        return None

# print(get_devis_draft())



# CREATE TABLE devis_draft_details (
#     devis_draft_number INT NOT NULL,
#     client VARCHAR(255) NOT NULL,
#     devis VARCHAR(255),
#     ar_ref VARCHAR(255),
#     productDescription TEXT,
#     quantity INT NOT NULL,
#     price DECIMAL(10, 2) NOT NULL,
#     dateF DATE,
#     ref VARCHAR(255),
#     date DATE NOT NULL,
#     total DECIMAL(10, 2) NOT NULL
#     userid INT NOT NULL,
# );

def create_devis_draft_details():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE devis_draft_details (devis_draft_number INT NOT NULL, client VARCHAR(255) NOT NULL, devis VARCHAR(255), ar_ref VARCHAR(255), productDescription TEXT, quantity INT NOT NULL, price DECIMAL(10, 2) NOT NULL, dateF DATE, ref VARCHAR(255), date DATE NOT NULL, total DECIMAL(10, 2) NOT NULL, userid INT NOT NULL)")
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Table created"
    except mysql.connector.Error as error:
        print(error)
        return None
    
def remove_devis_draft_details():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("DROP TABLE devis_draft_details")
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Table removed"
    except mysql.connector.Error as error:
        print(error)
        return None
    
def add_devis_draft_details(client, devis, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis_draft_number):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO devis_draft_details (client, devis, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis_draft_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (client, devis, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis_draft_number))
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Data added"
    except mysql.connector.Error as error:
        print(error)
        return None
    

remove_devis_draft()
create_devis_draft()