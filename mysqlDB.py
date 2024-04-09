import mysql.connector


# Database connection

SeverName = "159.8.122.152"
UserName = "datad02n_userpneu"
Password = "6A3AKayzuukD&j9eusK^"
DBName = "datad02n_data"

mydb = mysql.connector.connect(
    host=SeverName,
    user=UserName,
    password=Password,
    database=DBName
)

# Temporary Cart functions
# REMOVE FROM TEMP CART
def removeFrom_tmpCart(name):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM tempCart WHERE name = %s", (name,))
        mydb.commit()
        cursor.close()
        return "Data removed"
    except mysql.connector.Error as error:
        return None

# ADD TO TEMP CART
def addTo_tmpCart(data, userid):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM tempCart WHERE userid = %s AND ref = %s", (userid, data['ref']))
        if cursor.fetchone():
            cursor.execute("UPDATE tempCart SET qte = qte + 1 WHERE userid = %s AND ref = %s", (userid, data['ref']))
        else:
            cursor.execute("INSERT INTO tempCart (name, qte, price, ref, userid) VALUES (%s, %s, %s, %s, %s)", (data['name'], data['qte'], data['price'], data['ref'], userid))
            
        mydb.commit()
        cursor.close()
        return 'success'
    except mysql.connector.Error as error:
        return None

# SELECT TEMP CART
def select_tmpCart(userid):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM tempCart WHERE userid = %s", (userid,))
        data = cursor.fetchall()
        cursor.close()

        products = []

        for product in data:
            products.append({
                'name': product[0],
                'price': round(product[2],2),
                'ref': product[4],
                'qte': product[1]
            })
        return products
    except mysql.connector.Error as error:
        return None

# CLEAN TEMP CART  
def clean_tmpCart(userid):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM tempCart WHERE userid = %s", (userid,))
        mydb.commit()
        cursor.close()
        return "Data removed"
    except mysql.connector.Error as error:
        return None