# WifGyan — Full Project Specification

> This is the complete original spec. `AGENTS.md` is the short, current-state
> summary an AI agent should read every session; this file is the full
> reference for what each feature should eventually look like, including
> example output formats.

## 1. Background

International student in Korea, studying:

- Bachelor's degree, IT & Cyber Security

Interests:

- Python
- Cybersecurity
- Data Science
- Machine Learning / AI
- Networking
- Practical portfolio projects

Goal: a serious GitHub portfolio project, not a small college assignment.
Preference: beginner-friendly explanations along the way, but a final
architecture that is professional and scalable.

## 2. Inspiration: Airgorah

Original repository: https://github.com/martin-olivier/airgorah

Airgorah is a GUI-based Wi-Fi security auditing tool for Linux, including:

- Wi-Fi network discovery
- Access point information
- Client/device discovery
- Wi-Fi traffic capture
- WPA/WPA2 authentication/handshake capture
- PMKID-related analysis
- Wi-Fi security auditing
- Deauthentication/security testing
- Password auditing against captured authentication material
- Graphical interface

Limitation: primarily Linux, because advanced Wi-Fi capability depends on
Linux wireless drivers, monitor mode, packet capture, and packet injection.
It does not provide the same full functionality on Windows natively.

## 3. New project: WifGyan

Instead of porting Airgorah, build an original project inspired by its concept.

**Working name:** WifGyan

**Concept:** A Windows-first Wi-Fi security assessment, monitoring, analysis,
and reporting platform — think Airgorah + Wireshark-style analysis + Wi-Fi
security health checker + network inventory + historical monitoring +
security reports.

**Audience:** authorized network owners, administrators, students, and
cybersecurity professionals.

**Must clearly distinguish:**
- normal defensive/security analysis
- authorized credential access
- authorized lab testing
- advanced low-level wireless functionality

**Not** designed as an unauthorized hacking tool.

## 4–5. Wi-Fi network scanning & security analysis

Scan nearby Wi-Fi networks and display:

- SSID, BSSID
- signal strength
- channel
- frequency/band (2.4 GHz / 5 GHz / 6 GHz where available)
- security type, encryption
- vendor/OUI
- first seen, last seen

```
SSID        Security    Channel    Signal    Band
HomeWiFi    WPA3        36         -42 dBm   5 GHz
Coffee      WPA2        6          -65 dBm   2.4 GHz
Guest       Open        11         -72 dBm   2.4 GHz
```

Security analysis should identify concerns, explain *why* they matter, and
give a recommendation — not just an arbitrary score:

```
Security Assessment

Encryption       WPA2
WPS              Enabled
Password         Weak/Unknown
Rogue AP         None detected
Suspicious       Detected

⚠ WPS enabled
WPS can increase the attack surface of a Wi-Fi network.
Recommendation: Disable WPS if it isn't required.
```

## 6. Password handling

**If a Wi-Fi credential is legitimately stored/available on the authorized
Windows machine:** a protected, separate credential-viewing feature —
not shown automatically on the main dashboard.

```
WiFi: MyHomeWiFi

Password:
••••••••••••

[ Show Password ]

⚠ Requires authorization
```

**If the password isn't available:** the tool must NOT attempt to
discover/crack/recover it.

```
Password:
Not available

Security assessment:
⚠ Password security could not be directly verified.
```

## 7. Device/network inventory

For an authorized network, show devices visible on the local network.

```
DEVICE INVENTORY

192.168.1.1    Router       TP-Link
192.168.1.12   Laptop       Dell
192.168.1.15   Phone        Apple
192.168.1.20   Unknown      Unknown
```

Potential fields: IP address, MAC address, manufacturer, hostname, device
type, first seen, last seen, connection status.

**Privacy rule: the user's own device MAC address must never be stored or
displayed. This was explicitly requested to be forgotten and must stay
forgotten.**

## 8. Packet capture

Where Windows hardware/drivers permit, using established capture technology
(not reinvented):

```
Interface: Wi-Fi
Duration: 5 minutes

[ Start Capture ]

Packets captured       182,391
Management frames       31,294
Control frames          42,881
Data frames            108,216
```

## 9. PCAP/PCAPNG analysis

Import `capture.pcap` / `capture.pcapng` and analyze: 802.11 frames,
management frames, authentication, association, beacons, clients,
AP/client relationships, suspicious events, retransmissions, channel
information, security events, authentication material where present.

```
10:31:02   AP detected
10:31:04   Client appeared
10:31:07   Authentication
10:31:08   Association
10:32:11   Client disconnected
10:32:19   Client re-associated
```

## 10. WPA handshake detection

Analysis feature, not an automatic attack system.

```
Capture Analysis

✓ WPA2 authentication exchange detected

AP:      HomeLab
Client:  XX:XX:XX:XX:XX:XX
Status:  Complete authentication exchange
```

