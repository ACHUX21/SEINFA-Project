import pyodbc
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from jawt import authen,verifyjwt
from functions import last_dev, fetch_products, get_categories, Get_CT_NUM, insert_ToEntete, insert_ToLigne, insert_ToDocRegl, get_all_devis, get_devis_by_id, Search_Function
from mysqlDB import select_tmpCart, addTo_tmpCart, removeFrom_tmpCart, clean_tmpCart, get_TOTAL
from re import match

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.28.6,1433;DATABASE=UNIO 2020;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')

app = Flask(__name__, static_folder='static', template_folder='Template')


# Login Routes
@app.route('/')
def index():
    token = request.cookies.get('token')
    if token:
        return redirect(url_for('commandes'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    token = request.cookies.get('token')
    if token:
        return redirect(url_for('commandes'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    auth = authen(username, password)
    if not username or not password or not auth:
        return render_template('login.html', error='Nom d\'utilisateur ou mot de passe incorrect')
    response = make_response(redirect(url_for('commandes')))
    response.set_cookie('token', auth, httponly=True, secure=True)
    return response

# Commandes Route
@app.route('/commandes', methods=['GET'])
def commandes():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    
    p = select_tmpCart(payload['id'])
    if not p:
        return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20, request.args.get('cat')), categories=get_categories(),username=payload['username'],role=payload['role'], total=get_TOTAL(payload['id']))
    if request.args.get('cat'):
        return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20, request.args.get('cat')), categories=get_categories(), tmpCart=select_tmpCart(payload['id']),username=payload['username'],role=payload['role'], total=get_TOTAL(payload['id']))
    return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']),username=payload['username'],role=payload['role'], total=get_TOTAL(payload['id']))

# Submit Route
@app.route('/submit', methods=['POST'])
def submit():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    client = request.form['client']
    date = request.form['date']
    # 05-04-2024
    ref = request.form['ref']

    if not client or not date or not ref:
        return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='S\'il vous plaît remplir tous les champs')
    if not match(r'\d{2}-\d{2}-\d{4}', date):
        return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='La date doit être au format YYYY-MM-DD')
    client = Get_CT_NUM(client)
    if not client:
        return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='Client introuvable')
    if len(ref) > 17:
        return redirect(url_for('commandes'))
    userid = int(payload['id'])
    dateF = "1753-01-01"
    devis = last_dev()
    t = insert_ToEntete(client, date, ref, userid, dateF, devis)
    print(t)
    if not t:
        return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), error='Erreur lors de l\'enregistrement de la commande DOC_ENTETE')
    paniers = select_tmpCart(userid)
    if not paniers:
        return redirect(url_for('commandes'))
    for panier in paniers:
        t = insert_ToLigne(client, devis, panier['ref'], panier['name'], panier['qte'], panier['price'], dateF, ref, date, panier['qte'] * panier['price'])
        print(t)
        if not t:
            return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), error='Erreur lors de l\'enregistrement de la commande DOC_LIGNE')
        
    t = insert_ToDocRegl(devis, date)
    print(t)
    if not t:
        return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), error='Erreur lors de l\'enregistrement de la commande DOC_REGL')
    clean_tmpCart(userid)
    return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), success='Commande enregistrée avec succès', total=get_TOTAL(userid))

# Voir devis Route
@app.route('/voirdevis', methods=['GET'])
def voirDevis():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    devis = get_all_devis()
    return render_template('voir_commande.html', devis=devis, username=payload['username'],role=payload['role'])

# Cart Routes
@app.route('/addToCart', methods=['POST'])
def addToCart():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    data = request.get_json()
    p = addTo_tmpCart(data, payload['id'])
    if p:
        return jsonify('success')
    return jsonify('error')

@app.route('/removeFromCart', methods=['DELETE'])
def removeFromCart():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    data = request.get_json()
    if not data or 'name' not in data or not data['name'] or not isinstance(data['name'], str):
        return jsonify('Invalid data provided')
    p = removeFrom_tmpCart(data['name'])
    if p:
        return jsonify('success')
    return jsonify('error')

# Logout Route
@app.route('/logout')
def logout():
    r = make_response(redirect(url_for('index')))
    r.set_cookie('token', '', expires=0, httponly=True, secure=True)
    return r




# API Routes
# API Devis Route
@app.route('/api/voirdevis/<string:devis>', methods=['GET'])
def voirDevisNum(devis):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    devis = get_devis_by_id(devis)
    if not devis or not devis[0] or not devis[0]['products']:
        devis = [{'CT_Num': '', 'CT_Intitule': '', 'CT_Telephone': '', 'CT_Adresse': '', 'DO_Piece': '', 'DO_Ref': '', 'DO_Date': '', 'DO_Statut': 0, 'DO_TotalHT': 0, 'DO_TotalTTC': 0, 'products': [{'AR_Ref': '', 'DL_Design': '', 'DL_Qte': 0, 'DL_PUTTC': 0, 'DL_MontantHT': 0, 'DL_MontantTTC': 0}]}]
    return render_template('detail_commande.html',entete=devis[0], lignes=devis[0]['products'], username=payload['username'],role=payload['role'])

# API client Route
@app.route('/api/clients', methods=['GET'])
def clients():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    cursor = conn.cursor()
    query = "SELECT CT_INTITULE,CT_NUM from F_COMPTET Where CT_Type = 0 AND CT_Sommeil = 0 and CT_Prospect = 0 ORDER BY CT_INTITULE"
    cursor.execute(query) 
    clients = cursor.fetchall()
    cursor.close()
    return jsonify([dict(zip(('CT_INTITULE', 'CT_NUM'), row)) for row in clients])

# API products Route
@app.route('/api/products/<int:num>', methods=['GET'])
def products(num):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    if request.args.get('cat'):
        products = fetch_products(num, request.args.get('cat'))
    else:
        products = fetch_products(num)
    return jsonify(products)

@app.route('/api/search', methods=['GET'])
def search():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('index'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    
    if request.args.get('cat'):
        return jsonify(Search_Function(None, request.args.get('cat')))
    
    if not request.args.get('q'):
        return jsonify(Search_Function())
    return jsonify(Search_Function(request.args.get('q')))



if __name__ == '__main__':
    app.run(debug=True)