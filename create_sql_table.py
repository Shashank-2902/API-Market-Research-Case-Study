"""Creates the SQLite database and its tables. Run once before main.py."""

import sqlite3

DB_PATH = "electronic_parts.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parts (
        mpn TEXT PRIMARY KEY,
        keyword TEXT,
        part_id TEXT,
        part_name TEXT,
        manufacturer_name TEXT,
        manufacturer_id TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Prices (
        price_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        keyword TEXT,
        company_name TEXT,
        quantity INTEGER,
        currency TEXT,
        price REAL,
        conversionRate REAL,
        convertedCurrency TEXT,
        convertedPrice REAL,
        mpn TEXT,
        FOREIGN KEY (mpn) REFERENCES Parts(mpn)
    )
    """)

    # The table name keeps its original spelling to match the existing database.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Availabilty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        total_availability INTEGER,
        mpn TEXT,
        FOREIGN KEY (mpn) REFERENCES Parts(mpn)
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
