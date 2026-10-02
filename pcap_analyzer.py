from scapy.all import rdpcap, Dot11, EAPOL, Dot11Deauth
import sys
from pathlib import Path

def analyze_pcap(file_path: str):
    """
    Reads a .pcap file and counts the types of 802.11 Wi-Fi frames,
    as well as detecting specific security events like Handshakes and Deauths.
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
    
    # Security Event Counters
    eapol_frames = 0
    deauth_frames = 0
    
    print(f"Successfully loaded {total_packets} packets.")
    print("Analyzing 802.11 frame types & Security Events...")
    
    for pkt in packets:
        # Check for Security Events
        if pkt.haslayer(EAPOL):
            eapol_frames += 1
        if pkt.haslayer(Dot11Deauth):
            deauth_frames += 1

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

    print("\n--- PCAP Analysis Summary ---")
    print(f"Total Packets:     {total_packets}")
    print(f"Management Frames: {management_frames} (Beacons, Probes, Auth)")
    print(f"Control Frames:    {control_frames} (ACKs, RTS, CTS)")
    print(f"Data Frames:       {data_frames} (Actual network traffic)")
    print(f"Non-Wi-Fi Frames:  {other_frames}")
    
    print("\n--- Security Events ---")
    print(f"WPA Handshake Packets (EAPOL) : {eapol_frames}")
    print(f"Deauth Frames (Suspicious)    : {deauth_frames}")
    print("-----------------------------")

if __name__ == "__main__":
    # We expect the user to run: python pcap_analyzer.py path/to/capture.pcap
    if len(sys.argv) < 2:
        print("Usage: python pcap_analyzer.py <path_to_pcap_file>")
    else:
        analyze_pcap(sys.argv[1])
