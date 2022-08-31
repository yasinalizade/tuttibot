import psycopg2
import sys

from os import getenv


def composer_exists(cur, composer):
    cur.execute("INSERT INTO composers (composer) "
                "VALUES (%s) ON CONFLICT (composer) "
                "DO NOTHING", (composer,))
    cur.execute("SELECT id FROM composers WHERE composer = %s", (composer,))
    composer_id = cur.fetchone()
    return composer_id


def form_exists(cur, form_title):
    cur.execute("INSERT INTO forms (form) "
                "VALUES (%s) ON CONFLICT (form) "
                "DO NOTHING", (form_title,))
    cur.execute("SELECT id FROM forms WHERE form = %s", (form_title,))
    form_id = cur.fetchone()
    return form_id


def key_exists(cur, key):
    cur.execute("INSERT INTO keys (key) "
                "VALUES (%s) ON CONFLICT (key) "
                "DO NOTHING", (key,))
    cur.execute("SELECT id FROM keys WHERE key = %s", (key,))
    key_id = cur.fetchone()
    return key_id


def period_exists(cur, period):
    cur.execute("INSERT INTO periods (period) "
                "VALUES (%s) ON CONFLICT (period) "
                "DO NOTHING", (period,))
    cur.execute("SELECT id FROM periods WHERE period = %s", (period,))
    period_id = cur.fetchone()
    return period_id


def insert(piece: str, diff: str, time: str, comp: str,
           form: str, k: str, instr: str, per: str, file: str):
    con = None

    try:

        con = psycopg2.connect(
            host=getenv("HOST"),
            database=getenv("DATABASE"),
            user=getenv("USER"),
            password=getenv("PASSWORD")
        )

        cur = con.cursor()

        composer_id = composer_exists(cur, comp)
        form_id = form_exists(cur, form)
        key_id = key_exists(cur, k)
        period_id = period_exists(cur, per)

        cur.execute("INSERT INTO pieces (piece_title, file, difficulty, duration,"
                    "instruments, composer_id, form_id, key_id, period_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (piece, file, diff, time, instr, composer_id,
                     form_id, key_id, period_id))

        con.commit()

    except psycopg2.DatabaseError as e:

        print(f'Error {e}')
        sys.exit(1)

    finally:

        if con:
            con.close()
