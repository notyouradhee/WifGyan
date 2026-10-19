# WifGyan — Project Roadmap

## Milestone Overview

### Milestone 1: Scanner & Core Storage (v0.1) — COMPLETED
- [x] Windows `netsh` output parser (`scanner.py`)
- [x] Structured data models (`AccessPoint`, RSSI/dBm conversions, security grading) (`models.py`)
- [x] IEEE OUI vendor resolution with randomized MAC detection (`vendors.py`)
- [x] SQLite relational storage (`networks` + historical `observations`) (`database.py`)
- [x] Automated test suite with mock scans (`test_scanner.py`)

### Milestone 2: PCAP Packet Capture Analysis (v0.2) — COMPLETED
- [x] PCAP ingestion and frame categorization via Scapy (`pcap_analyzer.py`)
- [x] WPA 4-way handshake detection (EAPOL layer inspection)
- [x] Deauthentication attack detection (Dot11Deauth frames)
- [x] PMKID exposure detection in RSN information elements (Dot11Elt ID 48)
- [x] Chronological security event timeline with BSSID attribution

### Milestone 3: Dashboard & Anomaly Detection (v0.3) — IN PROGRESS
- [x] **Phase 3.1: FastAPI Web Service (`api.py`)**
  - [x] `GET /api/stats` — Network counts, secure vs. open summary
  - [x] `GET /api/networks` — Historical inventory
  - [x] `POST /api/scan` — On-demand background scan trigger
- [ ] **Phase 3.2: Graphical Web Dashboard**
  - [ ] Interactive network table with signal indicators and vendor badges
  - [ ] Channel distribution chart (2.4 GHz vs 5 GHz vs 6 GHz)
  - [ ] Real-time scan trigger button
- [ ] **Phase 3.3: Rogue AP & Evil Twin Detection**
  - [ ] SSID collision detection with differing security/vendor fingerprints
- [ ] **Phase 3.4: Automated Security Reporting**
  - [ ] Exportable audit summaries (JSON / Markdown / PDF)

### Milestone 4: Native Desktop UI (v1.0) — PLANNED
- [ ] Tauri / React frontend integration
- [ ] Npcap live packet capture listener (Windows NDIS)
- [ ] Comprehensive security rating engine and lab sandbox
