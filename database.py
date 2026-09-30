import sqlite3
from pathlib import Path

# We store the database file right next to this script
DB_PATH = Path(__file__).parent / "wifgyan.sqlite3"

def init_db():
    """
    Connects to the SQLite database (creating the file if it doesn't exist)
    and sets up our initial tables for saving scan data.
    """
    # The 'with' statement ensures the connection closes automatically when we're done
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # TABLE 1: 'networks'
        # This stores the core identity of the Access Point. 
        # BSSID (the MAC address) is the Primary Key because it is unique to each router.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS networks (
                bssid TEXT PRIMARY KEY,
                ssid TEXT,
                authentication TEXT,
                encryption TEXT,
                band TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # TABLE 2: 'observations'
        # This tracks the signal over time. Every time we scan, we add a new row here.
        # This will let us build those historical signal graphs later!
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT,
                signal_percent INTEGER,
                channel INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(bssid) REFERENCES networks(bssid)
            )
        """)
        
        conn.commit()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
