# from flask_api import status
from flask import Flask, request, abort, jsonify
# from flask_restful import reqparse, Api, Resource
from database_helper import Database  # need to fix this import
from user_helper import user_exists, authenticate_user, add_user

app = Flask(__name__)

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


@app.route('/')
def index():
    return "Hello, world!", 200


@app.route('/register', methods=['POST'])
def register_user():
    body = request.json
    username = request.authorization.get('username')
    password = request.authorization.get('password')
    if username is None or password is None:
        username = body.get('username')
        password = body.get('password')
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
            raise e
            return jsonify({'msg': 'ERROR: user registration failed'}), 500
    else:
        return jsonify({'msg': 'ERROR: username length must be 10 and must be a number'}), 400


@app.route('/player/<dci_number>', methods=['GET'])
def get_player(dci_number):
    db = Database('./src/dbd_api/dbd_creds')
    if request.method == 'GET':
        # get db conn
        if str.isdigit(dci_number) and len(dci_number) == 10:
            try:
                conn, cursor = db.get_db()
                # execute query
                cursor.execute("SELECT * FROM Player WHERE (dci_number = %s)", (dci_number,))
                # build response
                resp = {'body': cursor.fetchall()}
                # close connections
                db.close(cursor, conn)
                return jsonify(resp), 200
            except:
                return jsonify({'msg': 'ERROR'}), 500

        else:
            return jsonify({'msg': 'ERROR: username length must be 10 and must be a number'}), 400


def insert_player(name, dci_number):
    db = Database('./src/dbd_api/dbd_creds')
    conn, cursor = db.get_db()
    cursor.execute("INSERT INTO player(dci_number, p_name) VALUES (%s, %s)", (dci_number, name))
    # query item just inserted
    cursor.execute("SELECT * FROM player WHERE (dci_number = %s)", (dci_number,))
    # gram item just queried
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


# TODO need to look into how to prevent sql injection in body


# app will run when this file is run
if __name__ == '__main__':
    app.run(debug=True)

# TODO
# login (dci_number, password)
# 401 for wrong password
# 404 for not registered
# 200 for successful login

# TODO register(dci_number, name, password)
