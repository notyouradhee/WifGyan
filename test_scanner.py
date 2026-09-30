from scanner import parse_netsh_output

def test_parse_netsh_output():
    # 1. Read the raw sample we saved
    with open("samples/scan_01.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    # 2. Run it through the parser
    access_points = parse_netsh_output(raw_text)
    
    # 3. Assertions to verify our code works
    assert len(access_points) > 0, "No access points were found in the sample!"
    
    # Check the first AP specifically (MyHomeWiFi)
    first_ap = access_points[0]
    assert first_ap.ssid == "MyHomeWiFi"
    assert first_ap.authentication == "WPA2-Personal"
    assert first_ap.encryption == "CCMP"
    assert first_ap.bssid == "1a:2b:3c:4d:5e:6f"
    assert first_ap.signal_percent == 82
    assert first_ap.channel == 36
    assert first_ap.band == "5 GHz"
    
    print("✓ All tests passed! The parser correctly read the AccessPoint.")
    
if __name__ == "__main__":
    test_parse_netsh_output()
