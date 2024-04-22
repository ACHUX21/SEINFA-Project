import pyodbc, requests
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, render_template_string,g
from jawt import authen, verifyjwt
import time

from functions import (
    last_dev_mssql,
    fetch_products,
    get_categories,
    Get_CT_NUM,
    insert_ToEntete,
    insert_ToLigne,
    insert_ToDocRegl,
    get_all_devis,
    get_devis_by_id,
    Search_Function,
    get_all_devis_by_co_no,
    Get_All_Depot,
    Get_All_Users,
    get_all_depot_users,
    get_depots_by_user,
    add_user,
    get_all_depots,
    get_product_by_ref
)
from mysqlDB import (
    select_tmpCart,
    addTo_tmpCart,
    removeFrom_tmpCart,
    clean_tmpCart,
    get_TOTAL,
    last_dev,
    add_devis_draft,
    get_drafts,
    check_auth,
    get_drafts_details,
    get_draft_devis,
    clean_drafts,
    add_devis_draft_details_batch
)
from dash import (
    get_ca_client_co_no_2024,
    get_ca_products_co_no_2024,
    get_all_client_by_co_no,
    get_ca_by_co_no,
    get_all_ca,
    get_products_en_promotions,
    encours_commercial_client
)

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.56.212,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;MARS_Connection=Yes;MultipleActiveResultSets=True;')

app = Flask(__name__, static_folder='static', template_folder='Template')

def fetch_config():
    url = "https://data-dev.ma/seinfa/config.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        data = response.json()
        return data.get('maintenance_mode', False), data.get('promotion_value', 0)  # Default values if not found
    except requests.RequestException as e:
        print(f"Error fetching configuration: {e}")
        return False, 0  # Defaults to normal operation and promotion value 0 if there's an error

# Flask route or application logic
@app.before_request
def check_for_maintenance_and_promotion():
    maintenance_mode, promotion_value = fetch_config()
    if maintenance_mode:
        return render_template_string('''
        <h1>Site en maintenance</h1>
        <p>Le site est actuellement en maintenance, veuillez réessayer plus tard</p>
        '''), 503
    g.promotion_value = promotion_value  # Use Flask's g object to make it available globally in the app context


# Login Routes
@app.route('/')
def index():
    token = request.cookies.get('token')
    if token:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# dashboard Route
@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    return render_template('dashboard.html', username=payload['username'],role=payload['role'], data_client=get_ca_client_co_no_2024(payload['co_no'], payload['role']), data_product=get_ca_products_co_no_2024(payload['co_no'], payload['role']),count_client=get_all_client_by_co_no(payload['co_no'], payload['role']), ca=get_ca_by_co_no(payload['co_no'], payload['role']),ca_all=get_all_ca( payload['co_no'] ,payload['role'] ),encours_commercial_client=encours_commercial_client(payload['co_no'], payload['role']))

@app.route('/newandpromotions')
def newandpromotions():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    return render_template('actualiteetnews.html', username=payload['username'],role=payload['role'], products_en_promotions=get_products_en_promotions())

@app.route('/login', methods=['GET'])
def login():
    token = request.cookies.get('token')
    if token:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    auth = authen(username, password, request.remote_addr)
    if not username or not password or not auth:
        return render_template('login.html', error='Nom d\'utilisateur ou mot de passe incorrect')
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('token', auth)
    return response

# Commandes Route
@app.route('/commandes', methods=['GET'])
def commandes():
    # Retrieve the token and validate it
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))

    # Fetch necessary data based on the user's token and query parameters
    user_id = payload['id']
    category = request.args.get('cat')
    tmp_cart = select_tmpCart(user_id)
    categories = get_categories()
    last_device = last_dev()
    depot = Get_All_Depot()
    depot_per_user =get_depots_by_user(user_id)
    # Determine the number of products to fetch based on category presence
    if category:
        products = fetch_products(20, category)
    else:
        products = fetch_products(20)

    # Render the template with all necessary data
    return render_template(
        'commande.html',
        last_dev=last_device,
        products=products,
        categories=categories,
        tmpCart=tmp_cart,
        username=payload['username'],
        role=payload['role'],
        total=get_TOTAL(user_id),
        depot=depot,
        user_depot=depot_per_user

    )
