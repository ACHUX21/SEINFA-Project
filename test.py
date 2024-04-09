import mysql.connector

import pyodbc,datetime
from flask import jsonify

# Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.28.6,1433;DATABASE=UNIO 2020;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')


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

# CREATE TABLE tempCart(
#     name varchar(50) NULL,
#     qte int NULL,
#     price float NULL,
#     userid int NULL
#     ref varchar(50) NULL
# )

def create_tmpCart():
    cursor = mydb.cursor()
    cursor.execute("CREATE TABLE tempCart(name varchar(50) NULL, qte int NULL, price float NULL, userid int NULL, ref varchar(50) NULL)")
    mydb.commit()
    cursor.close()
    print("Table tempCart created")

def remove_tmpCart():
    cursor = mydb.cursor()
    cursor.execute("DROP TABLE tempCart")
    mydb.commit()
    cursor.close()
    print("Table tempCart removed")

def insert_tmpCart(name, qte, price, userid):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO tempCart (name, qte, price, userid) VALUES (%s, %s, %s, %s)", (name, qte, price, userid))
    mydb.commit()
    cursor.close()
    return "Data inserted"


# remove_tmpCart()
# create_tmpCart()

def Get_CT_NUM(CT_INTITULE):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CT_NUM FROM F_COMPTET WHERE CT_INTITULE = ?", CT_INTITULE)
        data = cursor.fetchone()
        cursor.close()
        return data[0]
    except Exception as e:
        return None
    

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
                'price': product[2],
                'ref': product[4],
                'qte': product[1]
            })
        return products
    except mysql.connector.Error as error:
        return None

def fer():
    userid = 1
    for panier in select_tmpCart(userid):
        print(panier)





def get_devis_by_id(devis_id):
    cursor = conn.cursor()
    query = """
    select F_COMPTET.CT_Num,F_COMPTET.CT_Intitule,F_COMPTET.CT_Telephone,F_COMPTET.CT_Adresse,F_DOCLIGNE.DO_Piece,F_DOCLIGNE.DO_Ref,F_DOCLIGNE.DO_Date ,F_DOCLIGNE.AR_Ref,F_DOCLIGNE.DL_Design,F_DOCLIGNE.DL_Qte,F_DOCLIGNE.DL_PUTTC,F_DOCLIGNE.DL_MontantHT,F_DOCLIGNE.DL_MontantTTC,F_DOCENTETE.DO_Statut,F_DOCENTETE.DO_TotalHT,F_DOCENTETE.DO_TotalTTC
    from F_DOCLIGNE inner join F_COMPTET on F_COMPTET.CT_Num = F_DOCLIGNE.CT_Num inner join F_DOCENTETE on F_DOCENTETE.do_piece = F_DOCLIGNE.DO_Piece where F_DOCLIGNE.DO_Type = 0 and F_DOCLIGNE.DO_Piece = ?
    """
    cursor.execute(query, devis_id)
    devis = cursor.fetchall()
    cursor.close()
    details = []
    products = []
    for row in devis:
        product = {
            'AR_Ref': row[7],
            'DL_Design': row[8],
            'DL_Qte': float(row[9]),
            'DL_PUTTC': float(row[10]),
            'DL_MontantHT': float(row[11]),
            'DL_MontantTTC': float(row[12])
        }
        products.append(product)

    for row in devis:
        devis = {
            'CT_Num': row[0],
            'CT_Intitule': row[1],
            'CT_Telephone': row[2],
            'CT_Adresse': row[3],
            'DO_Piece': row[4],
            'DO_Ref': row[5],
            'DO_Date': datetime.datetime.strftime(row[6], '%Y-%m-%d'),
            'DO_Statut': int(row[13]),
            'DO_TotalHT': float(row[14]),
            'DO_TotalTTC': float(row[15]),
        }
        details.append(devis)
        break
    
    details[0]['products'] = products

    return details



