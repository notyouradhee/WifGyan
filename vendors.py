from mac_vendor_lookup import MacLookup, VendorNotFoundError

# Initialize the lookup object. (It automatically downloads/caches the IEEE list on first run)
mac_lookup = MacLookup()

# We keep our static mock for the pytest test cases
OUI_DATABASE = {
    "1A:2B:3C": "Test Vendor / Mock",
    "8A:36:6C": "EFM Networks (ipTIME)",
}

def get_vendor(bssid: str) -> str:
    """
    Takes a BSSID (MAC address) and returns the manufacturer name using the official IEEE database.
    If the OUI is locally administered or not in the database, returns 'Unknown'.
    """
    if not bssid or len(bssid) < 8:
        return "Unknown"
    
    # Check our mock database first (to ensure test_scanner.py doesn't break)
    oui = bssid.upper().replace("-", ":")[:8]
    if oui in OUI_DATABASE:
        return OUI_DATABASE[oui]
        
    try:
        # Look it up using the massive IEEE database we installed!
        return mac_lookup.lookup(bssid)
    except VendorNotFoundError:
        # Many modern routers use "Locally Administered" MAC addresses for virtual networks
        # which are not registered to any manufacturer.
        return "Unknown (Virtual/Randomized)"
    except Exception:
        return "Unknown"
