# from flask_api import status
import logging
from flask import Flask, request, abort, jsonify, g
from flask_httpauth import HTTPBasicAuth
import psycopg2
import json
# for the life of me i can't get the deployed version to import the other files
# from dbd_api.database_helper import Database  # need to fix this import
# from dbd_api.user_helper import user_exists, authenticate_user, add_user

app = Flask(__name__)
auth = HTTPBasicAuth()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# this path is required for creds when flask is running./src/dbd_api/dbd_creds

# api is live at https://unthgdgw0h.execute-api.us-east-1.amazonaws.com/dev

##############################################
# resources to get started ask Nick for help #
##############################################

##############################
# help with database library #
##############################
# http://initd.org/psycopg/docs/usage.html

###########################
# Help with api framework #
###########################
# https://flask-restful.readthedocs.io/en/0.3.5/quickstart.html
# http://flask.pocoo.org/docs/1.0/

############################################
# Help with the serverless framework zappa #
############################################
# https://github.com/Miserlou/Zappa
# https://www.gun.io/blog/serverless-microservices-with-zappa-and-flask

# just for my reference

# https://github.com/Miserlou/Zappa#advanced-settings
DB_CREDENTIAL_PATH = './src/dbd_api/dbd_creds'
# for local testing
#DB_CREDENTIAL_PATH = 'dbd_creds'

@app.route('/')
@auth.login_required
def index():
    return "dbd_api v1.0", 200


@auth.verify_password
def verify_password(username, password):
    if user_exists(username):
        if authenticate_user(username, password):
            g.user = {'username': username}
            return True
        else:
            return False

    else:
        return False


@app.route('/register', methods=['POST'])
def register_user():
    body = request.json
    username = request.authorization.get('username')
    password = request.authorization.get('password')
    if username is None or password is None:
        return jsonify({'msg': 'ERROR: username or password missing'}), 400
    username = username.__str__()
    password = password.__str__()

    # get name enforce constraints
    name = body.get('name')
    if not name:
        return jsonify({'msg': 'ERROR: no name present'}), 400
    elif len(name) > 30:
        return jsonify({'msg': 'ERROR: name must be max of 30 characters'}), 400

    # enforce constraints on dci_number aka username
    if len(password) < 8:
        return jsonify({'msg': 'ERROR: password must be a minimum of 8 characters'}), 400

    if str.isdigit(username) and len(username) == 10:
        try:
            if user_exists(username):
                return jsonify({'msg': 'ERROR: user exists'}), 409
            elif add_user(username, password):
                insert_player(name, username)
                return jsonify({'msg': f'user: {username} created successfully'}), 200
            else:
                return jsonify({'msg': 'ERROR: user registration failed'}), 400
        except Exception as e:
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR: user registration failed'}), 500
    else:
        return jsonify({'msg': 'ERROR: username length must be 10 and must be a number'}), 400


# endpoint for getting player info
@app.route('/player', methods=['GET'])
@auth.login_required
def get_player():
    dci_number = g.user.get('username')
    db = Database(DB_CREDENTIAL_PATH)
    if request.method == 'GET':
        # get db conn
        try:
            conn, cursor = db.get_db()
            # execute query
            cursor.execute("SELECT * FROM Player WHERE (dci_number = %s)", (dci_number,))
            # build response
            resp = {'body': cursor.fetchall()}
            # close connections
            db.close(cursor, conn)
            return jsonify(resp), 200
        except Exception as e:
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR'}), 500


# endpoint for getting all characters for a player
@app.route('/character', methods=['GET'])
@auth.login_required
def characters():
    dci_number = g.user.get('username')
    db = Database(DB_CREDENTIAL_PATH)
    if request.method == 'GET':
        try:
            conn, cursor = db.get_db()
            # execute query
            cursor.execute("SELECT * FROM P_CHARACTER WHERE (dci_number = %s)", (dci_number,))
            # build response
            resp = {'body': cursor.fetchall()}
            # close connections
            db.close(cursor, conn)
            return jsonify(resp), 200
        except Exception as e:
            raise e
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR'}), 500


