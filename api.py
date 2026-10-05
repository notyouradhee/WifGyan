from fastapi import FastAPI, HTTPException
import sqlite3
from database import DB_PATH
import scanner

app = FastAPI(title="WifGyan API", description="Backend Dashboard for WifGyan")

@app.get("/api/stats")
def get_stats():
    """Returns basic stats about our scanned networks."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            total = cursor.execute("SELECT COUNT(*) FROM networks").fetchone()[0]
            secure = cursor.execute("SELECT COUNT(*) FROM networks WHERE authentication LIKE '%WPA%'").fetchone()[0]
            insecure = cursor.execute("SELECT COUNT(*) FROM networks WHERE authentication = 'Open' OR authentication LIKE '%WEP%'").fetchone()[0]
        
        return {
            "total_networks": total,
            "secure_networks": secure,
            "insecure_networks": insecure
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/networks")
def get_networks():
    """Returns a list of all historically scanned networks."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # This allows us to convert the SQL rows directly into JSON dictionaries
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM networks ORDER BY first_seen DESC").fetchall()
            
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan")
def trigger_scan():
    """Manually triggers a new Wi-Fi scan and saves it to the DB."""
    try:
        raw_text = scanner.get_netsh_output()
        access_points = scanner.parse_netsh_output(raw_text)
        
        # Save to db
        import database
        database.save_scan_results(access_points)
        
        return {"status": "success", "message": f"Scanned and saved {len(access_points)} networks."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
