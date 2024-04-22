import pyodbc,datetime
from flask import jsonify
import hashlib

def get_cursor():
    return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.56.212,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;MARS_Connection=Yes;MultipleActiveResultSets=True;').cursor()

def fetch_first(query, params=None):
    try:
        with get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_all(query, params=None):
    try:
        with get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def execute_query(query, params):
    try:
        with get_cursor() as cursor:
            cursor.execute(query, params)
            cursor.commit()
            print("Data inserted successfully")
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def last_dev_mssql():
    query = "SELECT DO_PIECE from F_DOCENTETE where DO_Type = 0 ORDER BY DO_PIECE DESC"
    devis = fetch_first(query)
    if devis:
        last_devis = devis[0]
        prefix = last_devis[:2]
        current_number = last_devis[2:]
        number = str(int(current_number) + 1).zfill(len(current_number))
        return prefix + number
    return None  # Handle the case when no record is found

def last_DR_No():
    query = "SELECT DR_No from F_DOCREGL ORDER BY DR_No DESC"
    devis = fetch_first(query)
    if devis:
        return int(devis[0]) + 1
    return None  # Handle the case when no record is found

def Get_CT_NUM(CT_INTITULE):
    query = "SELECT CT_NUM FROM F_COMPTET WHERE CT_INTITULE = ?"
    data = fetch_first(query, (CT_INTITULE,))
    if data:
        return data[0]
    return None

def fetch_products(num=4000, cat=None):
    if not isinstance(num, int):
        raise ValueError('num must be an integer')

    # Prepare the query depending on whether a category is specified
    if cat:
        query = f"SELECT TOP {num} article_table.*, " \
                f"ASZPROD.dbo.product_data.image_picture " \
                f"FROM article_table " \
                f"LEFT JOIN ASZPROD.dbo.product_data " \
                f"ON article_table.AR_Ref = ASZPROD.dbo.product_data.ar_ref " \
                f"WHERE article_table.categorie = ?"
                
        params = (cat,)
    else:
        query = f"SELECT TOP {num} article_table.*, " \
                f"ASZPROD.dbo.product_data.image_picture " \
                f"FROM article_table " \
                f"LEFT JOIN ASZPROD.dbo.product_data " \
                f"ON article_table.AR_Ref = ASZPROD.dbo.product_data.ar_ref " \
                f"ORDER BY AS_QteSto DESC"
        params = ()


    try:
        with get_cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred fetching products: {e}")
        return []  # Return an empty list in case of error

    # Process the fetched data
    products = []
    for row in data:
        # Assuming the positions of fields are consistent as per the select statement
        product = {
            'name': row[1],
            'price': round(row[2], 2),
            'qte': int(row[3]) if row[3] else 0,
            'category': row[4],
            'ref': row[0],
            'prix_achat': round(row[8],2),
            'img': row[9]
        }
        products.append(product)

    return products



def get_product_by_ref(ref):
    query = "SELECT article_table.*, ASZPROD.dbo.product_data.image_picture FROM article_table LEFT JOIN ASZPROD.dbo.product_data ON article_table.AR_Ref = ASZPROD.dbo.product_data.ar_ref WHERE article_table.AR_Ref = ?"
    data = fetch_first(query, (ref,))
    if data:
        product = {
            'name': data[1],
            'price': round(data[2], 2),
            'qte': int(data[3]) if data[3] else 0,
            'category': data[4],
            'ref': data[0],
            'prix_achat': round(data[8],2),
            'img': data[9]
        }
        return product
    return None
# Use fetch_all in the get_categories function
def get_categories():
    query = "SELECT categorie FROM article_table GROUP BY categorie ORDER BY SUM(AS_QteSto) DESC"
    data = fetch_all(query)
    categories = [row[0] for row in data] if data else []
    return categories

