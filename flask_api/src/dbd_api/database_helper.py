# by Nicholas lewis
# helper to make using psycopg2 a little easier
# https://linuxize.com/post/how-to-install-postgresql-on-ubuntu-18-04/

import psycopg2


def get_db_conn():
    try:
        # change to read password from file
        connect_str = "dbname='dbd_database' user='postgres' host='ec2-3-87-207-3.compute-1.amazonaws.com' password='password'"
        conn = psycopg2.connect(connect_str)
        return conn
    except Exception as e:
        print(e.__str__())
        return None


def get_cursor(connection):
    try:
        return connection.cursor()
    except Exception as e:
        print(e.__str__())


def get_db():
    conn = get_db_conn()
    cursor = get_cursor(conn)
    return conn, cursor


def close(cursor, conn):
    cursor.close()
    conn.close()


def test_db():
    conn = get_db_conn()
    assert conn is not None
    cursor = get_cursor(conn)
    assert cursor is not None
    cursor.execute("SELECT * FROM Player;")
    rows = cursor.fetchall()
    assert len(rows) > 0
    cursor.close()
    conn.close()
    print(rows)