# #def add_user(name,password,role,user_mail,image):
#     query = "INSERT INTO users(name,password,role,user_create_date,user_mail,image,1) VALUES (?,?,?,?,?,?)"
#     params = (name,password,role,datetime.datetime.now(),user_mail,image)
#     return execute_query(query, params)
@app.route('/users', methods=['GET'])
def users():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if payload['role'] != 'Administrateur':
        print(payload['role'])
        return redirect(url_for('index'))
    if not payload:
        return redirect(url_for('index'))
    return render_template('users.html', username=payload['username'],role=payload['role'], users=Get_All_Users(),depots = get_all_depots())

@app.route('/add_user', methods=['POST'])
def add_users():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    if not payload['role']:
        return redirect(url_for('logout'))
    if payload['role'] != 'Administrateur':
        return redirect(url_for('index'))
    if not payload:
        return redirect(url_for('index'))
    name = request.form['user_name']
    password = request.form['user_password']
    role = request.form['user_role']
    user_mail = request.form['user_email']
    image = ""
    statut = request.form['user_statut']
    # if not name or not password or not role or not user_mail or not image:
    #     return render_template('users.html', username=payload['username'],role=payload['role'], users=Get_All_Users(), error='S\'il vous plaît remplir tous les champs')
    f = add_user(name, password,role, user_mail,statut)
    print(f)
    if not f:
        return render_template('users.html', username=payload['username'],role=payload['role'], users=Get_All_Users(), error='Erreur lors de l\'enregistrement de l\'utilisateur')
    print(name,password,user_mail)
    return redirect(url_for('users'))

@app.route('/upload_pic', methods=['POST'])
def upload_pic():
    data = request.get_json()
    username = data['username']
    image = data['image']
    print(username, image)
    time.sleep(2)

    cursor = conn.cursor()
    query = "UPDATE users SET image_base64 = ? WHERE name = ?"
    cursor.execute(query, image, username)
    cursor.commit()
    cursor.close()
    return jsonify('success')

@app.route('/products', methods=['GET'])
def products_images():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    return render_template('products.html', articles=fetch_products(500), username=payload['username'],role=payload['role'])

@app.route('/product_details/<string:ref>', methods=['GET'])
def product_images(ref):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    product = get_product_by_ref(ref)
    return render_template('product_details.html',product=product, username=payload['username'],role=payload['role'])


@app.route('/users_depot', methods=['GET','POST'])
def users_depot():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    if not payload['role']:
        return redirect(url_for('logout'))
    if payload['role'] != 'Administrateur':
        return redirect(url_for('index'))
    if not payload:
        return redirect(url_for('index'))
    users = get_all_depot_users()  # Fetches the list of users
    if not users:
        print("No users fetched. Check the database and query.")
    return render_template('users_depot.html', users=users,depots = get_all_depots(),all_users=Get_All_Users(), username=payload['username'],role=payload['role'])
# api/user_depots
@app.route('/api/user_depots/<int:user_id>', methods=['POST'])
def update_user_depots(user_id):
    # Retrieve depot IDs from the form data
    data = request.get_json()
    depots = data['depots']
    cursor = conn.cursor()
    
    # Delete existing user-depot relations
    cursor.execute('DELETE FROM user_depots WHERE userid = ?', (user_id,))
    
    # Insert new user-depot relations
    for depot_id in depots:
        cursor.execute('INSERT INTO user_depots (userid, depot_id) VALUES (?, ?)', (user_id, depot_id))
    
    # Commit transaction and close connections
    conn.commit()
    cursor.close()
    
    # Return a success message
    return jsonify({'status': 'success'})


