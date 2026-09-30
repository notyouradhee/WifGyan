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
