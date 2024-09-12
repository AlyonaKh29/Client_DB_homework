import psycopg2
from psycopg2.sql import SQL, Identifier


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES client(client_id),
            number VARCHAR(20) UNIQUE
            );
        """)
    conn.commit()


def insert_client(conn, f_name, l_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client (first_name, last_name, email)
        VALUES (%s, %s, %s);
        """, (f_name, l_name, email))
    conn.commit()


def insert_phone(conn, id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_number (client_id, number)
        VALUES (%s, %s);
        """, (id, phone))
    conn.commit()


def get_client_id(conn, f_name, l_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT client_id
        FROM client
        WHERE first_name=%s AND last_name=%s AND email=%s;
        """, (f_name, l_name, email))
        result = cur.fetchone()
    return result[0]


def change_client(conn, id, f_name=None, l_name=None, email=None):
    arg_list = {'first_name': f_name, 'last_name': l_name, 'email': email}
    for key, arg in arg_list.items():
        if arg:
            with conn.cursor() as cur:
                cur.execute(SQL("""
                UPDATE client
                SET {}=%s
                WHERE client_id=%s;
                """).format(Identifier(key)), (arg, id))
            conn.commit()


def delete_phone(conn, id, number):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id=%s AND number=%s;
        """, (id, number))
    conn.commit()


def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client
        WHERE client_id=%s;
        """, (id,))
    conn.commit()


def find_client(conn, f_name=None, l_name=None, email=None, number=None):
    arg_list = {'first_name': f_name, 'last_name': l_name, 'email': email, 'number': number}
    for key, arg in arg_list.items():
        if arg:
            with conn.cursor() as cur:
                cur.execute(SQL("""
                SELECT c.first_name, c.last_name, c.email, p.number FROM client c
                LEFT JOIN phone_number p ON c.client_id = p.client_id
                WHERE {}=%s;
                """).format(Identifier(key)), (arg,))
                result = cur.fetchall()
    return result


