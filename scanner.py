import subprocess
from models import AccessPoint

def get_netsh_output() -> str:
    """Executes the Windows netsh command and returns the raw output."""
    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"], 
        capture_output=True, 
        text=True
    )
    return result.stdout

def parse_netsh_output(raw_text: str) -> list[AccessPoint]:
    """Parses raw netsh output into a list of structured AccessPoint objects."""
    lines = raw_text.split('\n')
    access_points = []
    
    current_ssid = ""
    current_network_type = ""
    current_authentication = ""
    current_encryption = ""
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        if clean_line.startswith("SSID"):
            parts = clean_line.split(":", 1)
            current_ssid = parts[1].strip() if len(parts) > 1 else ""
            
            # Reset network-level attributes for the new SSID
            current_network_type = ""
            current_authentication = ""
            current_encryption = ""

        elif clean_line.startswith("Network type"):
            current_network_type = clean_line.split(":", 1)[1].strip()
        elif clean_line.startswith("Authentication"):
            current_authentication = clean_line.split(":", 1)[1].strip()
        elif clean_line.startswith("Encryption"):
            current_encryption = clean_line.split(":", 1)[1].strip()

        elif clean_line.startswith("BSSID"):
            current_bssid = clean_line.split(":", 1)[1].strip()
            
            # Create a placeholder AccessPoint for this BSSID
            ap = AccessPoint(
                ssid=current_ssid,
                bssid=current_bssid,
                authentication=current_authentication,
                encryption=current_encryption,
                network_type=current_network_type,
                signal_percent=0,
                band="",
                channel=0,
                radio_type=""
            )
            access_points.append(ap)

        # Fill in BSSID-level attributes (applies to the most recently added AccessPoint)
        elif access_points and access_points[-1].bssid:
            last_ap = access_points[-1]
            if clean_line.startswith("Signal"):
                signal_str = clean_line.split(":", 1)[1].strip().replace('%', '')
                last_ap.signal_percent = int(signal_str) if signal_str.isdigit() else 0
            elif clean_line.startswith("Radio type"):
                last_ap.radio_type = clean_line.split(":", 1)[1].strip()
            elif clean_line.startswith("Band"):
                last_ap.band = clean_line.split(":", 1)[1].strip()
            elif clean_line.startswith("Channel"):
                channel_str = clean_line.split(":", 1)[1].strip()
                last_ap.channel = int(channel_str) if channel_str.isdigit() else 0

    return access_points

if __name__ == "__main__":
    raw_text = get_netsh_output()
    scanned_data = parse_netsh_output(raw_text)
    
    for ap in scanned_data:
        print(f"Network: {ap.ssid} ({ap.authentication})")
        print(f"  -> BSSID: {ap.bssid} | Signal: {ap.signal_percent}% ({ap.estimated_dbm} dBm) | Ch: {ap.channel} | Band: {ap.band}")
