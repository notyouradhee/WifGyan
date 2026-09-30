import subprocess

def scan_networks():
    """
    Executes the Windows netsh command and parses the output into structured data.
    """
    # 1. Execute the command and capture the output
    # capture_output=True grabs the text instead of printing it to the console
    # text=True decodes the raw bytes into a standard Python string
    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"], 
        capture_output=True, 
        text=True
    )
    
    lines = result.stdout.split('\n')
    
    networks = []
    current_network = None
    current_bssid = None

    # 2. Iterate through each line to build our data structure
    for line in lines:
        # Remove leading/trailing whitespace to easily match keywords
        clean_line = line.strip()
        
        # Ignore empty lines
        if not clean_line:
            continue

        # Detect a new SSID block
        if clean_line.startswith("SSID"):
            # If we were already building a network, save it before starting the new one
            if current_network:
                if current_bssid:
                    current_network['bssids'].append(current_bssid)
                networks.append(current_network)
            
            # Extract the network name (everything after the first colon)
            ssid_name = clean_line.split(":", 1)[1].strip()
            current_network = {
                "ssid": ssid_name,
                "authentication": "",
                "encryption": "",
                "bssids": []
            }
            current_bssid = None  # Reset BSSID for the new network

        # Parse Network-level attributes
        elif clean_line.startswith("Authentication") and current_network:
            current_network["authentication"] = clean_line.split(":", 1)[1].strip()
        elif clean_line.startswith("Encryption") and current_network:
            current_network["encryption"] = clean_line.split(":", 1)[1].strip()

        # Detect a new BSSID block under the current network
        elif clean_line.startswith("BSSID") and current_network:
            # If we were already building a BSSID, save it to the current network's list
            if current_bssid:
                current_network['bssids'].append(current_bssid)
            
            mac_address = clean_line.split(":", 1)[1].strip()
            current_bssid = {
                "mac": mac_address,
                "signal": "",
                "radio_type": "",
                "band": "",
                "channel": ""
            }

        # Parse BSSID-level attributes
        elif current_bssid:
            if clean_line.startswith("Signal"):
                current_bssid["signal"] = clean_line.split(":", 1)[1].strip()
            elif clean_line.startswith("Radio type"):
                current_bssid["radio_type"] = clean_line.split(":", 1)[1].strip()
            elif clean_line.startswith("Band"):
                current_bssid["band"] = clean_line.split(":", 1)[1].strip()
            elif clean_line.startswith("Channel"):
                current_bssid["channel"] = clean_line.split(":", 1)[1].strip()

    # 3. Save the very last network and BSSID being processed when the loop ends
    if current_network:
        if current_bssid:
            current_network['bssids'].append(current_bssid)
        networks.append(current_network)

    return networks

# Run the function and print the structured data
if __name__ == "__main__":
    scanned_data = scan_networks()
    
    # Print the data in a readable format
    for net in scanned_data:
        print(f"\nNetwork: {net['ssid']} ({net['authentication']})")
        for bssid in net['bssids']:
            print(f"  -> AP MAC: {bssid['mac']} | Signal: {bssid['signal']} | Ch: {bssid['channel']} | Band: {bssid['band']}")