# # Submit Route
# @app.route('/submit', methods=['POST'])
# def submit():
#     token = request.cookies.get('token')
#     if not token:
#         return redirect(url_for('index'))
#     payload = verifyjwt(token)
#     if not payload:
#         return redirect(url_for('index'))
#     client = request.form['client']
#     date = request.form['date']
#     date = '-'.join(date.split('-')[::-1])
#     ref = request.form['ref']
#     if not client or not date or not ref:
#         return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='S\'il vous plaît remplir tous les champs')
#     client = Get_CT_NUM(client)
#     var_last_devis = last_dev()
#     f = add_devis_draft(client, date, ref, var_last_devis, payload['id'], request.form['client'])
#     if not f:
#         return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='Erreur lors de l\'enregistrement de la commande')
#     if len(ref) > 17:
#         return redirect(url_for('commandes'))
#     paniers = select_tmpCart(payload['id'])
#     if not paniers:
#         return redirect(url_for('commandes'))
#     for panier in paniers:
#         f = add_devis_draft_details(client, panier['ref'], panier['name'], panier['qte'], panier['price'], "1753-01-01", ref, date, panier['qte'] * panier['price'], var_last_devis, payload['id'])
#         if not f:
#             return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='Erreur lors de l\'enregistrement de la commande')
#     clean_tmpCart(payload['id'])
#     return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), success='Commande enregistrée avec succès', total=get_TOTAL(payload['id']))


@app.route('/submit', methods=['POST'])
def submit():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))

    client = request.form['client']
    date = request.form['date']
    date = '-'.join(date.split('-')[::-1])  # Reformatting date if necessary
    ref = request.form['ref']
    if not client or not date or not ref:
        return render_template('commande.html', last_dev=last_dev(), products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error="S'il vous plaît remplir tous les champs")

    client_id = Get_CT_NUM(client)  # Get client ID based on name
    var_last_devis = last_dev()
    f = add_devis_draft(client_id, date, ref, var_last_devis, payload['id'], request.form['client'])
    if not f:
        return render_template("commande.html", last_dev=last_dev(), products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='Erreur lors de l\'enregistrement de la commande')

    if len(ref) > 17:
        return redirect(url_for('commandes'))

    paniers = select_tmpCart(payload['id'])
    if not paniers:
        return redirect(url_for('commandes'))

    details = []
    for panier in paniers:
        detail = {
            'client': client_id,
            'ar_ref': panier['ref'],
            'productDescription': panier['name'],
            'quantity': panier['qte'],
            'price': panier['price'],
            'dateF': "1753-01-01",
            'ref': ref,
            'date': date,
            'total': panier['qte'] * panier['price'],
            'devis': var_last_devis,
            'userid': payload['id']
        }
        details.append(detail)

    result = add_devis_draft_details_batch(details)
    if not result:
        return render_template("commande.html", last_dev=last_dev(), products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='Erreur lors de l\'enregistrement de la commande')

    clean_tmpCart(payload['id'])
    return render_template("commande.html", last_dev=last_dev(), products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), success='Commande enregistrée avec succès', total=get_TOTAL(payload['id']))


# @app.route('/submit', methods=['POST'])
# def submit():
#     token = request.cookies.get('token')
#     if not token:
#         return redirect(url_for('index'))
#     payload = verifyjwt(token)
#     if not payload:
#         return redirect(url_for('index'))
#     client = request.form['client']
#     date = request.form['date']
#     date = '-'.join(date.split('-')[::-1])
#     ref = request.form['ref']

#     if not client or not date or not ref:
#         return render_template('commande.html', last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='S\'il vous plaît remplir tous les champs')
#     client = Get_CT_NUM(client)
#     if not client:
#         return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(payload['id']), error='Client introuvable')
#     if len(ref) > 17:
#         return redirect(url_for('commandes'))
#     userid = int(payload['id'])
#     dateF = "1753-01-01"
#     devis = last_dev()
#     t = insert_ToEntete(client, date, ref, userid, dateF, devis)
#     print(t)
#     if not t:
#         return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), error='Erreur lors de l\'enregistrement de la commande DOC_ENTETE')
#     paniers = select_tmpCart(userid)
#     if not paniers:
#         return redirect(url_for('commandes'))
#     for panier in paniers:
#         t = insert_ToLigne(client, devis, panier['ref'], panier['name'], panier['qte'], panier['price'], dateF, ref, date, panier['qte'] * panier['price'])
#         print(t)
#         if not t:
#             return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), error='Erreur lors de l\'enregistrement de la commande DOC_LIGNE')
        
