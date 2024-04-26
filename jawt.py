import jwt,datetime,hashlib,pyodbc
import os

# JWT secret key
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'aopzoefj321'


# Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=196.115.7.4,1433;DATABASE=ASZPROD;UID=sa;PWD=90901504Data;Encrypt=no;TrustServerCertificate=yes;MARS_Connection=Yes;MultipleActiveResultSets=True;')

# CREATE TABLE login_hist (
#   ID int NOT NULL,
#   IDUSER int NOT NULL,
#   LOGINDATTIM datetime NOT NULL DEFAULT GETDATE(),
#   IP varchar(255) NOT NULL,
#   PREVLOG datetime NULL
# )


# JWT functions
def authen(username, password, ip):
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
        cursor.execute("SELECT actif from users WHERE name = ? AND password = ?", (username, password))
        statut = cursor.fetchone()[0]
        if statut == 0:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT role from users WHERE name = ? AND password = ?", (username, password))
        role = cursor.fetchone()[0]
        if not role:
            role = 'Utilisateur'
        cursor = conn.cursor()
        cursor.execute("SELECT CO_NO from users WHERE name = ? AND password = ?", (username, password))
        co_no = cursor.fetchone()[0]
        if not co_no:
            co_no = 0
        cursor.close()
        payload = {'username': username,'role': role, 'id': id, 'co_no': co_no, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        login_hist(id, ip, get_last_login(id))
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




def login_hist(userid, ip, prevlogin):
    try:
        print(userid, ip, prevlogin)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_hist (iduser, ip, prevlog) VALUES (?, ?, ?)", (userid, ip, prevlogin))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_last_login(userid):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 LOGINDATTIM FROM login_hist WHERE IDUSER = ? ORDER BY LOGINDATTIM DESC", (userid))
        last_login = cursor.fetchone()[0]
        cursor.close()
        return last_login
    except Exception as e:
        print(e)
        return datetime.datetime(1970, 1, 1, 0, 0, 0)