import psycopg2


def _get_db_conn():
    try:
        # change to read password from file
        connect_str = "dbname='dbd_database' user='postgres' host='localhost' password='password'"
        conn = psycopg2.connect(connect_str)
        return conn
    except Exception as e:
        print(e.__str__())
        return None


def _get_cursor(connection):
    try:
        return connection.cursor()
    except Exception as e:
        print(e.__str__())


def test_db():
    conn = _get_db_conn()
    assert conn is not None
    cursor = _get_cursor(conn)
    assert cursor is not None
    cursor.execute("SELECT * FROM Player;")
    rows = cursor.fetchall()
    assert len(rows) > 0
    cursor.close()
    conn.close()
    print(rows)