#     t = insert_ToDocRegl(devis, date)
#     print(t)
#     if not t:
#         return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), error='Erreur lors de l\'enregistrement de la commande DOC_REGL')
#     clean_tmpCart(userid)
#     return render_template("commande.html", last_dev=last_dev() , products=fetch_products(20), categories=get_categories(), tmpCart=select_tmpCart(userid), success='Commande enregistrée avec succès', total=get_TOTAL(userid))

# Voir devis Route
@app.route('/voirdevis', methods=['GET'])
def voirDevis():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    if payload['role'] == 'Administrateur':
        devis = get_all_devis()
    else:
        devis = get_all_devis_by_co_no(payload['co_no'])
    return render_template('voir_commande.html', devis=devis, username=payload['username'],role=payload['role'])

# Cart Routes
@app.route('/addToCart', methods=['POST'])
def addToCart():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
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
        return redirect(url_for('logout'))
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
    r.set_cookie('token', '', expires=0)
    return r




# Draft Routes
@app.route('/voirDraft', methods=['GET'])
def draftDevis():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    if payload['role'] == 'Administrateur':
        drafts = get_drafts()
    else:
        drafts = get_drafts(payload['id'])
    return render_template('voir_draft.html', draft=drafts, username=payload['username'],role=payload['role'])

# API Routes

# API Devis Draft Validation Route
@app.route('/api/validerdraft/<string:devis>', methods=['GET'])
def validerDraftNum(devis):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    if payload['role'] == 'Administrateur':
        auth = True
    else:
        auth = check_auth(payload['id'], devis)
    if not auth:
        return redirect(url_for('index'))
    data = get_drafts_details(devis)
    client = data[0]['client']
    date = data[0]['date']
    ref = data[0]['ref']
    print(client, date, ref)
    if not client or not date or not ref:
        return render_template('detail_devis_draft.html', error='S\'il vous plaît remplir tous les champs', username=payload['username'],role=payload['role'], data=[], d_data=[])
    var_last_devis = last_dev_mssql()
    userid = int(payload['id'])
    dateF = "1753-01-01"
    co_no = payload['co_no']
    f = insert_ToEntete(client, date, ref, userid, dateF, var_last_devis, co_no)
    if not f:
        return redirect(url_for('draftDevis'))
    for i in data:
        f = insert_ToLigne(client, var_last_devis, i['ar_ref'], i['productDescription'], float(i['quantity']), float(i['price']), dateF, ref, date, float(i['quantity']) * float(i['price']), co_no)
        if not f:
            return redirect(url_for('draftDevis'))
    f = insert_ToDocRegl(var_last_devis, date)
    if not f:
        return redirect(url_for('draftDevis'))
    clean_drafts(devis)
    return redirect(url_for('draftDevis'))





# API Devis Draft Route
@app.route('/api/voirdraft/<string:devis>', methods=['GET'])
def voirDraftNum(devis):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    if payload['role'] == 'Administrateur':
        auth = True
    else:
        auth = check_auth(payload['id'], devis)
    # print(auth)
    if not auth:
        return redirect(url_for('index'))
    data = get_drafts_details(devis)
    if payload['role'] == 'Administrateur':
        d_data = get_draft_devis(devis)
    else:
        d_data = get_drafts(payload['id'], devis)
    # print(d_data)
    if not data:
        return render_template('detail_devis_draft.html', error='Devis introuvable', username=payload['username'],role=payload['role'], data=[])
    return render_template('detail_devis_draft.html',d_data=d_data[0], data=data, username=payload['username'],role=payload['role'])


