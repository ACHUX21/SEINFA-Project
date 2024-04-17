import pyodbc,datetime
from flask import jsonify
import time


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.118.25.162,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')


# last devis
def last_dev_mssql():
    cursor = conn.cursor()
    query = "SELECT DO_PIECE from F_DOCENTETE where DO_Type = 0 ORDER BY DO_PIECE DESC"
    cursor.execute(query)
    devis = cursor.fetchone()
    cursor.close()
    last_devis = devis[0]
    prefix = last_devis[:2]
    current_number = last_devis[2:]
    number = str(int(current_number) + 1).zfill(len(current_number))
    return prefix + number

def last_DR_No():
    cursor = conn.cursor()
    query = "SELECT DR_No from F_DOCREGL ORDER BY DR_No DESC"
    cursor.execute(query)
    devis = cursor.fetchone()
    cursor.close()
    return int(devis[0] + 1)


#add taxe here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSERT FUNCTIONS
# INSERT INTO DOCENTETE
def insert_ToEntete(client, date, ref, userid, dateF, devis, co_no):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO dbo.F_DOCENTETE(DO_Domaine,DO_Type,DO_Piece,DO_Date,DO_Ref,DO_Tiers,CO_No,cbCO_No,DO_Period,DO_Devise,DO_Cours,DE_No,cbDE_No,LI_No,cbLI_No,CT_NumPayeur,DO_Expedit,DO_NbFacture,DO_BLFact,DO_TxEscompte,DO_Reliquat,DO_Imprim,CA_Num,DO_Coord01,DO_Coord02,DO_Coord03,DO_Coord04,DO_Souche,DO_DateLivr,DO_Condition,DO_Tarif,DO_Colisage,DO_TypeColis,DO_Transaction,DO_Langue,DO_Ecart,DO_Regime,N_CatCompta,DO_Ventile,AB_No,DO_DebutAbo,DO_FinAbo,DO_DebutPeriod,DO_FinPeriod,CG_Num,DO_Statut,DO_Heure,CA_No,CO_NoCaissier,DO_Transfere,DO_Cloture,DO_NoWeb,DO_Attente,DO_Provenance,CA_NumIFRS,MR_No,DO_TypeFrais,DO_ValFrais,DO_TypeLigneFrais,DO_TypeFranco,DO_ValFranco,DO_TypeLigneFranco,DO_Taxe1,DO_TypeTaux1,DO_TypeTaxe1,DO_Taxe2,DO_TypeTaux2,DO_TypeTaxe2,DO_Taxe3,DO_TypeTaux3,DO_TypeTaxe3,DO_MajCpta,DO_Motif,DO_Contact,DO_FactureElec,DO_TypeTransac,DO_DateLivrRealisee,DO_DateExpedition,DO_FactureFrs,DO_PieceOrig,DO_EStatut,DO_DemandeRegul,ET_No,cbET_No,DO_Valide,DO_Coffre,DO_TotalHT,DO_StatutBAP,DO_Escompte,DO_DocType,DO_TypeCalcul,DO_TotalHTNet,DO_TotalTTC,DO_NetAPayer,DO_MontantRegle,DO_AdressePaiement,DO_PaiementLigne,DO_MotifDevis,cbProt,cbCreateur,cbModification,cbReplication,cbFlag,cbCreation,cbHashVersion,cbHashDate,cbHashOrder,DO_Conversion,usercreatedevis) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(query, (0,0,devis,date,ref,client,co_no,co_no,2,0,0.000000,1,1,14,14,client,1,1,0,5.000000,0,"","","","","","",0,dateF,1,1,1,1,11,0,0.000000,21,2,0,0,dateF,dateF,dateF,dateF,"34210000",0,"000012617",0,0,0,0,"",0,0,"",0,0,15.000000,0,0,2500.000000,0,0.000000,0,0,0.00000,0,0,0.000000,0,0,0,"","",0,0,dateF,dateF,"","",0,0,0,"",0,0,0.000000,0,1,0,0,0.000000,0.000000,0.000000,0.000000,"",0,0,0,"COLU",date,0,0,date,1,"",0,0,userid))
        cursor.commit()
        cursor.close()
        print("Data inserted DocEntete")
        return "Data inserted DocEntete"
    except Exception as e:
        print(e)
        return None

#add taxe here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSERT INTO DOCLIGNE
def insert_ToLigne(client, devis, ar_ref, productDescription, quantity, price, dateF, ref, date, total, co_no):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO dbo.F_DOCLIGNE(DO_Domaine,DO_Type,CT_Num,DO_Piece,DL_PieceBC,DL_PieceBL,DO_Date,DL_DateBC,DL_DateBL,DL_Ligne,DO_Ref,DL_TNomencl,DL_TRemPied,DL_TRemExep,AR_Ref,DL_Design,DL_Qte,DL_QteBC,DL_QteBL,DL_PoidsNet,DL_PoidsBrut,DL_Remise01REM_Valeur,DL_Remise01REM_Type,DL_Remise02REM_Valeur,DL_Remise02REM_Type,DL_Remise03REM_Valeur,DL_Remise03REM_Type,DL_PrixUnitaire,DL_PUBC,CO_No,AG_No1,AG_No2,DL_PrixRU,DL_CMUP,DL_MvtStock,DT_No,EU_Enumere,EU_Qte,DL_TTC,DE_No,DL_NoRef,DL_TypePL,DL_PUDevise,DL_PUTTC,DO_DateLivr,CA_Num,DL_Frais,DL_Valorise,AR_RefCompose,DL_NonLivre,AC_RefClient,DL_MontantHT,DL_MontantTTC,DL_FactPoids,DL_Escompte,DL_PiecePL,DL_DatePL,DL_QtePL,DL_NoColis,DL_NoLink,DL_QteRessource,DL_DateAvancement,PF_Num,DL_PieceOFProd,DL_PieceDE,DL_DateDE,DL_QteDE,DL_Operation,DL_NoSousTotal,CA_No,DO_DocType) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(query, (0,0,client,devis,"","",date,dateF,dateF,1000,ref,0,0,0,ar_ref,productDescription,quantity,0.000000,0.000000,0.000000,0.000000,0.000000,1,0.000000,0,0.000000,0,price,0.000000,co_no,0,0,0.000000,6.000000,0,0,"Unité",quantity,0,1,1,0,0.000000,price*1.2,dateF,"",0.000000,1,"",0,"",total,total*1.2,0,0,"",dateF,0.000000,"",0,0,dateF,"",0,"",date,1.000000,"",0,0,0))
        cursor.commit()
        cursor.close()
        print("Data inserted DocLigne")
        return "Data inserted DocLigne"
    except Exception as e:
        print(e)
        return None

