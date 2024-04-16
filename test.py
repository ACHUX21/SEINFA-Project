import mysql.connector

import pyodbc,datetime
from flask import jsonify

# Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.118.25.162,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')



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

def create_devis_draft():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE devis_draft (id INT AUTO_INCREMENT PRIMARY KEY, client VARCHAR(255), date VARCHAR(255), ref VARCHAR(255), devis VARCHAR(255), userid VARCHAR(255))")
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Table devis_draft created")
        return "Table created"
    except mysql.connector.Error as error:
        print(error)
        return None
    
def create_devis_draft_details():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE devis_draft_details (id INT AUTO_INCREMENT PRIMARY KEY, client VARCHAR(255), devis VARCHAR(255), ar_ref VARCHAR(255), productDescription VARCHAR(255), quantity VARCHAR(255), price VARCHAR(255), dateF VARCHAR(255), ref VARCHAR(255), date VARCHAR(255), total VARCHAR(255), userid VARCHAR(255))")
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Table devis_draft_details created")
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
        print("Table devis_draft removed")
        return "Table removed"
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
        print("Table devis_draft_details removed")
        return "Table removed"
    except mysql.connector.Error as error:
        print(error)
        return None
    
# remove_devis_draft()
# remove_devis_draft_details()
# create_devis_draft()
# create_devis_draft_details()


def add_devis_draft(client, date, ref, devis ,userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO devis_draft (client, date, ref, devis, userid) VALUES (%s, %s, %s, %s, %s)", (client, date, ref, devis, userid))
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Data added in devis_draft")
        return "Data added"
    except mysql.connector.Error as error:
        print(error)
        return None
    

def add_devis_draft_details(client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO devis_draft_details (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid))
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Data added in devis_draft_details")
        return "Data added"
    except mysql.connector.Error as error:
        print(error)
        return None


# remove_devis_draft()
# remove_devis_draft_details()
# create_devis_draft()
# create_devis_draft_details()

# add_devis_draft("client", "date", "ref", "000000", "userid")
# add_devis_draft_details("client", "ar_ref", "productDescription", "quantity", "price", "dateF", "ref", "date", "total", "000000", "userid")

def select_devis_draft():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM devis_draft")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        for i in data:
            print(i)
        return data
    except mysql.connector.Error as error:
        print(error)
        return None
    
def select_devis_draft_details():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM devis_draft_details")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        for i in data:
            print(i)
        return data
    except mysql.connector.Error as error:
        print(error)
        return None
    
 

select_devis_draft()
select_devis_draft_details()


def add_devis_draft_details(client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO devis_draft_details (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid))
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Data added in devis_draft_details")
        return "Data added"
    except mysql.connector.Error as error:
        print(error)
        return None
    