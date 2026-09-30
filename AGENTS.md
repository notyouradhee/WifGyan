# WifGyan — Agent Instructions

Read this file at the start of every session. It is the short, current-state
summary. For the complete original specification — including example output
formats for every planned feature (scanner tables, security assessments,
device inventory, PCAP timelines, reports, Lab Mode) — see
**`docs/PROJECT_SPEC.md`**. Treat this file as "what to do right now and the
rules that never change"; treat PROJECT_SPEC.md as "what each feature should
eventually look like."

## What this is

A Windows-first Wi-Fi security assessment, monitoring, and reporting tool.
Inspired by Airgorah (github.com/martin-olivier/airgorah) but not a clone —
built as a cybersecurity/Python/data-science portfolio project.

## Non-negotiable rules

- **Defensive only.** Scanning, analysis, monitoring, reporting for networks
  the user owns or is explicitly authorized to test.
- **Never** implement deauthentication, packet injection, credential
  cracking, or any attack against networks the user doesn't control.
- A future "Lab Mode" for authorized advanced testing is isolated from the
  main app and is not being built yet.
- **Never store or display this machine's own MAC address.** This was
  explicitly requested to be forgotten.
- The app must never automatically attack arbitrary nearby networks.

## Current phase

**Phase 1 (MVP), Step 1: parser.**
Build an `AccessPoint` dataclass and a `parse_netsh_output()` function that
turns the text from `netsh wlan show networks mode=bssid` into structured
Python objects, tested against a real saved scan (`samples/scan_01.txt`).

Confirmed real-world fields to parse: SSID, Network type, Authentication,
Encryption, BSSID, Signal (%), Radio type, Band, Channel, and an optional
Bss Load block (Connected Stations, Channel Utilization, Medium Available
Capacity) — not every AP broadcasts Bss Load, so those fields must be
nullable. BSSID is the unique identity for an access point, not SSID.
Signal is a percentage; derive an estimated dBm as `(percent / 2) - 100`
and label it clearly as an estimate.

**Do not** start SQLite, FastAPI, the UI, or packet capture yet.

## Hardware

Adapter: MediaTek MT7921 Wi-Fi 6 802.11ax PCIe. Good for scanning, inventory,
history, and PCAP analysis. Monitor mode and packet injection are limited or
unavailable — no new adapter purchase unless that's proven necessary later.

## Planned stack (don't deviate without asking)

Python first for MVP → FastAPI backend → SQLite → React + TypeScript/Tauri
desktop UI later → Npcap for Windows packet capture when that phase starts.

## Working style

- One component at a time. Show a plan and wait for approval before writing
  files.
- Beginner-friendly explanations; production-quality, well-commented code.
- Give exact PowerShell/Windows commands with explanations when needed.
- Prefer free/open-source tools. No hardware purchases unless established
  as necessary.
- Explain code rather than dumping large blocks; keep architecture scalable.
- Test each milestone (e.g. pytest against real sample data) before moving
  to the next.

## Roadmap

- **v0.1 (current):** scanner, AP info, signal/channel graphs, vendor
  detection, security classification, local device discovery, SQLite,
  scan history, basic security findings.
- **v0.2:** PCAP import, handshake detection, PMKID detection,
  suspicious-event detection, timeline.
- **v0.3:** rogue AP detection, network-change detection, dashboard,
  PDF/JSON/CSV reports, Lab Mode.
- **v1.0:** full integration of the above.

## Keeping this file current

After each milestone, update the "Current phase" section above to reflect
what's actually done and what's next — don't let it drift out of sync with
the code.