# API Devis Route
@app.route('/api/voirdevis/<string:devis>', methods=['GET'])
def voirDevisNum(devis):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    devis = get_devis_by_id(devis)
    if not devis or not devis[0] or not devis[0]['products']:
        devis = [{'CT_Num': '', 'CT_Intitule': '', 'CT_Telephone': '', 'CT_Adresse': '', 'DO_Piece': '', 'DO_Ref': '', 'DO_Date': '', 'DO_Statut': 0, 'DO_TotalHT': 0, 'DO_TotalTTC': 0, 'products': [{'AR_Ref': '', 'DL_Design': '', 'DL_Qte': 0, 'DL_PUTTC': 0, 'DL_MontantHT': 0, 'DL_MontantTTC': 0}]}]
    return render_template('detail_commande.html',entete=devis[0], lignes=devis[0]['products'], username=payload['username'],role=payload['role'])

# CREATE TABLE [dbo].[product_data](
#     [ar_ref] [varchar](255) NOT NULL,
#     [image_picture] [varchar](max) NULL,
# PRIMARY KEY CLUSTERED 
# (
#     [ar_ref] ASC
# )

# API upload img product
@app.route('/api/uploadimg', methods=['POST'])
def upload_img():
    data = request.get_json()
    ref = data['ref']
    img = data['img']
    cursor = conn.cursor()
    query = "INSERT INTO product_data(ar_ref, image_picture) VALUES (?, ?)"
    cursor.execute(query, ref, img)
    cursor.commit()
    cursor.close()
    return jsonify('success')


# API client Route
@app.route('/api/clients', methods=['GET'])
def clients():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
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
        return redirect(url_for('logout'))
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
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    
    if request.args.get('cat'):
        return jsonify(Search_Function(None, request.args.get('cat')))
    
    if not request.args.get('q'):
        return jsonify(Search_Function())
    return jsonify(Search_Function(request.args.get('q')))

# Categories Route
@app.route('/api/categories', methods=['GET'])
def categories():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    categories = get_categories()
    return jsonify(categories)

# temp Cart Route
@app.route('/api/tmpcart', methods=['GET'])
def tmpCart():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    p = select_tmpCart(payload['id'])
    if not p:
        return jsonify([])
    return jsonify(p)

# Total Route
@app.route('/api/total', methods=['GET'])
def total():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('index'))
    return jsonify({'total': get_TOTAL(payload['id'])})

# update actif Route
@app.route('/api/update_actif/<string:username>', methods=['GET'])
def update_user_actif(username):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    if not payload['role']:
        return redirect(url_for('logout'))
    if payload['role'] != 'Administrateur':
        return redirect(url_for('index'))
    if not payload:
        return redirect(url_for('index'))
    cursor = conn.cursor()
    query = "UPDATE users SET actif = (CASE WHEN actif = 1 THEN 0 ELSE 1 END) WHERE name = ?"
    cursor.execute(query, username)
    cursor.commit()
    cursor.close()
    return redirect(url_for('users'))



# delete user Route
@app.route('/api/delete_user/<string:username>', methods=['GET'])
def delete_user(username):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    if not payload['role']:
        return redirect(url_for('logout'))
    if payload['role'] != 'Administrateur':
        return redirect(url_for('index'))
    if not payload:
        return redirect(url_for('index'))
    cursor = conn.cursor()
    query = "DELETE FROM users WHERE name = ?"
    cursor.execute(query, username)
    cursor.commit()
    cursor.close()
    return redirect(url_for('users'))

@app.route('/api/delete_depots_user/<int:user_id>', methods=['GET'])
def delete_depots_user(user_id):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('logout'))
    payload = verifyjwt(token)
    if not payload:
        return redirect(url_for('logout'))
    if not payload['role']:
        return redirect(url_for('logout'))
    if payload['role'] != 'Administrateur':
        return redirect(url_for('index'))
    if not payload:
        return redirect(url_for('index'))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_depots WHERE userid = ?', (user_id))
    conn.commit()
    cursor.close()
    return redirect(url_for('users_depot'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000,threaded=True)