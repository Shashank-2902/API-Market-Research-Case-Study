import sqlite3

def create_database():
    conn = sqlite3.connect("electronic_parts.db")
    cursor = conn.cursor()

    # Create Parts Table
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

    # Create Prices Table
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
        FOREIGN KEY (mpn) REFERENCES Sellers(mpn)
    )
    """)

    #Create Availabilty Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Availabilty (
       
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        date TEXT,     
        total_availability INTEGER,
        mpn TEXT,
        FOREIGN KEY (mpn) REFERENCES Sellers(mpn)
    )
    """)


    conn.commit()
    conn.close()

create_database()