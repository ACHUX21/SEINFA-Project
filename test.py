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
    
 

# select_devis_draft()
# select_devis_draft_details()


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




def get_drafts(id):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT devis_draft.`id`,devis_draft.`client`,devis_draft.`client_name`,devis_draft.`date`,devis_draft.`ref`,devis_draft.`devis`,devis_draft.`userid`,devis_draft.`draft_confirm`,SUM(devis_draft_details.total) as total FROM devis_draft inner JOIN devis_draft_details on devis_draft_details.devis = devis_draft.devis WHERE devis_draft.userid = %s GROUP by devis_draft.devis", (id,))
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        draft = []
        for i in data:
            dra = {
                "id": i[0],
                "client": i[1],
                "client_name": i[2],
                "date": i[3],
                "ref": i[4],
                "devis": i[5],
                "userid": i[6],
                "draft_confirm": i[7],
                "total": i[8]
            }
            draft.append(dra)
        print(draft)
        return draft
    except mysql.connector.Error as error:
        print(error)
        return None
    
    
def get_draft_details(id, devis):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM devis_draft_details WHERE userid = %s AND devis = %s", (id, devis))
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        draft = []
        for i in data:
            dra = {
                "id": i[0],
                "client": i[1],
                "ar_ref": i[2],
                "productDescription": i[3],
                "quantity": i[4],
                "price": i[5],
                "dateF": i[6],
                "ref": i[7],
                "date": i[8],
                "total": i[9],
                "devis": i[10],
                "userid": i[11]
            }
            draft.append(dra)
        print(draft)
        return draft
    except mysql.connector.Error as error:
        print(error)
        return None

def get_available_devis(userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT devis FROM devis_draft WHERE userid = %s", (userid,))
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        devis = []
        for i in data:
            devis.append(i[0])
        print(devis)
        return devis
    except mysql.connector.Error as error:
        print(error)
        return None


# get_drafts('5')
# print("\n")
# get_draft_details('1', '000000')

# get_available_devis('5')



def check_auth(userid, devis):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM devis_draft WHERE userid = %s AND devis = %s", (userid, devis))
        data = cursor.fetchone()
        cursor.close()
        mydb.close()
        print(data)
        if data:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print(error)
        return None


# check_auth('5', '000000')


def get_drafts_details(devis):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM devis_draft_details WHERE devis = %s", (devis,))
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        draft = []
        for i in data:
            dra = {
                "id": i[0],
                "client": i[1],
                "devis": i[2],
                "ar_ref": i[3],
                "productDescription": i[4],
                "quantity": i[5],
                "price": i[6],
                "dateF": i[7],
                "ref": i[8],
                "date": i[9], 
                "total": i[10],
                "userid": i[11]
            }
            draft.append(dra)
        print(draft)
        return draft
    except mysql.connector.Error as error:
        print(error)
        return None
    
get_drafts_details('000000')