def get_all_devis(offset=0, limit=200000):
    query = """
    SELECT do_piece, FORMAT(do_date, 'yyyy-MM-dd') as short_date, ct_intitule, do_ref, do_totalht, do_totalttc, do_statut
    FROM f_docentete
    INNER JOIN f_comptet ON f_comptet.ct_num = f_docentete.do_tiers
    WHERE do_type = 0
    ORDER BY do_date DESC
    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    params = (offset, limit)
    data = fetch_all(query, params)
    rounded_devis = []
    for row in data:
        devis = {
            'do_piece': row[0],
            'do_date': row[1],
            'ct_intitule': row[2],
            'do_ref': row[3],
            'do_totalht': f'{row[4]:,.2f}'.replace(',', ' '),
            'do_totalttc': f'{row[5]:,.2f}'.replace(',', ' '),
            'do_statut': row[6]
        }
        rounded_devis.append(devis)
    return rounded_devis

def get_all_devis_by_co_no(co_no, offset=0, limit=200000):
    query = """
    SELECT do_piece, FORMAT(do_date, 'yyyy-MM-dd') as short_date, ct_intitule, do_ref, do_totalht, do_totalttc, do_statut
    FROM f_docentete
    INNER JOIN f_comptet ON f_comptet.ct_num = f_docentete.do_tiers
    WHERE do_type = 0 AND f_docentete.co_no = ?
    ORDER BY do_date DESC
    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    params = (co_no, offset, limit)
    data = fetch_all(query, params)
    rounded_devis = []
    for row in data:
        devis = {
            'do_piece': row[0],
            'do_date': row[1],
            'ct_intitule': row[2],
            'do_ref': row[3],
            'do_totalht': f'{row[4]:,.2f}'.replace(',', ' '),
            'do_totalttc': f'{row[5]:,.2f}'.replace(',', ' '),
            'do_statut': row[6]
        }
        rounded_devis.append(devis)
    return rounded_devis

def get_devis_by_id(devis_id):
    query = """
    SELECT F_COMPTET.CT_Num, F_COMPTET.CT_Intitule, F_COMPTET.CT_Telephone, F_COMPTET.CT_Adresse,
           F_DOCLIGNE.DO_Piece, F_DOCLIGNE.DO_Ref, F_DOCLIGNE.DO_Date, F_DOCLIGNE.AR_Ref,
           F_DOCLIGNE.DL_Design, F_DOCLIGNE.DL_Qte, F_DOCLIGNE.DL_PUTTC, F_DOCLIGNE.DL_MontantHT,
           F_DOCLIGNE.DL_MontantTTC, F_DOCENTETE.DO_Statut, F_DOCENTETE.DO_TotalHT, F_DOCENTETE.DO_TotalTTC
    FROM F_DOCLIGNE
    INNER JOIN F_COMPTET ON F_COMPTET.CT_Num = F_DOCLIGNE.CT_Num
    INNER JOIN F_DOCENTETE ON F_DOCENTETE.do_piece = F_DOCLIGNE.DO_Piece
    WHERE F_DOCLIGNE.DO_Type = 0 AND F_DOCLIGNE.DO_Piece = ?
    """
    data = fetch_all(query, (devis_id,))

    if not data:
        return []

    products = [
        {
            'AR_Ref': row[7],
            'DL_Design': row[8],
            'DL_Qte': float(row[9]),
            'DL_PUTTC': float(row[10]),
            'DL_MontantHT': float(row[11]),
            'DL_MontantTTC': float(row[12])
        } for row in data
    ]

    row = data[0]
    details = {
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
        'products': products
    }

    return [details]

def Search_Function(q=None, cat=None):
    if cat:
        query = f"SELECT article_table.*, " \
                f"ASZPROD.dbo.product_data.image_picture " \
                f"FROM article_table " \
                f"LEFT JOIN ASZPROD.dbo.product_data " \
                f"ON article_table.AR_Ref = ASZPROD.dbo.product_data.ar_ref " \
                f"WHERE article_table.categorie = ?"
        params = (cat,)
    elif q:
        query = f"SELECT article_table.*, " \
                f"ASZPROD.dbo.product_data.image_picture " \
                f"FROM article_table " \
                f"LEFT JOIN ASZPROD.dbo.product_data " \
                f"ON article_table.AR_Ref = ASZPROD.dbo.product_data.ar_ref " \
                f"WHERE article_table.AR_Ref LIKE ?"
        params = ('%' + q + '%',)

    else:
        query = "SELECT AR_Ref, AR_Design FROM article_table"
        params = ()

    data = fetch_all(query, params)

    if q:
        # Assuming q needs a full detail list of products
        return [{
            'name': row[1],
            'price': round(row[2], 2),
            'qte': int(row[3]),
            'category': row[4],
            'ref': row[0],
            'prix_achat': round(row[8],2),
            'img': row[9]
        } for row in data]
    else:
        # For category-based and default list
        return [{
            'AR_Ref': row[0],
            'AR_Design': row[1],
        } for row in data]

