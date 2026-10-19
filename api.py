from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import sqlite3
from database import DB_PATH
import scanner
import vendors

app = FastAPI(title="WifGyan API", description="Backend Dashboard for WifGyan")

STATIC_DIR = Path(__file__).parent / "static"

def classify_security(authentication: str, encryption: str) -> str:
    """Evaluates the authentication and encryption to determine a security classification."""
    auth = (authentication or "").upper()
    enc = (encryption or "").upper()
    
    if auth == "OPEN" or enc == "NONE":
        return "Insecure (Open Network)"
    elif "WEP" in auth or "WEP" in enc:
        return "Insecure (WEP)"
    elif auth == "WPA-PERSONAL" or enc == "TKIP":
        return "Weak (WPA/TKIP)"
    elif "WPA3" in auth:
        return "Highly Secure (WPA3)"
    elif "WPA2" in auth or "CCMP" in enc:
        return "Secure (WPA2)"
    elif "ENTERPRISE" in auth:
        return "Secure (Enterprise)"
    else:
        return "Unknown"

@app.get("/")
def serve_dashboard():
    """Serves the primary web dashboard UI."""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI file not found.")
    return FileResponse(index_file)

@app.get("/api/stats")
def get_stats():
    """Returns basic stats about our scanned networks."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            total = cursor.execute("SELECT COUNT(*) FROM networks").fetchone()[0]
            secure = cursor.execute("SELECT COUNT(*) FROM networks WHERE authentication LIKE '%WPA%'").fetchone()[0]
            insecure = cursor.execute("SELECT COUNT(*) FROM networks WHERE authentication = 'Open' OR authentication LIKE '%WEP%'").fetchone()[0]
            observations = cursor.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
        
        return {
            "total_networks": total,
            "secure_networks": secure,
            "insecure_networks": insecure,
            "total_observations": observations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/networks")
def get_networks():
    """Returns a list of all scanned networks joined with their latest signal observations."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Join networks with their latest observation from the observations table
            query = """
                SELECT 
                    n.bssid,
                    n.ssid,
                    n.authentication,
                    n.encryption,
                    n.band,
                    n.first_seen,
                    o.signal_percent,
                    o.channel,
                    o.timestamp as last_seen
                FROM networks n
                LEFT JOIN (
                    SELECT bssid, signal_percent, channel, timestamp
                    FROM observations
                    WHERE id IN (
                        SELECT MAX(id) FROM observations GROUP BY bssid
                    )
                ) o ON n.bssid = o.bssid
                ORDER BY o.signal_percent DESC, n.first_seen DESC
            """
            rows = cursor.execute(query).fetchall()
            
        networks = []
        for row in rows:
            data = dict(row)
            # Add calculated vendor and security classification
            data["vendor"] = vendors.get_vendor(data["bssid"])
            signal = data.get("signal_percent")
            data["estimated_dbm"] = ((signal // 2) - 100) if signal is not None else None
            data["security_status"] = classify_security(data.get("authentication", ""), data.get("encryption", ""))
            networks.append(data)
            
        return networks
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
        
        return {
            "status": "success",
            "message": f"Scanned and saved {len(access_points)} networks.",
            "count": len(access_points)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static assets directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