## 11. PMKID detection

```
PMKID

Detected: Yes
Source: capture.pcapng
```

Focus: defensive/authorized analysis.

## 12. Suspicious Wi-Fi activity detection

```
Security Events

⚠ Excessive deauthentication frames
   127 events / 60 sec

⚠ Client repeatedly disconnected

✓ Normal beacon activity
```

Potential detections: excessive deauthentication, unusual authentication
activity, repeated disconnect/reconnect patterns, suspicious AP behavior,
unusual network changes, other measurable anomalies.

## 13. Rogue AP / Evil Twin detection

Defensive detection, not creation of rogue APs.

```
Legitimate:
MyHomeWiFi — BSSID A — WPA2

New network appears:
MyHomeWiFi — BSSID B — WPA2

⚠ POSSIBLE ROGUE ACCESS POINT
SSID matches known network
BSSID differs
Security configuration differs
First observed: 10:32
Signal: -44 dBm
```

## 14. Channel and signal analysis

Historical observations, visualized: signal strength, channel, AP count,
network density, channel congestion indicators, changes over time.

```
Signal strength
  |
-40 ┤    ╭──╮
-50 ┤────╯  ╰──╮
-60 ┤          ╰──
-70 ┤
    └────────────────
      Time
```

This is also the data-science-interest opportunity in the project.

## 15. Historical database

The application remembers previous scans.

Potential SQLite tables: `networks`, `devices`, `observations`, `captures`,
`security_events`, `assessments`, `reports`.

"What changed since the previous scan?"

```
Network Changes

+ New AP detected
+ 3 new devices
- 1 device disappeared
⚠ Security configuration changed
⚠ Possible rogue AP
```

## 16. Security reports

```
WifGyan Security Report

Target: Authorized Lab Network
Assessment Date: 2026-09-28

1. Network Information
2. Access Point Information
3. Connected Devices
4. Authentication Observations
5. Security Findings
6. Suspicious Events
7. Packet Analysis
8. Recommendations
9. Evidence
```

Export formats: PDF, HTML, JSON, CSV.

## 17. Lab Mode

A separate, authorized mode for advanced wireless security experimentation
against networks/devices the user owns or is explicitly authorized to test.

```
LAB MODE

Authorized Test Network

SSID: Aditya-Lab
BSSID: ...
Interface: USB Wi-Fi Adapter

[ Start Assessment ]
```

Advanced low-level wireless testing is isolated from the normal defensive
dashboard. The application never automatically attacks arbitrary nearby
networks.

## 18. Planned architecture

```
                  WifGyan
                       │
        ┌──────────────┴──────────────┐
        │                             │
    Desktop UI                   Core Engine
        │                             │
        │                       ┌─────┴─────┐
        │                       │           │
        │                    Scanner     Analyzer
        │                       │           │
        │                    Capture     Security
        │                       │           │
        │                    Database    Detection
        │
        └────────────── API ───────────────┘
                         │
                  Windows adapters
                         │
                       Npcap
```

## 19. Recommended technology stack

- **Frontend:** React + TypeScript
- **Desktop application:** Tauri
- **Core:** potentially Rust later
- **Initial development:** Python first, for speed and comfort
- **Database:** SQLite
- **Backend/API:** FastAPI
- **Packet capture:** Npcap / libpcap-compatible tooling, subject to
  adapter/driver support
- **Visualization:** Recharts, ECharts, or similar
- **Reports:** HTML → PDF

## 20. Architecture decision: modular capture layer

```
                 Capture Interface
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
 Windows/Npcap      Linux backend     PCAP File
        │               │               │
        └───────────────┼───────────────┘
                        ↓
                 Common Analyzer
```

The main application stays Windows-first; advanced capture capabilities
are optional/modular, because Windows wireless-driver capabilities differ
from Linux.

## 21. Windows support

Goal: the project runs fully on Windows for core functionality.

Planned Windows features: Wi-Fi scanning (SSID/BSSID, signal, channel,
2.4/5 GHz, security detection), device/network inventory, historical
monitoring, security warnings, PCAP import/analysis, handshake detection,
PMKID detection, rogue AP detection, security reports, SQLite database,
dashboard.

Some low-level features depend on the Wi-Fi adapter and Windows driver and
may not work identically on Windows: monitor mode, raw 802.11 capture,
packet injection, advanced active wireless testing.

## 22. Wi-Fi hardware

Adapter: **MediaTek MT7921 Wi-Fi 6 802.11ax PCIe Adapter**
Driver: MediaTek 3.0.1.1284 (dated 21-02-2023)
Status: Up, LinkSpeed 1.2 Gbps

There are also Windows virtual Wi-Fi adapters, but the physical adapter of
interest is the MT7921.

