import jwt,datetime, mysql.connector, hashlib
import os

# JWT secret key
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'aopzoefj321'


# Database connection

SeverName = "159.8.122.152"
UserName = "datad02n_userpneu"
Password = "6A3AKayzuukD&j9eusK^"
DBName = "datad02n_data"
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL UNIQUE,
#     password VARCHAR(255) NOT NULL,
#     role ENUM('admin', 'user') NOT NULL
# );

mydb = mysql.connector.connect(
    host=SeverName,
    user=UserName,
    password=Password,
    database=DBName
    )

# JWT functions
def authen(username, password):
    try:
        if not username or not password:
            return None
        cursor = mydb.cursor()
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute("SELECT id from users WHERE name = %s AND password = %s", (username, password))
        id = cursor.fetchone()[0]
        cursor.close()
        cursor = mydb.cursor()
        cursor.execute("SELECT role from users WHERE name = %s AND password = %s", (username, password))
        role = cursor.fetchone()[0]
        cursor.close()
        payload = {'username': username,'role': role, 'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}
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

