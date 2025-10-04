#!/usr/bin/env python3

from argparse import ArgumentParser
import csv
import logging
from logging import FileHandler, Formatter, StreamHandler
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import sys
from sys import stderr


logger = logging.getLogger(__name__)


def main():

    parser = ArgumentParser()
    parser.add_argument("dbfile", metavar="DATABASE_FILE", type=str, help="sqlite database file")
    parser.add_argument("-p", "--purge", action="store_true", help="drop all tables at the beginning of the script")
    parser.add_argument("-d", "--drop", action="store_true", help="drop all tables at the end of the script")
    parser.add_argument("-o", "--order", dest="orders", action="append", help="file containing an order to be placed")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()
    init_logger(args.verbose)

    try:
        conn: Connection = sqlite3.connect(args.dbfile)
        conn.cursor().execute("PRAGMA foreign_keys = ON")
    except Exception as e:
        logger.error(e)
        logger.error("Failed to connect to {args.dbfile}")
        sys.exit(1)

    if args.purge:
        try:
            drop_tables(conn)
        except Exception as e:
            logger.error(e)
            logger.error("Failed to drop tables")
            sys.exit(1)

    try:
        create_tables(conn)
    except Exception as e:
        logger.error(e)
        logger.error("Failed to create tables")
        sys.exit(1)

    try:
        init_table_users(conn, Path("users.csv"))
    except Exception as e:
        logger.error(e)
        logger.error("Failed to initialize the users table")
        sys.exit(1)

    try:
        init_table_inventory(conn, Path("inventory.csv"))
    except Exception as e:
        logger.error(e)
        logger.error("Failed to initialize the inventory table")
        sys.exit(1)

    if args.orders:
        for order in args.orders:
            try:
                place_order(conn,  Path(order))
            except Exception as e:
                logger.error(e)
                logger.error(f"Failed to place order: {order}")
                continue

    if args.drop:
        try:
            drop_tables(conn)
        except Exception as e:
            logger.error(e)
            logger.error("Failed to drop tables")
            sys.exit(1)


def init_logger(level, log_file="db.log") -> None:
    """
    Configures the logger to print to stdout and sets the log level.

    Args:
        level (int): Level of verbosity, with 0 being the lowest and 3 the highest.

    Returns: None
    """

    formatter = Formatter("[%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d %(msg)s")
    handlers = [
        StreamHandler(sys.stdout),
        FileHandler(log_file)
    ]
    for handler in handlers:
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


def create_tables(conn) -> None:
    """
    Creates the `users`, `inventory`, `orders`, and `order_items` tables.

    Args:
        conn (Connection): database connection

    Returns: None
    """

    logger.info("Creating tables...")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logger.info("Created table: users")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
                cost REAL NOT NULL CHECK (cost > 0),
                name TEXT NOT NULL CHECK (length(name) < 256),
                category TEXT DEFAULT '' CHECK (length(category) < 32),
                description TEXT DEFAULT '' CHECK (length(description < 4096))
            )
        """)
        logger.info("Created table: inventory")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users
            )
        """)
        logger.info("Created table: orders")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items(
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER REFERENCES orders,
                item_no INTEGER,
                product_id INTEGER REFERENCES inventory,
                quantity INTEGER NOT NULL CHECK (quantity > 0)
            )
        """)
        logger.info("Created table: order_items")

        if logger.isEnabledFor(logging.DEBUG):
            cur = conn.execute("SELECT sql FROM sqlite_schema WHERE type = 'table' AND name <> 'sqlite_sequence'")
            schemas = cur.fetchall()
            for schema in schemas:
                logger.debug('\n\t    ' + schema[0])


def init_table_users(conn, fpath: Path) -> None:
    """
    Initializes the users table.

    Args:
        conn (Connection): database connection
        fpath (Path): csv file with initial users

    Returns: None
    """

    logger.info("Initializing table: users ...")
    if not fpath.exists():
        raise FileNotFoundError(fpath)
    if not fpath.is_file():
        raise FileNotFoundError(f"Not a file: {fpath}")

    with open(fpath, "r") as csv_handle:
        users = [tuple(user) for user in list(csv.reader(csv_handle))]

    with conn:
        conn.executemany("INSERT INTO users (username, email) VALUES (?, ?)", users)
        if logger.isEnabledFor(logging.DEBUG):
            cur = conn.execute("SELECT username, email FROM users")
            for user in cur.fetchall():
                logger.debug(f"[USER]> username: {user[0]}, email: {user[1]}")


def init_table_inventory(conn, fpath: Path) -> None:
    """
    Initializes the inventory table.

    Args:
        conn (Connection): database connection
        fpath (Path): csv file with initial inventory

    Returns: None
    """

    logger.info("Initializing table: inventory ...")
    if not fpath.exists():
        raise FileNotFoundError(fpath)
    if not fpath.is_file():
        raise FileNotFoundError(f"Not a file: {fpath}")

    with open(fpath, "r") as csv_handle:
        csv_reader = csv.DictReader(
            csv_handle,
            fieldnames=["quantity", "cost", "name", "category", "description"],
            quoting=csv.QUOTE_NONNUMERIC,
            skipinitialspace=True
        )
        items = [item for item in list(csv_reader)]
        for item in items:
            item["quantity"] = int(item["quantity"])

    with conn:
        conn.executemany("""
            INSERT INTO inventory (quantity, cost, name, category, description)
            VALUES (:quantity, :cost, :name, :category, :description)
        """,
        items)
        if logger.isEnabledFor(logging.DEBUG):
            cur = conn.execute("SELECT cost, name, category, description FROM inventory")
            for item in cur.fetchall():
                logger.debug(f"[ITEM]> cost: {item[0]}, name: {item[1]}, category: {item[2]}, description: {item[3]}")


def place_order(conn, fpath: Path):
    """
    Places an order.

    Args:
        conn (Connection): database connection
        fpath (Path): csv file with the order items

    Returns: None
    """
    if not fpath.exists():
        raise FileNotFoundError(fpath)
    if not fpath.is_file():
        raise FileNotFoundError(f"Not a file: {fpath}")


def drop_tables(conn):
    """
    Drops all tables in the database.

    Args:
        conn (Connection): database connection

    Returns: None
    """

    logger.info("Dropping tables...")
    with conn:
        tables = ["users", "inventory", "orders", "order_items"]
        for table in tables:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
            logger.debug(f"Dropped table: {table}")


if __name__ == "__main__":
    main()
