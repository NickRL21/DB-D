import json
from flask_api import status
from flask import Flask
from database_helper import *
app = Flask(__name__)

@app.route('/player/<dci_number>')
def hello_world(dci_number):
    if str.isdigit(dci_number):
        conn = get_db_conn()
        cursor = get_cursor(conn)
        query = "SELECT * FROM Player WHERE (dci_number = %s)" % dci_number
        cursor.execute(query)
        return json.dumps({'statusCode': 200, 'body': cursor.fetchall()}), status.HTTP_200_OK
    else:
        return json.dumps({'body': 'invalid dci_number must be an int'}), status.HTTP_400_BAD_REQUEST
