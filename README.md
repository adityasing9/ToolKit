<div align="center">

![Terminal ToolKit Banner](toolkit_github_banner.png)


**A production-quality, pure Python CLI toolkit for Windows.**
It functions as a complete operating system utility, allowing you to manage Windows, run commands, view system stats, extract media, and more—all without leaving your terminal.

</div>

---

## ⚡ Quick Install (One-Line)

Run the following command in PowerShell to instantly download, install, and configure the Toolkit on your machine:

```powershell
iwr -useb https://raw.githubusercontent.com/adityasing9/ToolKit/main/install.ps1 | iex
```

*Optional shortened shortcut link:*
```powershell
irm https://tinyurl.com/ktlla | iex
```

---

## 🖥️ The Main Menu

When you launch the Toolkit, you will be greeted by the natively ANSI-colored main terminal interface:

```text
=============================================================
              ⚡ TERMINAL TOOLKIT v1.0
=============================================================

[1] AI Assistant             [10] Local Network Dashboard [19] Security
[2] Cheat Sheets & Docs      [11] Media Tools             [20] Settings
[3] Cleanup & Maintenance    [12] Network Monitor         [21] Storage & Notes
[4] Cloud Workspace          [13] Networking              [22] System Information
[5] Developer Tools          [14] Process Manager         [23] Universal Search
[6] Downloads                [15] Productivity            [24] User Management
[7] Driver Manager           [16] QR / Barcode            [25] Windows Analytics
[8] File & Folder            [17] Remote Device Manager   [26] Windows Toolkit
[9] Gaming Optimizer         [18] Run Commands            [0] Exit

Select >
```

---

## 🛠️ Features (26 Core Modules)

1. **AI Assistant**: Automated terminal AI agent integrations.
2. **Cheat Sheets & Docs**: Built-in responsive ASCII-formatted documentation tables for CMD, Linux, Git, SQL, Regex, and Markdown.
3. **Cleanup & Maintenance**: One-click cache flushing for Temp, Prefetch, Recycle Bin, DNS, and Winget.
4. **Cloud Workspace**: Cloud synchronization integrations (Coming Soon).
5. **Developer Tools**: Native `git` wrappers, SSH key viewers, and installation checkers for Node, Docker, Java, Go, Rust, etc.
6. **Downloads**: Full `yt-dlp` integration for 4K/8K Video, MP3 Audio, and YouTube Playlist extraction.
7. **Driver Manager**: WMI diagnostics for missing devices, driver export/backup/restore operations, and outdated driver listings.
8. **File & Folder**: Hide/Unhide files, Large File Finders, ZIP manipulation, and File Hashing.
9. **Gaming Optimizer**: Power plan selection, overlay service terminator, RAM standby flusher, TCP parameters, and registry gaming optimizations.
10. **Local Network Dashboard**: Concurrent multithreaded ping sweeps mapping local active IPs, physical MAC addresses, manufacturer OUIs, and device types (Phone, TV, PC, NAS, Printer, Router).
11. **Media Tools**: Image optimizer, pixel resizer, PDF merge/split, offline WinRT OCR extraction, and FFmpeg audio/video converters.
12. **Network Monitor**: Live upload/download bandwidth speedometers, process socket connection mapping, VPN interface status, and historical latency graphs.
13. **Networking**: Public/Local IP lookups, saved WiFi password extraction, and ping/tracert wrappers.
14. **Process Manager**: CPU/RAM processes list, forced process termination, parent-child process tree mapping, startup entries, and live monitors.
15. **Productivity**: Live Stopwatches/Timers, Password Generators, JSON Formatters, and Base64 encoders.
16. **QR / Barcode**: In-terminal ASCII QR code generation for WiFi setups, Emails, and URLs, with PNG exporting.
17. **Remote Device Manager**: Secure, AES-Fernet encrypted remote administration server (Agent) and controller (Client) supporting shells, file transfers, process killers, and power control.
18. **Run Commands**: A dynamic SQLite database pre-loaded with **40+ critical Windows commands** that you can search and execute instantly.
19. **Security**: Multi-threaded TCP Port Scanner, process killer, and local Hosts file blocker.
20. **Settings**: Configures API credentials (Gemini, Supabase), resets local configurations, and manages automated toolkit updates.
21. **Storage & Notes**: Database-backed Links, GitHub Repos, Code Snippets, and Notes.
22. **System Information**: Real-time `psutil` diagnostics covering CPU, RAM, Disk, Battery, and the Top 10 Memory Consuming Processes.
23. **Universal Search**: Everything++ system-wide scanner matching files, active processes, services, environment variables, git history, and docker targets.
24. **User Management**: Instant PowerShell wrappers to add/delete users and toggle Administrator rights.
25. **Windows Analytics**: Local usage analytics log (CPU, RAM, disk, network), battery health degradation diagnostics, boot duration metrics, and vertical ASCII telemetry charts.
26. **Windows Toolkit**: One-click DISM/SFC repairs, `chkdsk`, and Restore Point creation.

