import jwt,datetime,hashlib,pyodbc
import os

# JWT secret key
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'aopzoefj321'


# Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.28.6,1433;DATABASE=UNIO 2020;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;')

# JWT functions
def authen(username, password):
    try:
        if not username or not password:
            return None
        cursor = conn.cursor()
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute("SELECT id from users WHERE name = ? AND password = ?", (username, password))
        id = cursor.fetchone()[0]
        if not id:
            return None
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("SELECT role from users WHERE name = ? AND password = ?", (username, password))
        role = cursor.fetchone()[0]
        if not role:
            role = 'Utilisateur'
        cursor.close()
        payload = {'username': username,'role': role, 'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return None


def verifyjwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

