from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error

def get_connection():
    # Returns a database connection
    return mysql.connector.connect(
        host="159.8.122.152",
        user="datad02n_userpneu",
        password="6A3AKayzuukD&j9eusK^",
        database="datad02n_data"
    )

@contextmanager
def managed_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()  # Ensure transaction is committed here.
    finally:
        cursor.close()
        conn.close()

def get_TOTAL(userid):
    query = "SELECT SUM(price * qte) FROM tempCart WHERE userid = %s"
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, (userid,))
            data = cursor.fetchone()
        
        if data and data[0] is not None:
            total = f"{data[0]:,.2f}"
            return total
        return "0.00"
    except Error as error:
        print(f"Error: {error}")
        return "0.00"


def removeFrom_tmpCart(name):
    try:
        with managed_cursor() as cursor:
            cursor.execute("DELETE FROM tempCart WHERE name = %s", (name,))
        return "Data removed"
    except Error as error:
        print(f"Error: {error}")
        return None


# Add to tempCart

def addTo_tmpCart(data, userid):
    try:
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT 1 FROM tempCart WHERE userid = %s AND ref = %s", (userid, data['ref']))
        
        if cursor.fetchone():
            cursor.execute("UPDATE tempCart SET qte = qte + %s WHERE userid = %s AND ref = %s", (data['qte'], userid, data['ref']))
        else:
            cursor.execute("INSERT INTO tempCart (name, qte, price, ref, userid, img) VALUES (%s, %s, %s, %s, %s, %s)", (data['name'], data['qte'], data['price'], data['ref'], userid, data['img']))
        
        mydb.commit()
        cursor.close()
        mydb.close()
        return 'success'
    except mysql.connector.Error as error:
        print(error)
        return None


def select_tmpCart(userid):
    if not userid:
        return None

    query = "SELECT name, qte, price, ref, famille, img FROM tempCart WHERE userid = %s"
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, (userid,))
            data = cursor.fetchall()

        products = []
        for product in data:
            products.append({
                'name': product[0],
                'qte': product[1],
                'price': round(product[2], 2),
                'ref': product[3],
                'famille': product[4],
                'img': product[5]
            })

        return products
    except Error as error:
        print(f"Error: {error}")
        return None

# Clean tempCart
def clean_tmpCart(userid):
    query = "DELETE FROM tempCart WHERE userid = %s"
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, (userid,))
        return "Data removed"
    except Error as error:
        print(f"Error: {error}")
        return None



# devis_draft
def last_dev():
    query = "SELECT MAX(devis) FROM devis_draft"
    try:
        with managed_cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchone()
        
        if data[0] is None:
            return "000000"  # Return default if no records exist
        
        last = int(data[0]) + 1  # Increment the last devis number
        return "{:06d}".format(last)  # Format as a six-digit number, padded with zeros
    except Error as error:
        print(f"Error: {error}")
        return "000000"



def add_devis_draft(client, date, ref, devis, userid, client_name):
    query = """
    INSERT INTO devis_draft (client, date, ref, devis, userid, client_name)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (client, date, ref, devis, userid, client_name)
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, values)
        print("Data added in devis_draft")
        return "Data added"
    except Error as error:
        print(f"Error: {error}")
        return None
    
# def add_devis_draft_details(client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid):
#     try:
#         with managed_cursor() as cursor:
#             query = """
#             INSERT INTO devis_draft_details (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             values = (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid)
#             cursor.execute(query, values)
#             print("Data added in devis_draft_details")
#             return "Data added"
#     except Error as error:
#         print(f"Error: {error}")
#         return None