**Do not ask for or store this machine's MAC address — explicitly asked to
be forgotten.**

## 23. What the current adapter supports

| Capability | Support |
|---|---|
| Wi-Fi scanning | ✅ |
| SSID/BSSID information | ✅ |
| Signal information | ✅ |
| Channel information | ✅ |
| 2.4/5 GHz | ✅ |
| Security detection | ✅ |
| Network inventory | ✅ |
| Historical monitoring | ✅ |
| Security warnings | ✅ |
| PCAP analysis | ✅ |
| Handshake detection from PCAP | ✅ |
| PMKID detection from PCAP | ✅ |
| Windows packet capture | ✅/⚠️ |
| Raw 802.11 monitor mode | ⚠️ |
| Advanced active testing | ⚠️/❌ |

No new adapter yet — build and test Windows core functionality first. Only
investigate a compatible USB adapter if raw 802.11 monitor-mode capture
becomes genuinely necessary later.

## 24. Planned development phases

**Version 0.1 — MVP**
Wi-Fi scanner, AP information, signal/channel graphs, vendor detection,
security classification, local device discovery, SQLite database, scan
history, basic security findings, Windows support.

**Version 0.2**
PCAP import, packet analyzer, authentication-event detection, handshake
detection, PMKID detection, suspicious-event detection, timeline.

**Version 0.3**
Rogue AP detection, network-change detection, security dashboard, PDF
reports, JSON/CSV export, lab mode.

**Version 1.0**
```
Windows
   │
   ├── Scanner
   ├── Network inventory
   ├── PCAP capture/import
   ├── 802.11 analyzer
   ├── Authentication analysis
   ├── Rogue AP detection
   ├── Security assessment
   ├── Historical monitoring
   ├── Data visualization
   ├── Lab mode
   └── Reporting
```

## 25. Why this project

A strong cybersecurity + Python + data science portfolio project,
demonstrating:

- **Cybersecurity:** Wi-Fi security, 802.11 concepts, packet analysis,
  network security, security auditing, anomaly detection
- **Python:** APIs, network data processing, automation, database
  interaction, analysis
- **Data Science:** historical Wi-Fi observations, signal analysis,
  anomaly detection, visualization, potentially ML later
- **Software Engineering:** modular architecture, database design, APIs,
  testing, Git/GitHub, documentation
- **UI/UX:** professional dashboard, graphs, security findings, reports

## 26. How to start

Do not build the whole project immediately. Start from the smallest
working component.

```
Phase 1:
Windows
   ↓
Wi-Fi scanner
   ↓
Structured Python data
   ↓
SQLite
   ↓
Security analyzer
   ↓
Basic dashboard
```

First step: run `netsh wlan show networks mode=bssid` and design the
Python scanner from the actual information available, instead of guessing.

## 27. Project philosophy

Not a clone of Airgorah. WifGyan = Windows-first Wi-Fi security
observability and assessment platform.

Differentiators: Windows-first, security-health dashboard, historical
monitoring, rogue AP detection, security-event detection, PCAP analysis,
transparent security findings, professional reporting, modular capture
backend, optional authorized lab mode.

Clear separation between defensive monitoring/analysis and advanced
authorized laboratory testing.

## 28. How the AI assistant should help

Act as technical project mentor/developer:

- Explain things clearly and practically; don't jump ahead unnecessarily.
- Build one component at a time.
- Give exact Windows/PowerShell commands when needed, and explain what
  each command does.
- Prefer free/open-source technologies.
- No hardware purchases unless established as actually necessary.
- Keep the architecture scalable.
- Help write clean GitHub-quality code.
- Explain code rather than dumping huge blocks.
- Keep security functionality focused on authorized/defensive use.
- Test each milestone before moving to the next.
- Eventually help create a professional README, documentation,
  screenshots, architecture diagram, tests, and release.

---

## Progress log

- **2026-09-28:** Fixed `netsh wlan show networks mode=bssid` returning only
  one network — cause was Windows Location Services / "let desktop apps
  access location" being off. Full BSSID-level scan now works. Confirmed
  real output fields: SSID, Network type, Authentication, Encryption,
  BSSID, Signal (%), Radio type, Band, Channel, optional Bss Load
  (Connected Stations, Channel Utilization, Medium Available Capacity),
  QoS fields, Basic/Other rates. Signal is a percentage, not dBm — plan is
  to store the raw percentage and derive an estimated dBm
  (`(percent / 2) - 100`), clearly labeled as an estimate. BSSID (not
  SSID) is the unique identity for an access point.
- **Current step:** Phase 1, Step 1 — build `AccessPoint` dataclass and a
  `parse_netsh_output()` parser, tested against a real saved scan file
  (`samples/scan_01.txt`). No SQLite, API, or UI yet.
