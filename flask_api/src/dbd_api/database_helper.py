# by Nicholas lewis
# helper to make using psycopg2 a little easier
# https://linuxize.com/post/how-to-install-postgresql-on-ubuntu-18-04/
import json

import psycopg2


class Database:
    def __init__(self, credential_path):
        lines = ''
        with open (credential_path, 'r') as creds:
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

    def close(self, cursor, conn):
        cursor.close()
        conn.close()


def __test_db():
    db = Database('dbd_creds')
    conn, cursor = db.get_db()
    assert conn is not None
    assert cursor is not None
    cursor.execute("SELECT * FROM Player;")
    rows = cursor.fetchall()
    assert len(rows) > 0
    cursor.close()
    conn.close()
    print(rows)

