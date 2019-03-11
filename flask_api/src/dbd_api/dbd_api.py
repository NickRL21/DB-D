from flask_api import status
import flask
from flask_restful import reqparse, Api, Resource
from database_helper import Database  # need to fix this import
app = flask.Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('name')


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


@app.route('/player/<dci_number>', methods=['GET', 'POST'])
def get(dci_number):
    db = Database('dbd_creds')
    if flask.request.method == 'GET':
        # make sure dci_number is an int for safety
        if str.isdigit(dci_number):
            dci_number = int(dci_number)
            # get db conn
            conn, cursor = db.get_db()
            # execute query
            cursor.execute("SELECT * FROM Player WHERE (dci_number = %s)", (dci_number,))
            # build response
            resp = {'body': cursor.fetchall()}
            # close connections
            db.close(cursor, conn)
            # return response and status code
            return flask.jsonify(resp), status.HTTP_200_OK
        else:
            return flask.jsonify({'body': 'invalid dci_number must be an int'}), status.HTTP_400_BAD_REQUEST
    else:
        args = parser.parse_args()
        name = args.get('name')
        if str.isdigit(dci_number):
            dci_number = int(dci_number)
            if name:
                # get db conn and cursor
                conn, cursor = db.get_db()
                # execute insert
                cursor.execute("INSERT INTO player(dci_number, name) VALUES (%s, %s)", (dci_number, name))
                # query item just inserted
                cursor.execute("SELECT * FROM player WHERE dci_number = %s", (dci_number,))
                # gram item just queried
                added = cursor.fetchone()
                # check to make sure that it was added properly
                if added[1] == name and added[0] == dci_number:
                    # if so commit changes to database so that they persist
                    conn.commit()
                    # close the connections
                    db.close(cursor, conn)
                    return flask.jsonify({'status': 'success'})
                else:
                    db.close(cursor, conn)
                    return flask.jsonify({"status": "error: not added"}), status.HTTP_400_BAD_REQUEST
                pass

            else:
                return flask.jsonify({"status": "error: no name"}), status.HTTP_400_BAD_REQUEST
        else:
            return flask.jsonify({'body': 'invalid dci_number must be an int'}), status.HTTP_400_BAD_REQUEST


# TODO need to look into how to prevent sql injection in body


# app will run when this file is run
if __name__ == '__main__':
    app.run(debug=True)



