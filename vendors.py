# A small initial database of MAC OUI prefixes.
# In a production app, this could be loaded from an external API or a large JSON file.
OUI_DATABASE = {
    "1A:2B:3C": "Test Vendor / Mock",
    "8A:36:6C": "EFM Networks (ipTIME)",
    "00:14:22": "Dell Inc.",
    "00:1A:2B": "Cisco Systems",
    "00:50:56": "VMware, Inc.",
    "CC:46:D6": "Cisco Meraki",
    "F8:1A:67": "TP-Link",
    "D8:07:B6": "Apple, Inc.",
    "00:11:32": "Synology"
}

def get_vendor(bssid: str) -> str:
    """
    Takes a BSSID (MAC address) and returns the manufacturer name.
    If the OUI is not in the database, returns 'Unknown'.
    """
    if not bssid or len(bssid) < 8:
        return "Unknown"
    
    # Normalize the BSSID to uppercase and grab the first 8 characters (XX:XX:XX)
    oui = bssid.upper().replace("-", ":")[:8]
    
    return OUI_DATABASE.get(oui, "Unknown")
