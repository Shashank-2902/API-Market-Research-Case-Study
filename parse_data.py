import sqlite3

def insert_data(part_data):
    # print(part_data)
    conn = sqlite3.connect("electronic_parts.db")
    cursor = conn.cursor()

    for part in part_data:
        # Insert Part if not already present
        cursor.execute("SELECT COUNT(*) FROM Parts WHERE mpn = ?", (part["mpn"],))
        if cursor.fetchone()[0] == 0:  # If no record exists with this mpn
            cursor.execute("""
            INSERT INTO Parts (mpn, keyword, part_id, part_name, manufacturer_name, manufacturer_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (part["mpn"], part["keyword"], part["part_id"], part["part_name"], part["manufacturer_name"], part["manufacturer_id"]))

        # Total availabilty
        cursor.execute("""
            INSERT INTO Availabilty (date, total_availability, mpn)
            VALUES (?, ?, ?)
        """, (part["date"], part["total_availability"], part["mpn"]))

        # Insert Sellers and Prices, checking for duplicates based on company_name and quantity
        for seller in part["seller_data"]:
            company_name = seller.get("company_name", "Unknown")

            if "prices" in seller:
                for price_entry in seller["prices"]:
                    # Check if a record already exists with the same company_name and quantity
                    cursor.execute("""
                    SELECT COUNT(*) FROM Prices WHERE company_name = ? AND quantity = ? AND date = ?
                    """, (company_name, price_entry["quantity"], part["date"]))
                    if cursor.fetchone()[0] == 0:  # No duplicate price entry found
                        cursor.execute("""
                        INSERT INTO Prices (date, keyword, company_name, quantity, currency, price, conversionRate, convertedCurrency, convertedPrice, mpn)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (part["date"], part["keyword"], company_name, price_entry["quantity"], price_entry["currency"], price_entry["price"], 
                                price_entry["conversionRate"], price_entry["convertedCurrency"], price_entry["convertedPrice"], part["mpn"]))

    conn.commit()
    conn.close()
    return "Data saved into database successfully"