def Get_All_Depot():
    query = "SELECT DE_No, DE_Intitule FROM F_DEPOT"
    data = fetch_all(query)
    return [{'DE_No': row[0], 'DE_Intitule': row[1]} for row in data]

def Get_All_Users():
    # Modified query to format the user_create_date in the desired format with French day and month names
    query = """
    SELECT 
    users.id,
    users.name, 
    users.role, 
    FORMAT(users.user_create_date, 'dd MMM yyyy, HH:mm', 'fr-FR') as user_create_date_formatted,
    FORMAT(MAX(login_hist.LOGINDATTIM), 'dd MMM yyyy, HH:mm', 'fr-FR') as last_login_date_formatted,
    users.user_mail,users.image_base64,users.actif
    FROM 
    users 
    LEFT JOIN 
    login_hist 
    ON 
    users.id = login_hist.IDUSER
    GROUP BY 
    users.id, users.name, users.role, users.user_create_date,users.user_mail,users.image_base64,users.actif
    """
    data = fetch_all(query)
    return [{'id':row[0], 'name': row[1], 'role': row[2], 'user_create_date': row[3], 'last_login_date': row[4], 'user_mail': row[5], 'image_base64': row[6], 'actif': row[7]} for row in data]

def add_user(name,password,role,user_mail,status):
    password = hashlib.md5(password.encode()).hexdigest()
    query = "INSERT INTO users(name,password,role,user_mail,image_base64,actif) VALUES (?,?,?,?,?,?)"
    params = (name,password,role,user_mail,"image",status)
    return execute_query(query, params)

def get_all_depot_users():
    # Updated query to also select the userid
    query = "SELECT userid, name, DE_Intitule FROM user_sel_depots ORDER BY name"
    data = fetch_all(query)
    user_depot_map = {}
    # Create a dictionary to map each user to their depots
    for userid, name, depot in data:
        user_key = (userid, name)  # Using a tuple to store both userid and name as key
        if user_key in user_depot_map:
            user_depot_map[user_key].append(depot)
        else:
            user_depot_map[user_key] = [depot]

    # Format the data for easy use in the front end
    formatted_data = [{'userid': userid, 'name': name, 'DE_Intitule': ', '.join(depots)} for (userid, name), depots in user_depot_map.items()]
    return formatted_data


def get_depots_by_user(userid):
    #select * from user_sel_depots where userid = 1
    query = "SELECT DE_No,DE_Intitule FROM user_sel_depots WHERE userid = ?"
    data = fetch_all(query, (userid,))
    print(data)
    return data


def get_all_depots():
    query = "SELECT DE_No, DE_Intitule FROM F_DEPOT"
    data = fetch_all(query)
    return [{'DE_No': row[0], 'DE_Intitule': row[1]} for row in data]

# Updated function using the new execute_query
def insert_ToEntete(client, date, ref, userid, dateF, devis, co_no):
    query = "INSERT INTO dbo.F_DOCENTETE(DO_Domaine,DO_Type,DO_Piece,DO_Date,DO_Ref,DO_Tiers,CO_No,cbCO_No,DO_Period,DO_Devise,DO_Cours,DE_No,cbDE_No,LI_No,cbLI_No,CT_NumPayeur,DO_Expedit,DO_NbFacture,DO_BLFact,DO_TxEscompte,DO_Reliquat,DO_Imprim,CA_Num,DO_Coord01,DO_Coord02,DO_Coord03,DO_Coord04,DO_Souche,DO_DateLivr,DO_Condition,DO_Tarif,DO_Colisage,DO_TypeColis,DO_Transaction,DO_Langue,DO_Ecart,DO_Regime,N_CatCompta,DO_Ventile,AB_No,DO_DebutAbo,DO_FinAbo,DO_DebutPeriod,DO_FinPeriod,CG_Num,DO_Statut,DO_Heure,CA_No,CO_NoCaissier,DO_Transfere,DO_Cloture,DO_NoWeb,DO_Attente,DO_Provenance,CA_NumIFRS,MR_No,DO_TypeFrais,DO_ValFrais,DO_TypeLigneFrais,DO_TypeFranco,DO_ValFranco,DO_TypeLigneFranco,DO_Taxe1,DO_TypeTaux1,DO_TypeTaxe1,DO_Taxe2,DO_TypeTaux2,DO_TypeTaxe2,DO_Taxe3,DO_TypeTaux3,DO_TypeTaxe3,DO_MajCpta,DO_Motif,DO_Contact,DO_FactureElec,DO_TypeTransac,DO_DateLivrRealisee,DO_DateExpedition,DO_FactureFrs,DO_PieceOrig,DO_EStatut,DO_DemandeRegul,ET_No,cbET_No,DO_Valide,DO_Coffre,DO_TotalHT,DO_StatutBAP,DO_Escompte,DO_DocType,DO_TypeCalcul,DO_TotalHTNet,DO_TotalTTC,DO_NetAPayer,DO_MontantRegle,DO_AdressePaiement,DO_PaiementLigne,DO_MotifDevis,cbProt,cbCreateur,cbModification,cbReplication,cbFlag,cbCreation,cbHashVersion,cbHashDate,cbHashOrder,DO_Conversion,usercreatedevis) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    params = (0,0,devis,date,ref,client,co_no,co_no,2,0,0.000000,1,1,14,14,client,1,1,0,5.000000,0,"","","","","","",0,dateF,1,1,1,1,11,0,0.000000,21,2,0,0,dateF,dateF,dateF,dateF,"34210000",0,"000012617",0,0,0,0,"",0,0,"",0,0,15.000000,0,0,2500.000000,0,0.000000,0,0,0.00000,0,0,0.000000,0,0,0,"","",0,0,dateF,dateF,"","",0,0,0,"",0,0,0.000000,0,1,0,0,0.000000,0.000000,0.000000,0.000000,"",0,0,0,"COLU",date,0,0,date,1,"",0,0,userid)
    return execute_query(query, params)

