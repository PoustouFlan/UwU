import sqlite3

def connection():
    conn = sqlite3.connect("users.db")
    return conn

def init(conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    conn.execute(
        """
        CREATE TABLE PAYS
        (
            ID          INT PRIMARY KEY     NOT NULL,
            TOTAL       INT                 NOT NULL,
            CORRECT     INT                 NOT NULL,
            SURVIE      INT                 NOT NULL,
            AVENTURE    INT                 NOT NULL,
            STREAK      INT                 NOT NULL,
            VIES        INT                 NOT NULL,
            START       INT                 NOT NULL
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE CAPITALES
        (
            ID          INT PRIMARY KEY     NOT NULL,
            TOTAL       INT                 NOT NULL,
            CORRECT     INT                 NOT NULL,
            SURVIE      INT                 NOT NULL,
            AVENTURE    INT                 NOT NULL,
            STREAK      INT                 NOT NULL,
            VIES        INT                 NOT NULL,
            START       INT                 NOT NULL
        );
        """
    )

    if to_close:
        conn.close()

def ajout_utilisateur(id, table, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    conn.execute(
        f"""
        INSERT INTO {table} (ID, TOTAL, CORRECT, SURVIE, AVENTURE, STREAK, VIES, START)
        VALUES ({id}, 0, 0, 0, 0, 0, 0, 1)
        """
    )
    conn.commit()

    if to_close:
        conn.close()

def donnees_pays(conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()
    
    cursor = conn.execute(
        """
            SELECT ID, TOTAL, CORRECT, SURVIE, AVENTURE from PAYS
        """
    )

    for row in cursor:
        yield {
            "id": row[0],
            "total": row[1],
            "correct": row[2],
            "survie": row[3],
            "aventure": row[4],
        }
    
    if to_close:
        conn.close()

def donnees_capitales(conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()
    
    cursor = conn.execute(
        """
            SELECT ID, TOTAL, CORRECT, SURVIE, AVENTURE from CAPITALES
        """
    )

    for row in cursor:
        yield {
            "id": row[0],
            "total": row[1],
            "correct": row[2],
            "survie": row[3],
            "aventure": row[4],
        }
    
    if to_close:
        conn.close()

def donnee(id, table, colonne, conn = None, default = 0):
    to_close = conn is None
    if to_close:
        conn = connection()

    cursor = conn.execute(
        f"""
            SELECT ID, {colonne} from {table} where ID = {id}
        """
    )
    found = False
    for row in cursor:
        found = True
        value = row[1]
    if not found:
        ajout_utilisateur(id, table, conn)
        value = default

    if to_close:
        conn.close()
    return value

def set_donnee(id, table, colonne, valeur, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    try:
        exist = conn.execute(f"SELECT {colonne} from {table} where ID = {id}").fetchone()
        if exist is None:
            ajout_utilisateur(id, table, conn)

        conn.execute(
            f"""
                UPDATE {table} set {colonne} = {valeur} where ID = {id}
            """
        )
        conn.commit()
    except Exception as e:
        print(e)

    if to_close:
        conn.close()

def increment_total(id, table, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    actual = donnee(id, table, "TOTAL", conn)
    set_donnee(id, table, "TOTAL", actual+1, conn)

    if to_close:
        conn.close()

def increment_correct(id, table, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    actual = donnee(id, table, "CORRECT", conn)
    set_donnee(id, table, "CORRECT", actual+1, conn)

    if to_close:
        conn.close()

def increment_streak(id, table, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    actual = donnee(id, table, "STREAK", conn)
    start = donnee(id, table, "START", conn)
    set_donnee(id, table, "STREAK", actual+1, conn)

    if start == 1:
        survie = donnee(id, table, "SURVIE", conn)
        if survie < actual + 1:
            set_donnee(id, table, "SURVIE", actual+1)

    elif start == 3:
        aventure = donnee(id, table, "AVENTURE", conn)
        if aventure < actual + 1:
            set_donnee(id, table, "AVENTURE", actual+1)

    if to_close:
        conn.close()

def decrement_vies(id, table, conn = None):
    to_close = conn is None
    if to_close:
        conn = connection()

    actual = donnee(id, table, "VIES", conn)
    set_donnee(id, table, "VIES", actual-1)

    if to_close:
        conn.close()