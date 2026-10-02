from scapy.all import rdpcap, Dot11
import sys
from pathlib import Path

def analyze_pcap(file_path: str):
    """
    Reads a .pcap file and counts the types of 802.11 Wi-Fi frames.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Could not find file {file_path}")
        return

    print(f"Loading {path.name}... (This might take a moment for large files)")
    
    # rdpcap loads the entire packet capture into memory. 
    # For massive files in the future, we will use PcapReader to stream it.
    packets = rdpcap(str(path))
    
    total_packets = len(packets)
    management_frames = 0
    control_frames = 0
    data_frames = 0
    other_frames = 0
    
    print(f"Successfully loaded {total_packets} packets.")
    print("Analyzing 802.11 frame types...")
    
    for pkt in packets:
        # Check if the packet has an 802.11 Wi-Fi layer
        if pkt.haslayer(Dot11):
            # The 'type' field in Dot11 determines the frame kind:
            # 0 = Management, 1 = Control, 2 = Data
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
    print("-----------------------------")

if __name__ == "__main__":
    # We expect the user to run: python pcap_analyzer.py path/to/capture.pcap
    if len(sys.argv) < 2:
        print("Usage: python pcap_analyzer.py <path_to_pcap_file>")
    else:
        analyze_pcap(sys.argv[1])
