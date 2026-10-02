from scapy.all import rdpcap, Dot11, EAPOL, Dot11Deauth, Dot11Elt
import sys
from pathlib import Path
from datetime import datetime

def extract_bssid(pkt) -> str:
    """Safely extracts the BSSID from a packet if available."""
    if hasattr(pkt, "addr3") and pkt.addr3:
        return pkt.addr3
    elif hasattr(pkt, "addr2") and pkt.addr2:
        return pkt.addr2
    return "Unknown"

def analyze_pcap(file_path: str):
    """
    Reads a .pcap file and counts the types of 802.11 Wi-Fi frames,
    detects security events, and builds a timeline with BSSID mapping.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Could not find file {file_path}")
        return

    print(f"Loading {path.name}... (This might take a moment for large files)")
    packets = rdpcap(str(path))
    
    total_packets = len(packets)
    management_frames = 0
    control_frames = 0
    data_frames = 0
    other_frames = 0
    
    # Timeline to track WHO and WHEN
    events_timeline = []
    
    print(f"Successfully loaded {total_packets} packets.")
    print("Analyzing packets for security events...")
    
    for pkt in packets:
        # Determine human-readable timestamp
        # Scapy packet times are usually float unix timestamps
        pkt_time = datetime.fromtimestamp(float(pkt.time)).strftime('%H:%M:%S') if pkt.time else "Unknown"
        bssid = extract_bssid(pkt)

        # 1. Check for WPA Handshakes (EAPOL)
        if pkt.haslayer(EAPOL):
            events_timeline.append({"time": pkt_time, "bssid": bssid, "event": "WPA Handshake (EAPOL)"})
            
        # 2. Check for Deauthentication Attacks
        if pkt.haslayer(Dot11Deauth):
            events_timeline.append({"time": pkt_time, "bssid": bssid, "event": "Deauthentication Attack"})
            
        # 3. Check for PMKID (Inside RSN Information Elements)
        # RSN is element ID 48. If it's long enough, it often contains a PMKID hash.
        if pkt.haslayer(Dot11Elt):
            layer = pkt.getlayer(Dot11Elt)
            while layer:
                if layer.ID == 48 and len(layer.info) >= 22:
                    # Simple heuristic for MVP: Large RSN IEs usually contain the PMKID count and list
                    events_timeline.append({"time": pkt_time, "bssid": bssid, "event": "Potential PMKID Hash Exposed"})
                    break
                layer = layer.payload.getlayer(Dot11Elt)

        # Categorize overall 802.11 frames
        if pkt.haslayer(Dot11):
            if pkt.type == 0:
                management_frames += 1
            elif pkt.type == 1:
                control_frames += 1
            elif pkt.type == 2:
                data_frames += 1
        else:
            other_frames += 1

    print("\n--- PCAP Traffic Summary ---")
    print(f"Total Packets:     {total_packets}")
    print(f"Management Frames: {management_frames}")
    print(f"Control Frames:    {control_frames}")
    print(f"Data Frames:       {data_frames}")
    
    print("\n--- Security Event Timeline ---")
    if not events_timeline:
        print("No security events detected in this capture.")
    else:
        for event in events_timeline:
            print(f"[{event['time']}] {event['event']:<30} -> Target BSSID: {event['bssid']}")
    print("---------------------------------")

if __name__ == "__main__":
    # We expect the user to run: python pcap_analyzer.py path/to/capture.pcap
    if len(sys.argv) < 2:
        print("Usage: python pcap_analyzer.py <path_to_pcap_file>")
    else:
        analyze_pcap(sys.argv[1])
