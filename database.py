import sqlite3
from pathlib import Path
from typing import List
from models import AccessPoint

# We store the database file right next to this script
DB_PATH = Path(__file__).parent / "wifgyan.sqlite3"

def save_scan_results(access_points: List[AccessPoint]):
    """
    Saves a list of AccessPoint objects into the database.
    Updates the networks table if it's a new network,
    and always adds a new row to the observations table.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        for ap in access_points:
            # 1. Insert or Ignore into 'networks'
            # We use INSERT OR IGNORE because the BSSID is the primary key.
            # If the router is already in the database, it won't crash; it just skips this step.
            cursor.execute("""
                INSERT OR IGNORE INTO networks (bssid, ssid, authentication, encryption, band)
                VALUES (?, ?, ?, ?, ?)
            """, (ap.bssid, ap.ssid, ap.authentication, ap.encryption, ap.band))
            
            # 2. Insert into 'observations'
            # We always want a new row here to track the signal strength at this exact moment in time.
            cursor.execute("""
                INSERT INTO observations (bssid, signal_percent, channel)
                VALUES (?, ?, ?)
            """, (ap.bssid, ap.signal_percent, ap.channel))
            
        conn.commit()
        print(f"Successfully saved {len(access_points)} Access Points to the database.")

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
