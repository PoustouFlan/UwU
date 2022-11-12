import sqlite3

def connection():
    conn = sqlite3.connect("users.db")
    return conn

def init(conn):
    conn.execute(
        """
        CREATE TABLE USERS
        (
            ID          INT PRIMARY KEY     NOT NULL,
            TOTAL       INT,
            CORRECT     INT
        );
        """
    )
    conn.close()

def ajout_utilisateur(id, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    conn.execute(
        f"""
        INSERT INTO USERS (ID, TOTAL, CORRECT)
        VALUES ({id}, 0, 0)
        """
    )
    conn.commit()

    if to_close:
        conn.close()

def total(id, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    cursor = conn.execute(
        f"""
            SELECT ID, TOTAL from USERS where ID = {id}
        """
    )
    found = False
    for row in cursor:
        found = True
        value = row[1]
    if not found:
        ajout_utilisateur(id, conn)
        value = 0

    if to_close:
        conn.close()
    return value
    

def correct(id, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    cursor = conn.execute(
        f"""
            SELECT ID, CORRECT from USERS where ID = {id}
        """
    )

    found = False
    for row in cursor:
        found = True
        value = row[1]
        break
    if not found:
        ajout_utilisateur(id, conn)
        value = 0

    if to_close:
        conn.close()
    return row[1]

def increment_total(id, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    actual = total(id, conn)
    conn.execute(
        f"""
            UPDATE USERS set TOTAL = {actual+1} where ID = {id}
        """
    )
    conn.commit()

    if to_close:
        conn.close()

def increment_correct(id, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    actual = correct(id, conn)
    conn.execute(
        f"""
            UPDATE USERS set CORRECT = {actual+1} where ID = {id}
        """
    )
    conn.commit()

    if to_close:
        conn.close()