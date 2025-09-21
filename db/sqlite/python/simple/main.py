#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
from logging import Formatter, StreamHandler
import sqlite3
from sqlite3 import Connection
import sys
from sys import stderr


logger = logging.getLogger(__name__)


def main():

    parser = ArgumentParser()
    parser.add_argument("dbfile", metavar="DATABASE_FILE", type=str, help="sqlite database file")
    parser.add_argument("-d", "--drop", action="store_true", help="drop all tables at the end of the script")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()
    init_logger(args.verbose)

    try:
        conn: Connection = sqlite3.connect(args.dbfile)
        conn.cursor().execute("PRAGMA foreign_keys = ON")
    except Exception as e:
        print(e, file=stderr)
        print(f"ERROR: Failed to connect to {args.dbfile}", file=stderr)
        sys.exit(1)

    try:
        create_tables(conn)
    except Exception as e:
        print(e, file=stderr)
        print(f"ERROR: Failed to create tables")
        sys.exit(1)


def init_logger(level):
    handler = StreamHandler(sys.stdout)
    formatter = Formatter("[%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d %(msg)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    match level:
        case 0:
            logger.setLevel(logging.ERROR)
        case 1:
            logger.setLevel(logging.WARNING)
        case 2:
            logger.setLevel(logging.INFO)
        case _:
            logger.setLevel(logging.DEBUG)


def create_tables(conn):
    logger.info("Creating tables")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
                cost READ NOT NULL CHECK (cost > 0),
                name TEXT NOT NULL CHECK (length(name) < 256),
                category TEXT DEFAULT '' CHECK (length(category) < 32),
                description TEXT DEFAULT '' CHECK (length(description < 4096))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items(
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER REFERENCES orders,
                item_no INTEGER,
                product_id INTEGER REFERENCES inventory,
                quantity INTEGER NOT NULL CHECK (quantity > 0)
            )
        """)

    if logger.isEnabledFor(logging.DEBUG):
        cur = conn.cursor()
        cur.execute("SELECT sql FROM sqlite_schema WHERE type = 'table' AND name <> 'sqlite_sequence'")
        schemas = cur.fetchall()
        for schema in schemas:
            logger.debug('\n\t    ' + schema[0])


if __name__ == "__main__":
    main()
