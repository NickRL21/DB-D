import json
from flask_api import status
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from database_helper import *
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('name')


# class for resource group
class Player(Resource):
    # get player based on dci
    def get(self, dci_number):
        # make sure dci_number is an int for safety
        if str.isdigit(dci_number):
            dci_number = int(dci_number)
            # get db conn
            conn, cursor = get_db()
            # execute query
            cursor.execute("SELECT * FROM Player WHERE (dci_number = %s)", (dci_number,))
            # build response 
            resp = {'body': cursor.fetchall()}
            # close connections
            close(cursor, conn)
            return resp, status.HTTP_200_OK
        else:
            return {'body': 'invalid dci_number must be an int'}, status.HTTP_400_BAD_REQUEST

# TODO need to look into how to prevent sql injection in body
    def post(self, dci_number):
        args = parser.parse_args()
        name = args.get('name')
        if str.isdigit(dci_number):
            dci_number = int(dci_number)
            if name:
                # get db conn and cursor
                conn, cursor = get_db()
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
                    close(cursor, conn)
                    return {'status': 'success'}
                else:
                    close(cursor, conn)
                    return {"status": "error: not added"}, status.HTTP_400_BAD_REQUEST
                pass

            else:
                return {"status": "error: no name"}, status.HTTP_400_BAD_REQUEST
        else:
            return {'body': 'invalid dci_number must be an int'}, status.HTTP_400_BAD_REQUEST


# add resource and url
api.add_resource(Player, '/player/<dci_number>')

if __name__ == '__main__':
    app.run(debug=True)



