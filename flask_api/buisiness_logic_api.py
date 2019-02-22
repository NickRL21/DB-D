import psycopg2


def _get_db_conn():
    try:
        # change to read password from file
        connect_str = "dbname='dbd_database' user='postgres' host='localhost' password='password'"
        conn = psycopg2.connect(connect_str)
        return conn
    except exception as e:
        print(e.__str__())
        return None


def _get_cursor(connection):
    try:
        cursor = connection.cursor()
    except exception as e:
        print(e.__str__())


def test_db():
    conn = _get_db_conn
    if conn is not None:
        cursor = _get_cursor
    else:
        assert False
    rows = cursor.execute("""SELECT * from Players""")
    print(rows)
    if len(rows) == 0:
        assert False
    else:
        assert True