def insert_ToLigne(client, devis, ar_ref, productDescription, quantity, price, dateF, ref, date, total, co_no):
    query = "INSERT INTO dbo.F_DOCLIGNE(DO_Domaine,DO_Type,CT_Num,DO_Piece,DL_PieceBC,DL_PieceBL,DO_Date,DL_DateBC,DL_DateBL,DL_Ligne,DO_Ref,DL_TNomencl,DL_TRemPied,DL_TRemExep,AR_Ref,DL_Design,DL_Qte,DL_QteBC,DL_QteBL,DL_PoidsNet,DL_PoidsBrut,DL_Remise01REM_Valeur,DL_Remise01REM_Type,DL_Remise02REM_Valeur,DL_Remise02REM_Type,DL_Remise03REM_Valeur,DL_Remise03REM_Type,DL_PrixUnitaire,DL_PUBC,CO_No,AG_No1,AG_No2,DL_PrixRU,DL_CMUP,DL_MvtStock,DT_No,EU_Enumere,EU_Qte,DL_TTC,DE_No,DL_NoRef,DL_TypePL,DL_PUDevise,DL_PUTTC,DO_DateLivr,CA_Num,DL_Frais,DL_Valorise,AR_RefCompose,DL_NonLivre,AC_RefClient,DL_MontantHT,DL_MontantTTC,DL_FactPoids,DL_Escompte,DL_PiecePL,DL_DatePL,DL_QtePL,DL_NoColis,DL_NoLink,DL_QteRessource,DL_DateAvancement,PF_Num,DL_PieceOFProd,DL_PieceDE,DL_DateDE,DL_QteDE,DL_Operation,DL_NoSousTotal,CA_No,DO_DocType) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    params = (0,0,client,devis,"","",date,dateF,dateF,1000,ref,0,0,0,ar_ref,productDescription,quantity,0.000000,0.000000,0.000000,0.000000,0.000000,1,0.000000,0,0.000000,0,price,0.000000,co_no,0,0,0.000000,6.000000,0,0,"Unité",quantity,0,1,1,0,0.000000,price*1.2,dateF,"",0.000000,1,"",0,"",total,total*1.2,0,0,"",dateF,0.000000,"",0,0,dateF,"",0,"",date,1.000000,"",0,0,0)
    return execute_query(query, params)

def insert_ToDocRegl(devis, date):
    query = "INSERT INTO dbo.F_DOCREGL(DR_No, DO_Domaine, DO_Type, DO_Piece, DR_TypeRegl, DR_Date, DR_Libelle, DR_Pourcent, DR_Montant, DR_MontantDev, DR_Equil, EC_No, DR_Regle, N_Reglement, CA_No, DO_DocType) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    params = (last_DR_No(), 0, 0, devis, 2, date, '', 0.000000, 0.000000, 0.000000, 1, 0, 0, 1, 0, 0)
    return execute_query(query, params)