# endpoint for getting, adding, deleting, or updating a single player
@app.route('/character/<char_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def character(char_name):
    # enforce length constraint
    if not char_name:
        return jsonify({'msg': 'ERROR: character name cannot be null'}), 400
    if len(char_name) > 30:
        return jsonify({'msg': 'ERROR: character name too long, max 30 characters'}), 400

    dci_number = g.user.get('username')
    db = Database(DB_CREDENTIAL_PATH)
    if request.method == 'GET':
        try:
            # get db connection
            conn, cursor = db.get_db()
            # execute query
            cursor.execute("SELECT * FROM P_CHARACTER WHERE (dci_number = %s AND p_name = %s)", (dci_number, char_name,))
            # build response
            resp = {'body': cursor.fetchone()}
            # close connections
            db.close(cursor, conn)
            return jsonify(resp), 200
        except Exception as e:
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR'}), 500

    # create new character
    elif request.method == 'POST':
        try:
            body = request.json
            if body:
                if items_in_dict_not_greater_than(body, 30):
                    if body.get('level') > 20 or body.get('level') < 0:
                        return jsonify({'msg': 'ERROR: invalid level'}), 400
                    # get db connection
                    conn, cursor = db.get_db()
                    # insert character
                    cursor.execute("INSERT INTO P_CHARACTER(dci_number, p_name, race, class, background, level) VALUES(%s, %s, %s, %s, %s, %s)",
                                   (dci_number, char_name, body.get('race'), body.get('class'), body.get('background'), int(body.get('level'))))
                    # retrieve character
                    cursor.execute("SELECT * FROM P_CHARACTER WHERE (dci_number = %s AND p_name = %s)",
                                   (dci_number, char_name,))
                    # make sure it was retrieved
                    char = cursor.fetchone()
                    logger.info(char)
                    if char[0] != dci_number:
                        db.close(cursor, conn)
                        return jsonify({'msg': 'ERROR, item not added'}), 500
                    conn.commit()
                    # close connections
                    db.close(cursor, conn)
                    return jsonify({'character': char}), 201
                else:
                    return jsonify({'msg': 'ERROR: one or more items in body too long'}), 400
            else:
                return jsonify({'msg': 'ERROR: no body present'}), 400

        except Exception as e:
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR'}), 500
    # update character
    if request.method == 'PUT':
        try:
            body = request.json
            if body:
                if items_in_dict_not_greater_than(body, 30):
                    # get db connection
                    conn, cursor = db.get_db()
                    # get existing character
                    cursor.execute("SELECT * FROM P_CHARACTER WHERE (dci_number = %s AND p_name = %s)",
                                   (dci_number, char_name,))
                    char = cursor.fetchone()
                    logger.info(char)
                    # verify character exists
                    if not char:
                        db.close(cursor, conn)
                        return jsonify({'msg': f'ERROR, character with name: {char_name} does not exist'}), 400
                    # character schema (dci_number, p_name, race, class , background, level)
                    # update attributes that need updating
                    update_data = {}
                    if 'race' in body:
                        update_data['race'] = body.get('race')
                    else:
                        update_data['race'] = char[2]

                    if 'class' in body:
                        update_data['class'] = body.get('class')
                    else:
                        update_data['class'] = char[3]

                    if 'background' in body:
                        update_data['background'] = body.get('background')
                    else:
                        update_data['background'] = char[4]

                    if 'level' in body:
                        level = body.get('level')
                        if level > 20 or level < 0:
                            return jsonify({'msg': 'ERROR: invalid level'}), 400
                        update_data['level'] = level
                    else:
                        update_data['level'] = char[5]

                    # update database
                    cursor.execute("UPDATE P_CHARACTER SET race=%s, class=%s, background=%s, level=%s WHERE dci_number = %s and p_name = %s", (update_data['race'], update_data['class'], update_data['background'], update_data['level'], dci_number, char_name,))
                    conn.commit()
                    # close connections
                    db.close(cursor, conn)
                    return jsonify({'msg': f'SUCCESS: character {char_name} updated'}), 200
                else:
                    return jsonify({'msg': 'ERROR: one or more items in body too long'}), 400
            else:
                return jsonify({'msg': 'ERROR: no body present'}), 400

        except Exception as e:
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR'}), 500

    elif request.method == 'DELETE':
        return jsonify({'msg': 'ERROR: not implemented'}), 500


# endpoint for getting, adding, deleting, or updating magic items
@app.route('/magic_items/<char_name>', methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def magic_item(char_name):
    # enforce length constraint
    if not char_name:
        return jsonify({'msg': 'ERROR: character name cannot be null'}), 400
    if len(char_name) > 30:
        return jsonify({'msg': 'ERROR: character name too long, max 30 characters'}), 400

    dci_number = g.user.get('username')
    db = Database(DB_CREDENTIAL_PATH)
    if request.method == 'GET':
        try:
            # TODO check to see if character exists first for better error messages
            # get db connection
            conn, cursor = db.get_db()
            # execute query
            cursor.execute("SELECT * FROM MAGICAL_ITEM WHERE (dci_number = %s and character_name= %s)", (dci_number, char_name,))
            # build response
            resp = {'body': cursor.fetchone()}
            # close connections
            db.close(cursor, conn)
            return jsonify(resp), 200
        except Exception as e:
            logger.error(e.__str__())
            return jsonify({'msg': 'ERROR'}), 500

    if request.method == 'POST':
        try:
            body = request.json
            if body:
                if items_in_dict_not_greater_than(body, 30):
                    # get db connection
                    conn, cursor = db.get_db()
                    # insert magical item
                    cursor.execute("INSERT INTO Magical_item(dci_number, character_name, item_name, quantity, date_acquired) VALUES(%s, %s, %s, %s, %s)",
                                   (dci_number, char_name, body.get('item_name'), body.get('quantity'), body.get('date_acquired')))

                    # make sure it was retrieved
                    # retrieve character
                    cursor.execute("SELECT * FROM Magical_item WHERE (dci_number = %s AND character_name = %s AND item_name = %s)",
                                   (dci_number, char_name, body.get('item_name'),))
                    char = cursor.fetchone()
                    logger.info(char)
                    if char[0] != dci_number:
                        db.close(cursor, conn)
                        return jsonify({'msg': 'ERROR, item not added'}), 500
                    conn.commit()
                    # close connections
                    db.close(cursor, conn)
                    return jsonify({'character': char}), 201
                else:
                    return jsonify({'msg': 'ERROR: one or more items in body too long'}), 400
            else:
                return jsonify({'msg': 'ERROR: no body present'}), 400
        except Exception as e:
            logger.error(e.__str__())
            raise e
            return jsonify({'msg': 'ERROR'}), 500


def insert_player(name, dci_number):
    db = Database(DB_CREDENTIAL_PATH)
    conn, cursor = db.get_db()
    cursor.execute("INSERT INTO player(dci_number, p_name) VALUES (%s, %s)", (dci_number, name))
    # query item just inserted
    cursor.execute("SELECT * FROM player WHERE (dci_number = %s)", (dci_number,))
    # grab item just queried
    added = cursor.fetchone()
    # check to make sure that it was added properly
    if added[1] == name and added[0] == dci_number:
        # if so commit changes to database so that they persist
        conn.commit()
        db.close(conn, cursor)
        return True
    else:
        db.close(conn, cursor)
        return False


def items_in_dict_not_greater_than(input_dict, length):
    for k, v in input_dict.items():
        if isinstance(v, str):
            if len(v) > length:
                return False
    return True


# app will run when this file is run
if __name__ == '__main__':
    app.run(debug=True)

# TODO
# login (dci_number, password)
# 401 for wrong password
# 404 for not registered
# 200 for successful login

# TODO register(dci_number, name, password)


# helper methods unfortunatly these have to be in this file right now
# i cant get lambda to import the helper files

######################
# user login helper methods
######################
from passlib.apps import custom_app_context as pwd_context


def user_exists(dci_number):
    user_db = Database(DB_CREDENTIAL_PATH)
    conn, cursor = user_db.get_db()
    cursor.execute("SELECT dci_number FROM users WHERE dci_number = %s", (dci_number,))
    user = cursor.fetchone()
    Database.close(conn, cursor)
    if user is not None:
        return True
    else:
        return False


def add_user(dci_number, password):
    hashed_pwd = hash(password)
    user_db = Database(DB_CREDENTIAL_PATH)
    conn, cursor = user_db.get_db()
    try:
        cursor.execute("INSERT INTO users VALUES (%s, %s)", (dci_number, hashed_pwd,))
        cursor.execute("SELECT * FROM users WHERE dci_number = %s", (dci_number,))
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
    user_db = Database(DB_CREDENTIAL_PATH)
    conn, cursor = user_db.get_db()
    cursor.execute("SELECT pwd_hash FROM users WHERE dci_number = %s", (dci_number,))
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


###################
# database helper
###################

class Database:
    def __init__(self, credential_path):
        lines = ''
        with open(credential_path, 'r') as creds:
            for line in creds.readlines():
                lines += line
        self._credentials = json.loads(lines)

    def get_db_conn(self):
        try:
            # change to read password from file
            connect_str = f"dbname='{self._credentials.get('dbname')}' user='{self._credentials.get('user')}' host='{self._credentials.get('host')}' password='{self._credentials.get('password')}'"
            conn = psycopg2.connect(connect_str)
            return conn
        except Exception as e:
            print(e.__str__())
            return None

    @staticmethod
    def get_cursor(connection):
        try:
            return connection.cursor()
        except Exception as e:
            print(e.__str__())

    def get_db(self):
        conn = self.get_db_conn()
        cursor = self.get_cursor(conn)
        return conn, cursor

    @staticmethod
    def close(cursor, conn):
        cursor.close()
        conn.close()
