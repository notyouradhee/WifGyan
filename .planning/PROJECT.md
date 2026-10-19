# WifGyan — Project Specification

## 1. Executive Summary
**WifGyan** is a Windows-first Wi-Fi security assessment, monitoring, and reporting tool.
Inspired by tools like Airgorah, it is designed as a cybersecurity and data-science portfolio project emphasizing clean architecture, defensiveness, and automated risk scoring.

## 2. Core Non-Negotiable Rules
- **Defensive only:** Scanning, analysis, monitoring, and reporting for networks the user owns or is authorized to assess.
- **No attacks:** Never implement deauthentication injection, credential cracking, or active unauthorized probing.
- **Privacy:** Never store or display this machine's own MAC address.
- **Hardware baseline:** MediaTek MT7921 Wi-Fi 6 802.11ax PCIe (Standard Windows NDIS mode; no monitor mode injection required).

## 3. Technology Stack
- **Language / Runtime:** Python 3.12+
- **Scanner Engine:** Windows `netsh wlan show networks mode=bssid` with structured regex parsing
- **OUI Vendor Lookup:** `mac-vendor-lookup` with local IEEE cache + heuristic handling for locally administered/randomized MACs
- **Storage:** Local zero-config SQLite (`wifgyan.sqlite3`)
- **Packet Analysis:** `scapy` for offline `.pcap` / `.pcapng` inspection (EAPOL handshakes, deauth frames, PMKID in RSN IE)
- **API Bridge:** `FastAPI` + `uvicorn` serving REST endpoints
- **Testing:** `pytest` against real and synthetic mock captures
- **Orchestration:** Open GSD spec-driven development loop
