from dataclasses import dataclass

@dataclass
class AccessPoint:
    ssid: str
    bssid: str
    authentication: str
    encryption: str
    signal_percent: int
    band: str
    channel: int
    network_type: str = ""
    radio_type: str = ""
    
    @property
    def estimated_dbm(self) -> int:
        """Derive an estimated dBm from signal percentage: (percent / 2) - 100"""
        return (self.signal_percent // 2) - 100

    @property
    def security_status(self) -> str:
        """Evaluates the authentication and encryption to determine a security classification."""
        auth = self.authentication.upper()
        enc = self.encryption.upper()
        
        if auth == "OPEN" or enc == "NONE":
            return "Insecure (Open Network)"
        elif "WEP" in auth or "WEP" in enc:
            return "Insecure (WEP is easily cracked)"
        elif auth == "WPA-PERSONAL" or enc == "TKIP":
            return "Weak (WPA/TKIP is outdated)"
        elif "WPA3" in auth:
            return "Highly Secure (WPA3)"
        elif "WPA2" in auth or "CCMP" in enc:
            return "Secure (WPA2)"
        elif "ENTERPRISE" in auth:
            return "Secure (Enterprise)"
        else:
            return "Unknown"