def get_drafts(id="all", devis="all"):
    query = """
    SELECT 
        devis_draft.`id`,
        devis_draft.`client`,
        devis_draft.`client_name`,
        devis_draft.`date`,
        devis_draft.`ref`,
        devis_draft.`devis`,
        devis_draft.`userid`,
        devis_draft.`draft_confirm`,
        SUM(devis_draft_details.total) as total
    FROM devis_draft 
    INNER JOIN devis_draft_details 
    ON devis_draft_details.devis = devis_draft.devis
    """
    params = ()

    if devis == "all" and id != "all":
        query += " WHERE devis_draft.userid = %s GROUP BY devis_draft.devis"
        params = (id,)
    elif devis != "all" and id != "all":
        query += " WHERE devis_draft.userid = %s AND devis_draft.devis = %s GROUP BY devis_draft.devis"
        params = (id, devis)
    elif devis == "all" and id == "all":
        query += " GROUP BY devis_draft.devis"
    else: # If id is "all" but devis is not "all"
        query += " WHERE devis_draft.devis = %s GROUP BY devis_draft.devis"
        params = (devis,)

    try:
        with managed_cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchall()

        drafts = [
            {
                "id": i[0],
                "client": i[1],
                "client_name": i[2],
                "date": i[3],
                "ref": i[4],
                "devis": i[5],
                "userid": i[6],
                "status": i[7],
                "total": float(i[8]) if i[8] is not None else 0.00
            } for i in data
        ]
        return drafts
    except Error as error:
        print(f"Error: {error}")
        return None


def get_draft_devis(devis):
    query = """
    SELECT 
        devis_draft.`id`,
        devis_draft.`client`,
        devis_draft.`client_name`,
        devis_draft.`date`,
        devis_draft.`ref`,
        devis_draft.`devis`,
        devis_draft.`userid`,
        devis_draft.`draft_confirm`,
        SUM(devis_draft_details.total) as total
    FROM devis_draft
    INNER JOIN devis_draft_details ON devis_draft_details.devis = devis_draft.devis
    WHERE devis_draft.devis = %s
    GROUP BY devis_draft.devis
    """
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, (devis,))
            data = cursor.fetchall()

        drafts = [
            {
                "id": i[0],
                "client": i[1],
                "client_name": i[2],
                "date": i[3],
                "ref": i[4],
                "devis": i[5],
                "userid": i[6],
                "status": i[7],
                "total": float(i[8]) if i[8] is not None else 0.00
            } for i in data
        ]
        return drafts
    except Error as error:
        print(f"Error: {error}")
        return None


def check_auth(userid, devis):
    query = "SELECT 1 FROM devis_draft WHERE userid = %s AND devis = %s"
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, (userid, devis))
            data = cursor.fetchone()
        return bool(data)  # Returns True if data is found, False otherwise
    except Error as error:
        print(f"Error: {error}")
        return None

def get_drafts_details(devis):
    query = """
    SELECT 
        id, client, devis, ar_ref, productDescription, quantity,
        price, dateF, ref, date, total, userid
    FROM devis_draft_details 
    WHERE devis = %s
    """
    try:
        with managed_cursor() as cursor:
            cursor.execute(query, (devis,))
            data = cursor.fetchall()

        drafts_details = [
            {
                "id": row[0],
                "client": row[1],
                "devis": row[2],
                "ar_ref": row[3],
                "productDescription": row[4],
                "quantity": row[5],
                "price": row[6],
                "dateF": row[7],
                "ref": row[8],
                "date": row[9],
                "total": row[10],
                "userid": row[11]
            } for row in data
        ]
        return drafts_details
    except Error as error:
        print(f"Error: {error}")
        return None

    
def clean_drafts(devis):
    queries = [
        "DELETE FROM devis_draft WHERE devis = %s",
        "DELETE FROM devis_draft_details WHERE devis = %s"
    ]
    try:
        with managed_cursor() as cursor:
            for query in queries:
                cursor.execute(query, (devis,))
        return "Data removed"
    except Error as error:
        print(f"Error: {error}")
        return None


def add_devis_draft_details_batch(details):
    query = """
    INSERT INTO devis_draft_details (client, ar_ref, productDescription, quantity, price, dateF, ref, date, total, devis, userid)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = []
    for detail in details:
        values.append((detail['client'], detail['ar_ref'], detail['productDescription'], detail['quantity'],
                       detail['price'], detail['dateF'], detail['ref'], detail['date'], detail['total'],
                       detail['devis'], detail['userid']))

    try:
        with managed_cursor() as cursor:
            cursor.executemany(query, values)
            print("Data added in devis_draft_details")
            return "Data added"
    except Error as error:
        print(f"Error: {error}")
        return None