---

## 📁 Project Directory Structure

Here is the repository directory layout showing how the codebase is structured:

```text
ToolKit/
├── main.py                # Main CLI execution entry point
├── install.ps1            # Windows Powershell Installer & CLI Manager
├── requirements.txt       # Python project dependencies
├── README.md              # Project documentation
└── toolkit/
    ├── __init__.py
    ├── db.py              # SQLite Database schema & initialization
    ├── utils.py           # Universal ANSI color definitions & console helpers
    └── modules/           # Module folder containing 16 sub-utilities
        ├── __init__.py
        ├── ai.py              # [1] AI Assistant (Gemini REST client, Vision OCR)
        ├── cleanup.py         # [2] Cleanup & Maintenance (Cache, Winget, Prefetch flusher)
        ├── cloud.py           # [3] Cloud Workspace (Supabase sync, Backup/Restore)
        ├── developer.py       # [4] Developer Tools (Git helper, SSH key reader, SDK checks)
        ├── downloads.py       # [5] Downloads (yt-dlp integration for 4K video/MP3 audio)
        ├── files.py           # [6] File & Folder (Hide, Zip, Duplicate finder, Shredder, Timestamps)
        ├── network.py         # [7] Networking (Public/Local IP, DNS/WHOIS lookup, Speed Test)
        ├── productivity.py    # [8] Productivity (Timer/Stopwatch, JSON formatter, Base64 crypt)
        ├── qr.py              # [9] QR / Barcode (ASCII QR renderer, Wifi/URL QR creator)
        ├── encyclopedia.py    # [10] Run Commands (40+ Windows commands search & execution database)
        ├── security.py        # [11] Security (Hosts blocker, Port scanner, Firewall creator, BitLocker)
        ├── settings.py        # [12] Settings (Matrix/Cyberpunk themes, CLI updater, credentials)
        ├── storage.py         # [13] Storage & Notes (Saved Links, Github Repos, Notes, Code Snippets)
        ├── sysinfo.py         # [14] System Information (CPU, RAM, GPU, Processes, WMI Diagnostics)
        ├── users.py           # [15] User Management (Admin toggle, User creation PowerShell wrapper)
        ├── windows_tools.py   # [16] Windows Toolkit (SFC/DISM repair, chkdsk, UAC Device Manager launcher)
        ├── dashboard.py       # [17] System Dashboard / Search Engine (Everything++ search scan)
        ├── media_tools.py     # [18] Media Tools (Image optimization, PDF, OCR, video conversion)
        ├── docs_cheatsheets.py # [19] Cheat Sheets & Docs (Terminal documentation reference tables)
        ├── process_manager.py # [20] Process Manager (Process list, tree, live monitor, CPU/RAM detection)
        ├── network_monitor.py # [21] Network Monitor (Live upload/download speedometer, VPN detection)
        ├── driver_manager.py  # [22] Driver Manager (Backup, export, restore, missing PNP devices)
        ├── gaming_optimizer.py # [23] Gaming Optimizer (High Performance, RAM flusher, overlays killer)
        ├── windows_analytics.py # [24] Windows Analytics (Historical usage logger, battery, boot logs)
        ├── network_dashboard.py # [25] Local Network Dashboard (Ping sweep subnet active device scanner)
        ├── remote_agent.py    # [26] Remote Device Manager (Background socket server Agent service)
        └── remote_manager.py  # [26] Remote Device Manager (Secure client Controller CLI menu)
```

