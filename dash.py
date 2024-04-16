import pyodbc,datetime
from flask import jsonify
import time


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.118.25.162,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')

def get_ca_client_co_no_2024(co_no, role):
    try:
        cursor = conn.cursor()
        
        if role == 'Administrateur':
            cursor.execute("SELECT TOP 10 client,sum(dl_montantttc) as Dl_MontantTTC,CO_No,CT_Num FROM ca_client_co_no_2024 group by client,CO_No,CT_Num ORDER BY Dl_MontantTTC DESC")
        else:
            cursor.execute("SELECT TOP 10 client,sum(dl_montantttc) as Dl_MontantTTC,CO_No,CT_Num FROM ca_client_co_no_2024 WHERE Co_no = ? group by client,CO_No,CT_Num ORDER BY Dl_MontantTTC DESC", co_no)
        rows = cursor.fetchall()
        list = []
        for row in rows:
            list.append({'client': row[0], 'dl_montantttc': f"{row[1]:,.2f}", 'co_no': row[2], 'ct_num': row[3]})
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
        list = []
        for row in rows:
            list.append({'ar_design': row[0], 'dl_montantttc': f"{row[1]:,.2f}", 'co_no': row[2], 'dl_qte': int(row[3]), 'ar_ref': row[4], 'famille': row[5]})
        print(list)
        return list
    except Exception as e:
        return None