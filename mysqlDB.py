import mysql.connector
import time

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

# Get total from tempCart
def get_TOTAL(userid):
    try:
        mydb = get_connection()
        time.sleep(0.5)
        cursor = mydb.cursor()
        cursor.execute("SELECT SUM(price * qte) FROM tempCart WHERE userid = %s", (userid,))
        data = cursor.fetchone()
        cursor.close()
        mydb.close()
        
        if data[0] is None:
            return "0.00"
        
        data = f"{data[0]:,.2f}"
        return data
    except mysql.connector.Error as error:
        print(error)
        return "0.00"

# Remove from tempCart
def removeFrom_tmpCart(name):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM tempCart WHERE name = %s", (name,))
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Data removed"
    except mysql.connector.Error as error:
        print(error)
        return None

# Add to tempCart
def addTo_tmpCart(data, userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM tempCart WHERE userid = %s AND ref = %s", (userid, data['ref']))
        
        if cursor.fetchone():
            cursor.execute("UPDATE tempCart SET qte = qte + %s WHERE userid = %s AND ref = %s", (data['qte'], userid, data['ref']))
        else:
            cursor.execute("INSERT INTO tempCart (name, qte, price, ref, userid) VALUES (%s, %s, %s, %s, %s)", (data['name'], data['qte'], data['price'], data['ref'], userid))
        
        mydb.commit()
        cursor.close()
        mydb.close()
        return 'success'
    except mysql.connector.Error as error:
        print(error)
        return None

# Select from tempCart
def select_tmpCart(userid):
    try:
        mydb = get_connection()
        if not userid:
            mydb.close()
            return None

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM tempCart WHERE userid = %s", (userid,))
        data = cursor.fetchall()
        cursor.close()
        mydb.close()

        products = []

        for product in data:
            products.append({
                'name': product[0],
                'price': round(product[2], 2),
                'ref': product[4],
                'qte': product[1]
            })

        return products
    except mysql.connector.Error as error:
        print(error)
        return None

# Clean tempCart
def clean_tmpCart(userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM tempCart WHERE userid = %s", (userid,))
        mydb.commit()
        cursor.close()
        mydb.close()
        return "Data removed"
    except mysql.connector.Error as error:
        print(error)
        return None



# devis_draft
def last_dev():
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT MAX(devis) FROM devis_draft")
        data = cursor.fetchone()
        cursor.close()
        mydb.close()
        
        if data[0] is None:
            return "000000"
        
        last = int(data[0])
        last += 1
        data = "{:06d}".format(last)
        return data
    except mysql.connector.Error as error:
        print(error)
        return "000000"
    

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