---

## 🗺️ Complete Menu & Sub-Menu Map

Below is the complete tree layout of all nested settings and options available inside the toolkit:

```text
- [1] AI Assistant
  ├── Ask AI (General Programming Chat)
  ├── Explain Error (Stacktrace debugger)
  ├── Explain Command (Shell command guide)
  ├── Generate Regex
  ├── Generate SQL
  ├── Generate Bash / PowerShell / Python code
  ├── Summarize Logs & Fix Error Helper
  └── OCR (Multimodal Image-to-Text extraction)

- [2] Cheat Sheets & Docs [NEW]
  ├── Windows Commands (sfc, dism, flushdns, gpupdate, chkdsk)
  ├── Linux Commands (ls, chmod, chown, df, free, grep, top)
  ├── Git Cheat Sheet (init, add, commit, push, merge, stash, log)
  ├── SQL Cheat Sheet (select, insert, join, create, group by, indexes)
  ├── Regex Examples (digit, word, email, ip matches)
  ├── Markdown Guide (headers, bold/italic, lists, tables, code)
  └── Keyboard Shortcuts (system, browser, VS Code shortcuts)

- [3] Cleanup & Maintenance
  ├── Temp & Prefetch Cache Flush
  ├── Recycle Bin Empty
  ├── DNS Cache Flush
  ├── Winget Cache Flush
  └── Full System Flush

- [4] Cloud Workspace
  ├── Cloud Backup (Upload SQLite database to Supabase)
  ├── Cloud Restore (Download SQLite database from Supabase)
  └── List Cloud Backups

- [5] Developer Tools
  ├── Git Status auditor
  ├── Git Commit & Push shortcut
  ├── SSH Public Key Viewer
  └── SDK Environment Auditor (Node, Java, Rust, Go, Docker, etc.)

- [6] Downloads
  ├── Download Video (4K/8K via yt-dlp)
  ├── Download Audio (MP3 high fidelity)
  └── Download YouTube Playlist

- [7] Driver Manager [NEW]
  ├── Export Drivers (extracts system third-party drivers to backup directory via DISM)
  ├── Backup Drivers (creates structured registry-friendly drivers copy via PnpUtil)
  ├── Restore Drivers (recursively adds and installs drivers from local backup folder)
  ├── Missing Drivers Scanner (queries WMI and PnP interfaces for hardware errors)
  └── Active OEM Drivers (lists active third-party device drivers and firmware versions)

- [8] File & Folder
  ├── Hide / Unhide Files & Folders
  ├── Find Large Files (>100MB tree)
  ├── Duplicate File Finder (MD5 based)
  ├── Folder Size Calculator
  ├── Compress / Extract ZIP files
  ├── File Hash Auditor (MD5, SHA1, SHA256)
  ├── Secure Delete (3-pass random byte Shredder)
  └── Change File Timestamps (Creation, Modification, Last Access) [NEW]

- [9] Gaming Optimizer [NEW]
  ├── Background Apps (restricts background app allowances and halts telemetry tracking)
  ├── Power Optimization (allocates and selects Windows Ultimate Performance schemes)
  ├── Standby RAM Cache (releases memory allocations in system standby queues)
  ├── Active Overlays (closes active Steam, Discord, and Geforce screen overlays)
  ├── Network Latency Tuning (modifies TcpAckFrequency and TCPNoDelay settings)
  └── GameDVR Options (deactivates performance-costing Windows GameDVR features)

- [10] Local Network Dashboard [NEW]
  ├── Subnet Scanner (automatically discovers active IP hosts on the local subnet range)
  ├── ARP Cache Parsing (extracts MAC addresses for discovered network targets)
  ├── Vendor OUI Resolution (maps MAC addresses back to hardware manufacturers/vendors)
  ├── Latency Ping Tests (validates active device response delays in milliseconds)
  └── Device Categorization (groups nodes by type: Phone, TV, Laptop/PC, Printer, NAS, Router)

- [11] Media Tools [NEW]
  ├── Image Optimizer (compress PNG, JPG, JPEG, WEBP)
  ├── Resize Image (custom height/width with aspect ratio scaling)
  ├── PDF Merge (merge multiple PDF files)
  ├── PDF Split (extract page ranges or split entire PDF)
  ├── Offline OCR (native Windows OcrEngine text extraction)
  ├── Audio Converter (mp3, wav, aac, flac, m4a, ogg via FFmpeg)
  ├── Video Converter (mp4, mkv, avi, webm, gif via FFmpeg)
  └── Metadata & EXIF Viewer (Pillow and pypdf specs scanner)

- [12] Network Monitor [NEW]
  ├── Bandwidth Tracking (real-time upload and download byte counters)
  ├── Top Connections Map (lists socket descriptors mapping back to active processes)
  ├── Blocked Hosts Scanner (parses blocked targets inside the Windows hosts file)
  ├── System DNS Configuration (resolves configured DNS servers on active adaptors)
  ├── VPN Connection Detector (automatically scans active interfaces for VPN tags)
  └── Latency Graph Monitor (live pings to 1.1.1.1 matched to an ASCII sparkline graph)

- [13] Networking
  ├── Public & Local IP lookups
  ├── MAC Address auditor
  ├── DNS Configuration & Flush DNS
  ├── Ping & Traceroute execution
  ├── DNS & WHOIS Domain lookup (RDAP) [NEW]
  ├── Saved WiFi Passwords extraction
  ├── Connected Devices Scanner (ARP table)
  └── Network Speed Test (Cloudflare throughput test) [NEW]

- [14] Process Manager [NEW]
  ├── Active Processes List (sortable by RAM or CPU usage)
  ├── Process Control (kill or restart process instances)
  ├── Process Tree Viewer (parent-child relationship map)
  ├── Startup Applications (HKCU & HKLM Run registry key listings)
  ├── High Utilization Scanners (CPU/RAM threshold alerts)
  └── Live Task Monitor (refreshing console statistics dashboard)

- [15] Productivity
  ├── Stopwatch & Countdown Timer
  ├── Password Generator (Secure length & entropy)
  ├── JSON Formatter
  └── Base64 Encoder/Decoder

- [16] QR / Barcode
  ├── Text / URL QR Code
  ├── Email QR Code
  ├── WiFi Setup QR Code
  └── ASCII Terminal Renderer & PNG export

- [17] Remote Device Manager [NEW]
  ├── Encrypted Sockets (uses AES-Fernet secure E2E encryption for all remote packets)
  ├── Setup Wizard (provisions Device ID & HMAC pairing codes for authorized connections)
  ├── Interactive CMD/PowerShell (handles bidirectional remote console terminal streams)
  ├── File Transfer Manager (supports folder navigation, file downloads and uploads)
  ├── Process & Service Controllers (lists, controls, starts, stops, or terminates items)
  └── Remote Power Options (triggers workstation sleep, lock, restarts, or shutdowns)

- [18] Run Commands
  ├── Search Command Database
  ├── Execute Command directly
  └── List Command Catalog (40+ built-in cmd shortcuts)

- [19] Security
  ├── Block / Unblock Website domains (via hosts)
  ├── Hosts File Editor (requires Admin)
  ├── Port Scanner (TCP port scan)
  ├── Kill Process (via PID)
  ├── Startup Malware Scan (Heuristics Registry run keys)
  ├── Firewall Rules Creator (Block Port / Block App) [NEW]
  ├── Active Connections Mapping (Port/PID/Process name audit) [NEW]
  └── BitLocker Status (Console-based PowerShell/WMIC checker) [NEW]

- [20] Settings
  ├── Swap Color Themes (Matrix, Cyberpunk, Light, Dark)
  ├── Update Toolkit (GitHub pull)
  ├── Reset settings
  └── Configure API / Cloud Keys (Gemini, Supabase credentials)

- [21] Storage & Notes
  ├── Links Manager (URL cards display)
  ├── Github Saved Repos
  ├── Code Snippet Bookkeeper
  ├── Quick Notes
  └── Export Database Backup

- [22] System Information
  ├── CPU, RAM, and GPU diagnostics
  ├── Disk Space & Partitioning
  ├── Battery Health (mWh design vs full capacity, cycles, backup estimators) [NEW]
  ├── Motherboard & BIOS Info
  ├── Top 10 Memory Consuming Processes
  ├── Active Windows Services listing [NEW]
  ├── WMI Health Diagnostics (SMART drive health) [NEW]
  ├── CPU/GPU Temperature sensor checker [NEW]
  └── System Dashboard (Double-pane boxed summary layout) [NEW]

- [23] Universal Search [NEW]
  └── Keyword Search (scans notes, snippets, commands, links, and repositories)

- [24] User Management
  ├── Add / Delete Local User Accounts
  ├── Promote User to Administrator
  ├── Demote User to Standard
  └── List Local System Users

- [25] Windows Analytics [NEW]
  ├── Boot Time Records (scans Event Log diagnostics for system boot times)
  ├── Battery Health (queries laptop battery designs vs actual charge capacities)
  ├── Historical Database (stores CPU, RAM, disk, and bandwidth usage statistics)
  └── Terminal Graphs (plots historical telemetry on weekly/monthly vertical ASCII bar charts)

- [26] Windows Toolkit
  ├── Windows Activation & Key Manager [NEW]
  │   ├── View Activation Expiry Status
  │   ├── View Detailed License Information (slmgr /dlv)
  │   ├── View Installed Product Key
  │   ├── Backup & Store Product Key to File
  │   ├── Uninstall Installed Product Key (slmgr /upk)
  │   ├── Clear Product Key from Registry (slmgr /cpky)
  │   └── Complete Key Deletion (Uninstall + Clear Registry)
  ├── Device Manager UAC Launcher
  ├── Services & Startup Managers
  ├── Windows Repair (SFC + DISM RestoreHealth)
  ├── Environment Variables Editor
  └── Create System Restore Point
```

