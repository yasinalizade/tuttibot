import psycopg2

from dotenv import load_dotenv
from os import getenv

load_dotenv()

con = psycopg2.connect(
    host=getenv("HOST"),
    database=getenv("DATABASE"),
    user=getenv("USER"),
    password=getenv("PASSWORD")
)

cur = con.cursor()

cur.execute("CREATE TABLE composers"
            "(id SERIAL PRIMARY KEY,"
            "composer VARCHAR,"
            "CONSTRAINT constraint_name UNIQUE (composer));")

cur.execute("CREATE TABLE forms"
            "(id SERIAL PRIMARY KEY,"
            "form VARCHAR,"
            "CONSTRAINT constraint_name1 UNIQUE (form));")

cur.execute("CREATE TABLE keys"
            "(id SERIAL PRIMARY KEY,"
            "key VARCHAR,"
            "CONSTRAINT constraint_name2 UNIQUE (key));")

cur.execute("CREATE TABLE periods"
            "(id SERIAL PRIMARY KEY,"
            "period VARCHAR,"
            "CONSTRAINT constraint_name4 UNIQUE (period));")

cur.execute("CREATE TABLE pieces"
            "(id SERIAL PRIMARY KEY,"
            "piece_title VARCHAR,"
            "file VARCHAR,"
            "difficulty VARCHAR,"
            "duration VARCHAR,"
            "instruments VARCHAR,"
            "composer_id INTEGER NOT NULL,"
            "form_id INTEGER NOT NULL,"
            "key_id INTEGER NOT NULL,"
            "period_id INTEGER NOT NULL,"
            "FOREIGN KEY (composer_id) REFERENCES composers (id),"
            "FOREIGN KEY (form_id) REFERENCES forms (id),"
            "FOREIGN KEY (key_id) REFERENCES keys (id),"
            "FOREIGN KEY (period_id) REFERENCES periods (id), "
            "CONSTRAINT constraint_name5 UNIQUE (piece_title, file));")

con.commit()

cur.close()
con.close()
