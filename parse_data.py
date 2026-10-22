"""Writes collected part, availability and price data into the SQLite database."""

import sqlite3

DB_PATH = "electronic_parts.db"


def insert_data(part_data):
    """Insert parts, availability and prices, skipping rows that already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for part in part_data:
        cursor.execute("SELECT COUNT(*) FROM Parts WHERE mpn = ?", (part["mpn"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """INSERT INTO Parts (mpn, keyword, part_id, part_name, manufacturer_name, manufacturer_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (part["mpn"], part["keyword"], part["part_id"], part["part_name"],
                 part["manufacturer_name"], part["manufacturer_id"]),
            )

        # The table name keeps its original spelling to match the existing database.
        cursor.execute(
            "INSERT INTO Availabilty (date, total_availability, mpn) VALUES (?, ?, ?)",
            (part["date"], part["total_availability"], part["mpn"]),
        )

        for seller in part["seller_data"]:
            company_name = seller.get("company_name", "Unknown")
            for price in seller.get("prices", []):
                # One price per company, quantity and day.
                cursor.execute(
                    "SELECT COUNT(*) FROM Prices WHERE company_name = ? AND quantity = ? AND date = ?",
                    (company_name, price["quantity"], part["date"]),
                )
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        """INSERT INTO Prices (date, keyword, company_name, quantity, currency, price,
                                               conversionRate, convertedCurrency, convertedPrice, mpn)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (part["date"], part["keyword"], company_name, price["quantity"],
                         price["currency"], price["price"], price["conversionRate"],
                         price["convertedCurrency"], price["convertedPrice"], part["mpn"]),
                    )

    conn.commit()
    conn.close()
    return "Data saved into database successfully"
