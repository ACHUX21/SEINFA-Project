import pyodbc,datetime
from flask import jsonify
import time


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.56.212,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;MARS_Connection=Yes;MultipleActiveResultSets=True;')

def get_ca_client_co_no_2024(co_no, role):
    try:
        cursor = conn.cursor()
        
        if role == 'Administrateur':
            cursor.execute("SELECT TOP 10 client,sum(Dl_MontantTTC_2024) as Dl_MontantTTC_2024,sum(Dl_MontantTTC_2023) as Dl_MontantTTC_2023,CO_No,CT_Num FROM ca_client_co_no_2024 group by client,CO_No,CT_Num ORDER BY Dl_MontantTTC_2024 DESC")
        else:
            cursor.execute("SELECT TOP 10 client,sum(Dl_MontantTTC_2024) as Dl_MontantTTC_2024,sum(Dl_MontantTTC_2023) as Dl_MontantTTC_2023,CO_No,CT_Num FROM ca_client_co_no_2024 WHERE Co_no = ? group by client,CO_No,CT_Num ORDER BY Dl_MontantTTC_2024 DESC", co_no)
        rows = cursor.fetchall()

        cursor.close()
        list = []
        for row in rows:
            list.append({'client': row[0], 'Dl_MontantTTC_2024': f"{row[1]:,.2f}", 'Dl_MontantTTC_2023': f"{row[2]:,.2f}", 'co_no': row[3], 'ct_num': row[4]})
        # print(list)
        return list
    except Exception as e:
        return None




def get_ca_products_co_no_2024(co_no, role):
    try:
        cursor = conn.cursor()
        if role == 'Administrateur':
            cursor.execute("SELECT TOP 10 AR_Design,sum(dl_montantttc) as Dl_MontantTTC,CO_No,sum(dl_qte) as dl_qte,ar_ref,famille FROM ca_products_co_no_2024 group by AR_Design,CO_No,ar_ref,famille ORDER BY Dl_MontantTTC DESC")
        else:
            cursor.execute("SELECT TOP 10 AR_Design,sum(dl_montantttc) as Dl_MontantTTC,CO_No,sum(dl_qte) as dl_qte,ar_ref,famille FROM ca_products_co_no_2024 WHERE Co_no = ? group by AR_Design,CO_No,ar_ref,famille ORDER BY Dl_MontantTTC DESC" , co_no)
        rows = cursor.fetchall()
        cursor.close()
        list = []
        for row in rows:
            list.append({'ar_design': row[0], 'dl_montantttc': f"{row[1]:,.2f}", 'co_no': row[2], 'dl_qte': int(row[3]), 'ar_ref': row[4], 'famille': row[5]})
        # print(list)
        return list
    except Exception as e:
        return None
    
def get_all_client_by_co_no(co_no,role):
    try:
        cursor = conn.cursor()
        if role == 'Administrateur':
            cursor.execute("select count(distinct ct_num) as client from ca_client_co_no_2024")
        else:
            cursor.execute("select count(distinct ct_num) as client from ca_client_co_no_2024 where co_no=?", co_no)
        rows = cursor.fetchall()
        cursor.close()
        return rows[0][0]
    except Exception as e:
        return None
    
def get_ca_by_co_no(co_no,role):
    try:
        cursor = conn.cursor()
        if role == 'Administrateur':
            cursor.execute("SELECT sum(Dl_MontantTTC_2024) as Dl_MontantTTC_2024,sum(Dl_MontantTTC_2023) as Dl_MontantTTC_2023  FROM ca_client_co_no_2024")
        else:
            cursor.execute("SELECT sum(Dl_MontantTTC_2024) as Dl_MontantTTC_2024,sum(Dl_MontantTTC_2023) as Dl_MontantTTC_2023 FROM ca_client_co_no_2024 WHERE Co_no = ?", co_no)
        rows = cursor.fetchall()
        cursor.close()
        return {'Dl_MontantTTC_2024': f"{rows[0][0]:,.2f}", 'Dl_MontantTTC_2023': f"{rows[0][1]:,.2f}"}
    except Exception as e:
        return None
    
def get_all_ca(co_no,role):
    try:
        cursor = conn.cursor()
        if role == 'Administrateur':
            cursor.execute("SELECT sum(Dl_MontantTTC) as Dl_MontantTTC FROM ca_client_co_no_2024")
        else:
            cursor.execute("SELECT sum(Dl_MontantTTC) as Dl_MontantTTC FROM ca_client_co_no_2024 WHERE Co_no = ?", co_no)
        rows = cursor.fetchall()
        cursor.close()
        return f"{rows[0][0]:,.2f}"
    except Exception as e:
        return None
    
def get_products_en_promotions():
    try:
        cursor = conn.cursor()
        query = f"""
        SELECT promotion.*,product_data.image_picture FROM promotion left join product_data on promotion.ar_ref = product_data.ar_ref
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        products = []
        for row in data:
            product = {
                'name': row[1],
                'price': round(row[2], 2),
                'category': row[3],
                'ref': row[0],
                'en_promotion': row[4],
                'prix_en_promotion': round(row[5], 2),
                'img': row[6]
            }
            products.append(product)

        return products
    except Exception as e:
        return None
    
def encours_commercial_client(co_no,role):
    try:
        # select DO_Piece, CO_No, DO_TotalTTC, montantàregle
        # from facture_asz_no_regler;
        cursor = conn.cursor()
        if role == 'Administrateur':
            cursor.execute("SELECT sum(DO_TotalTTC) FROM facture_asz_no_regler")
        else:
            cursor.execute("SELECT sum(DO_TotalTTC) FROM facture_asz_no_regler WHERE CO_No = ?", co_no)
        rows = cursor.fetchall()
        cursor.close()
        return f"{rows[0][0]:,.2f}"
    except Exception as e:
        return None