# INSERT INTO DOCREGL
def insert_ToDocRegl(devis, date):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO dbo.F_DOCREGL(DR_No, DO_Domaine, DO_Type, DO_Piece, DR_TypeRegl, DR_Date, DR_Libelle, DR_Pourcent, DR_Montant, DR_MontantDev, DR_Equil, EC_No, DR_Regle, N_Reglement, CA_No, DO_DocType) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(query, (last_DR_No(), 0, 0, devis, 2, date, '', 0.000000, 0.000000, 0.000000, 1, 0, 0, 1, 0, 0))
        cursor.commit()
        cursor.close()
        print("Data inserted DocRegl")
        return "Data inserted DocRegl"
    except Exception as e:
        print(e)
        return None

  
# other functions
# GET CLIENT NUMBER BY CT_INTITULE
def Get_CT_NUM(CT_INTITULE):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CT_NUM FROM F_COMPTET WHERE CT_INTITULE = ?", CT_INTITULE)
        data = cursor.fetchone()
        cursor.close()
        return data[0]
    except Exception as e:
        return e
    
# FETCH PRODUCTS
def fetch_products(num=20, cat=None):
    if not isinstance(num, int):
        raise ValueError('num must be an integer')
    cursor = conn.cursor()
    query = f"""
    SELECT TOP {num} * FROM article_table ORDER BY AS_QteSto DESC
    """
    if cat:
        query = f"""
        SELECT TOP {num} * FROM article_table WHERE categorie = ?  ORDER BY AS_QteSto DESC
        """
        cursor.execute(query, cat)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    products = []
    for row in data:
        product = {
            'name': row[1],
            'price': round(row[2], 2),
            'qte': int(row[3]),
            'category': row[4],
            'ref': row[0],
        }
        products.append(product)

    return products

# GET CATEGORIES
def get_categories():   
    cursor = conn.cursor()
    query = f"SELECT categorie FROM article_table GROUP BY categorie ORDER BY SUM(AS_QteSto) DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    categories = []
    for row in data:
        categories.append(row[0])
    return categories



# voir  les devis
def get_all_devis(offset=0, limit=200000):
    cursor = conn.cursor()
    query = """
    SELECT do_piece, FORMAT(do_date, 'yyyy-MM-dd') as short_date, ct_intitule, do_ref, do_totalht, do_totalttc, do_statut
    FROM f_docentete
    INNER JOIN f_comptet ON f_comptet.ct_num = f_docentete.do_tiers
    WHERE do_type = 0
    ORDER BY do_date DESC
    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    cursor.execute(query, (offset, limit))
    devis = cursor.fetchall()
    cursor.close()
    rounded_devis = []
    for row in devis:
 
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
    cursor = conn.cursor()
    query = """
    SELECT do_piece, FORMAT(do_date, 'yyyy-MM-dd') as short_date, ct_intitule, do_ref, do_totalht, do_totalttc, do_statut
    FROM f_docentete
    INNER JOIN f_comptet ON f_comptet.ct_num = f_docentete.do_tiers
    WHERE do_type = 0 AND f_docentete.co_no = ?
    ORDER BY do_date DESC
    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    cursor.execute(query, (co_no, offset, limit))
    devis = cursor.fetchall()
    cursor.close()
    rounded_devis = []
    for row in devis:
 
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

    try:
        details[0]['products'] = products
    except:
        pass

    return details


def Search_Function(q=None, cat=None):
    if cat:
        query = """ SELECT AR_Ref, AR_Design FROM article_table WHERE categorie = ? """
        cursor = conn.cursor()
        cursor.execute(query, cat)
        data = cursor.fetchall()
        cursor.close()
        products = []
        for row in data:
            product = {
                'AR_Ref': row[0],
                'AR_Design': row[1],
            }
            products.append(product)
        return products
    if q:
        query = """ SELECT * FROM article_table WHERE AR_Ref LIKE ? """
        cursor = conn.cursor()
        cursor.execute(query, (q,))
        data = cursor.fetchall()
        cursor.close()
        products = []
        for row in data:
            product = {
                'name': row[1],
                'price': round(row[2], 2),
                'qte': int(row[3]),
                'category': row[4],
                'ref': row[0],
            }
            products.append(product)
            break
        
        return products

    query = """ SELECT AR_Ref, AR_Design FROM article_table """
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    products = []
    for row in data:
        product = {
            'AR_Ref': row[0],
            'AR_Design': row[1],
        }
        products.append(product)
    return products

