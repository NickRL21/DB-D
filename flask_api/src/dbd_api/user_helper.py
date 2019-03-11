import psycopg2
from database_helper import Database

from passlib.apps import custom_app_context as pwd_context


def user_exists(dci_number):
    user_db = Database('dbd_creds')
    conn, cursor = user_db.get_db()
    cursor.execute("SELECT dci_number FROM users WHERE dci_number = %s", (int(dci_number),))
    user = cursor.fetchone()
    Database.close(conn, cursor)
    if user is not None:
        return True
    else:
        return False


def add_user(dci_number, password):
    hashed_pwd = hash(password)
    user_db = Database('dbd_creds')
    conn, cursor = user_db.get_db()
    try:
        cursor.execute("INSERT INTO users VALUES (%s, %s)", (int(dci_number), hashed_pwd,))
        cursor.execute("SELECT * FROM users WHERE dci_number = %s", (int(dci_number),))
        added = cursor.fetchone()
        # check to make sure that it was added properly
        if added[0] == dci_number:
            conn.commit()
            Database.close(conn, cursor)
            return True
        else:
            raise Exception('failed to add')
    except Exception as e:
        print(e.__str__())
        Database.close(conn, cursor)
        return False


def authenticate_user(dci_number, password):
    user_db = Database('dbd_creds')
    conn, cursor = user_db.get_db()
    cursor.execute("SELECT pwd_hash FROM users WHERE dci_number = %s", (int(dci_number),))
    hash = cursor.fetchone()
    Database.close(conn, cursor)
    if hash is not None:
        if verify(password, hash[0]):
            return True
        else:
            return False
    else:
        return False


def hash(password):
    return pwd_context.encrypt(password)


def verify(password, hash):
    return pwd_context.verify(password, hash)


a = authenticate_user(1422314756, 'password')
