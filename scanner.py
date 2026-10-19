import subprocess
import time
from models import AccessPoint
import database

def trigger_hardware_scan() -> None:
    """Forces the Windows Wi-Fi adapter to broadcast active 802.11 probe requests via wlanapi.dll."""
    try:
        import ctypes
        import ctypes.wintypes

        wlanapi = ctypes.windll.wlanapi
        client_handle = ctypes.wintypes.HANDLE()
        negotiated_version = ctypes.wintypes.DWORD()
        
        # Open handle to Windows WLAN service
        ret = wlanapi.WlanOpenHandle(2, None, ctypes.byref(negotiated_version), ctypes.byref(client_handle))
        if ret != 0:
            return

        class WLAN_INTERFACE_INFO(ctypes.Structure):
            _fields_ = [
                ('InterfaceGuid', ctypes.c_byte * 16),
                ('strInterfaceDescription', ctypes.c_wchar * 256),
                ('isState', ctypes.c_uint)
            ]

        class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
            _fields_ = [
                ('dwNumberOfItems', ctypes.wintypes.DWORD),
                ('dwIndex', ctypes.wintypes.DWORD),
                ('InterfaceInfo', WLAN_INTERFACE_INFO * 1)
            ]

        pInterfaceList = ctypes.POINTER(WLAN_INTERFACE_INFO_LIST)()
        ret = wlanapi.WlanEnumInterfaces(client_handle, None, ctypes.byref(pInterfaceList))
        if ret == 0 and pInterfaceList.contents.dwNumberOfItems > 0:
            guid = pInterfaceList.contents.InterfaceInfo[0].InterfaceGuid
            # Command physical adapter to actively scan all Wi-Fi channels
            wlanapi.WlanScan(client_handle, ctypes.byref(guid), None, None, None)
            time.sleep(2.5)  # Wait for radio responses

        wlanapi.WlanCloseHandle(client_handle, None)
    except Exception:
        pass

def get_netsh_output(active_scan: bool = True) -> str:
    """Executes an active probe scan and returns the raw netsh output."""
    if active_scan:
        trigger_hardware_scan()
        
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
    # Ensure the database tables are created before scanning
    database.init_db()
    
    raw_text = get_netsh_output()
    scanned_data = parse_netsh_output(raw_text)
    
    for ap in scanned_data:
        print(f"Network: {ap.ssid} | Security: {ap.security_status}")
        print(f"  -> BSSID: {ap.bssid} ({ap.vendor}) | Auth: {ap.authentication} | Enc: {ap.encryption}")
        print(f"  -> Signal: {ap.signal_percent}% ({ap.estimated_dbm} dBm) | Ch: {ap.channel} | Band: {ap.band}\n")

    # Save the parsed data to our SQLite database
    database.save_scan_results(scanned_data)
