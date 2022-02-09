import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    "DROP TABLE IF EXISTS USERS",
    "DROP TABLE IF EXISTS STOCK",
    "DROP TABLE IF EXISTS OWNERSHIP",
    """CREATE TABLE IF NOT EXISTS USERS(
        USERNAME    VARCHAR(30) NOT NULL UNIQUE,
        PASSWORD    VARCHAR(256) NOT NULL,
        PRIMARY KEY (USERNAME)
        )
    """,
    """CREATE TABLE IF NOT EXISTS STOCK(
        STOCKCODE     CHAR(10) NOT NULL UNIQUE,
        STOCKNAME     VARCHAR(100) NOT NULL,
        DETAIL        TEXT,
        CURRPRICE     NUMERIC(15,6),
        CHANGE        NUMERIC(15,6)
        )
    """,
    """CREATE TABLE IF NOT EXISTS OWNERSHIP(
        TRANSACTION_ID SERIAL,
        USERNAME    VARCHAR(30) NOT NULL REFERENCES USERS(USERNAME),
        STOCKCODE   CHAR(10) NOT NULL REFERENCES STOCK(STOCKCODE),
        QUANTITY    INTEGER,
        COST NUMERIC(15,6)
        )
    """,
]


def initialize(url):
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in INIT_STATEMENTS:
                cursor.execute(statement)
                print("done")
            cursor.close()
    except Exception as err:
        print("Error: ", err)


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