---

## 🚀 Global 'tool' Shortcut & Direct Routing

You can bypass the interactive menu entirely and trigger any toolkit feature globally from **any directory** on your computer using the **`tool`** command.

> [!NOTE]
> If you are running commands directly inside the repository folder *before* restarting your terminal (or without global setup), PowerShell requires the **`.\`** prefix:
> ```powershell
> .\tool <command>
> ```
> Once the global PATH setup is applied and you open a new terminal, you can type **`tool <command>`** from anywhere.

### Global Setup
1. Run **Option 1 (Install / Update & Run Toolkit)** from your CLI Manager (`install.ps1`). This automatically registers the ToolKit directory to your Windows User `PATH` environment variable.
2. Open a **new** terminal window (to load the updated environment path changes).

### Complete Command Alias Directory
You can pass any of the following parameters to the **`tool`** command to trigger a specific module directly:

| Command Module | Supported Aliases |
| :--- | :--- |
| **Command Center Dashboard** | `tool dash`, `tool status`, `tool dashboard` |
| **[1] AI Assistant** | `tool ai`, `tool assistant`, `tool gpt`, `tool gemini`, `tool chat`, `tool bot` |
| **[2] Cheat Sheets & Docs** | `tool docs`, `tool cheat`, `tool cheatsheet`, `tool git`, `tool sql`, `tool regex` |
| **[3] Cleanup & Maintenance** | `tool clean`, `tool cleanup`, `tool flush`, `tool clear`, `tool purge` |
| **[4] Cloud Workspace** | `tool cloud`, `tool workspace`, `tool supabase`, `tool sync`, `tool backup`, `tool restore` |
| **[5] Developer Tools** | `tool dev`, `tool developer`, `tool git`, `tool ssh`, `tool env`, `tool sdk` |
| **[6] Downloads** | `tool download`, `tool downloads`, `tool youtube`, `tool yt`, `tool ytdl`, `tool video`, `tool mp3` |
| **[7] Driver Manager** | `tool driver`, `tool drivers`, `tool pnputil`, `tool dism-driver`, `tool backup-drivers` |
| **[8] File & Folder** | `tool file`, `tool files`, `tool folder`, `tool folders`, `tool shred`, `tool zip`, `tool hash`, `tool timestamp` |
| **[9] Gaming Optimizer** | `tool gameopt`, `tool fps`, `tool optimize-game`, `tool game`, `tool gaming` |
| **[10] Local Network Dashboard** | `tool networkdashboard`, `tool netdash`, `tool subnet`, `tool discover`, `tool devices`, `tool arp` |
| **[11] Media Tools** | `tool media`, `tool pdf`, `tool ocr`, `tool convert`, `tool resize` |
| **[12] Network Monitor** | `tool networkmonitor`, `tool netmon`, `tool traffic`, `tool bandwidth`, `tool latency`, `tool dns`, `tool vpn` |
| **[13] Networking** | `tool network`, `tool networking`, `tool ip`, `tool ping`, `tool wifi`, `tool speed`, `tool speedtest`, `tool whois` |
| **[14] Process Manager** | `tool process`, `tool proc`, `tool kill`, `tool taskmgr`, `tool monitor`, `tool pstree`, `tool startup` |
| **[15] Productivity** | `tool productivity`, `tool timer`, `tool stopwatch`, `tool password`, `tool json`, `tool base64` |
| **[16] QR / Barcode** | `tool qr`, `tool barcode`, `tool wifiqr` |
| **[17] Remote Device Manager** | `tool remote`, `tool agent`, `tool pair`, `tool rterminal`, `tool rconnect`, `tool remotemanager` |
| **[18] Run Commands** | `tool commands`, `tool cmd`, `tool run`, `tool encyclopedia`, `tool catalog` |
| **[19] Security** | `tool security`, `tool firewall`, `tool ports`, `tool hosts`, `tool bitlocker` |
| **[20] Settings** | `tool settings`, `tool theme`, `tool config` |
| **[21] Storage & Notes** | `tool storage`, `tool notes`, `tool links`, `tool snippets`, `tool db` |
| **[22] System Information** | `tool sysinfo`, `tool info`, `tool specs`, `tool temp`, `tool temperature`, `tool cpu`, `tool ram`, `tool gpu`, `tool battery` |
| **[23] Universal Search** | `tool search`, `tool find`, `tool query`, `tool ask` |
| **[24] User Management** | `tool user`, `tool users`, `tool admin`, `tool accounts` |
| **[25] Windows Analytics** | `tool analytics`, `tool telemetry`, `tool boothistory`, `tool battery`, `tool history`, `tool usage` |
| **[26] Windows Toolkit** | `tool windows`, `tool toolkit`, `tool sfc`, `tool dism`, `tool restorepoint`, `tool activate`, `tool activation` |

### Direct Module Routing (Fallback)
If you are manually running scripts from within the repository root, you can bypass the interactive menu by calling `main.py` directly:
```powershell
python main.py dashboard      # Launches the side-by-side System Dashboard
python main.py search         # Launches the Universal Search Engine
python main.py sysinfo        # Launches the System Information menu
```

---

## ⚙️ Manual Setup (For Developers)

1. Clone the repository.
2. Ensure you have Python 3.10+ installed.
3. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install requirements:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run the application:
   ```powershell
   python main.py
   ```
