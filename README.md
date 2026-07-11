<div align="center">

```text
 __________________________________________________________________
|                                                                  |
|   _______                  _             _   _______      _ _    |
|  |__   __|                (_)           | | |__   __|    | | |   |
|     | | ___ _ __ _ __ ___  _ _ __   __ _| |    | | ___   | | |   |
|     | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |    | |/ _ \  | | |   |
|     | |  __/ |  | | | | | | | | | | (_| | |    | | (_) | | | |   |
|     |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|    |_|\___/  |_|_|   |
|                                                                  |
|                    v1.0 (CLI Edition)                            |
|__________________________________________________________________|
```

**A production-quality, pure Python CLI toolkit for Windows.**
It functions as a complete operating system utility, allowing you to manage Windows, run commands, view system stats, extract media, and more—all without leaving your terminal.

</div>

---

## ⚡ Quick Install (One-Line)

Run the following command in PowerShell as Administrator to instantly download, install, and configure the Toolkit on your machine:

```powershell
iwr -useb https://raw.githubusercontent.com/adityasing9/ToolKit/main/install.ps1 | iex
```

---

## 🖥️ The Main Menu

When you launch the Toolkit, you will be greeted by the natively ANSI-colored main terminal interface:

```text
=============================================================
              ⚡ TERMINAL TOOLKIT v1.0
=============================================================

[1] AI Assistant             [9] QR / Barcode
[2] Cleanup & Maintenance    [10] Run Commands
[3] Cloud Workspace          [11] Security
[4] Developer Tools          [12] Settings
[5] Downloads                [13] Storage & Notes
[6] File & Folder            [14] System Information
[7] Networking               [15] User Management
[8] Productivity             [16] Windows Toolkit
[0] Exit

Select >
```

---

## 🛠️ Features (16 Core Modules)

1. **AI Assistant**: Automated terminal AI agent integrations (Coming Soon).
2. **Cleanup & Maintenance**: One-click cache flushing for Temp, Prefetch, Recycle Bin, DNS, and Winget.
3. **Cloud Workspace**: Cloud synchronization integrations (Coming Soon).
4. **Developer Tools**: Native `git` wrappers, SSH key viewers, and installation checkers for Node, Docker, Java, Go, Rust, etc.
5. **Downloads**: Full `yt-dlp` integration for 4K/8K Video, MP3 Audio, and YouTube Playlist extraction.
6. **File & Folder**: Hide/Unhide files, Large File Finders, ZIP manipulation, and File Hashing.
7. **Networking**: Public/Local IP lookups, saved WiFi password extraction, and ping/tracert wrappers.
8. **Productivity**: Live Stopwatches/Timers, Password Generators, JSON Formatters, and Base64 encoders.
9. **QR / Barcode**: In-terminal ASCII QR code generation for WiFi setups, Emails, and URLs, with PNG exporting.
10. **Run Commands**: A dynamic SQLite database pre-loaded with **40+ critical Windows commands** that you can search and execute instantly.
11. **Security**: Multi-threaded TCP Port Scanner, process killer, and local Hosts file blocker.
12. **Settings**: Instant terminal Theme swapping (Matrix, Cyberpunk, etc.) and auto-updaters.
13. **Storage & Notes**: Database-backed Links, GitHub Repos, Code Snippets, and Notes.
14. **System Information**: Real-time `psutil` diagnostics covering CPU, RAM, Disk, Battery, and the Top 10 Memory Consuming Processes.
15. **User Management**: Instant PowerShell wrappers to add/delete users and toggle Administrator rights.
16. **Windows Toolkit**: One-click DISM/SFC repairs, `chkdsk`, and Restore Point creation.

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
        └── windows_tools.py   # [16] Windows Toolkit (SFC/DISM repair, chkdsk, UAC Device Manager launcher)
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

- [2] Cleanup & Maintenance
  ├── Temp & Prefetch Cache Flush
  ├── Recycle Bin Empty
  ├── DNS Cache Flush
  ├── Winget Cache Flush
  └── Full System Flush

- [3] Cloud Workspace
  ├── Cloud Backup (Upload SQLite database to Supabase)
  ├── Cloud Restore (Download SQLite database from Supabase)
  └── List Cloud Backups

- [4] Developer Tools
  ├── Git Status auditor
  ├── Git Commit & Push shortcut
  ├── SSH Public Key Viewer
  └── SDK Environment Auditor (Node, Java, Rust, Go, Docker, etc.)

- [5] Downloads
  ├── Download Video (4K/8K via yt-dlp)
  ├── Download Audio (MP3 high fidelity)
  └── Download YouTube Playlist

- [6] File & Folder
  ├── Hide / Unhide Files & Folders
  ├── Find Large Files (>100MB tree)
  ├── Duplicate File Finder (MD5 based)
  ├── Folder Size Calculator
  ├── Compress / Extract ZIP files
  ├── File Hash Auditor (MD5, SHA1, SHA256)
  ├── Secure Delete (3-pass random byte Shredder)
  └── Change File Timestamps (Creation, Modification, Last Access)

- [7] Networking
  ├── Public & Local IP lookups
  ├── MAC Address auditor
  ├── DNS Configuration & Flush DNS
  ├── Ping & Traceroute execution
  ├── DNS & WHOIS Domain lookup (RDAP)
  ├── Saved WiFi Passwords extraction
  ├── Connected Devices Scanner (ARP table)
  └── Network Speed Test (Cloudflare measurement)

- [8] Productivity
  ├── Stopwatch & Countdown Timer
  ├── Password Generator (Secure length & entropy)
  ├── JSON Formatter
  └── Base64 Encoder/Decoder

- [9] QR / Barcode
  ├── Text / URL QR Code
  ├── Email QR Code
  ├── WiFi Setup QR Code
  └── ASCII Terminal Renderer & PNG export

- [10] Run Commands
  ├── Search Command Database
  ├── Execute Command directly
  └── List Command Catalog (40+ built-in cmd shortcuts)

- [11] Security
  ├── Block / Unblock Website domains (via hosts)
  ├── Hosts File Editor (requires Admin)
  ├── Port Scanner (TCP port scan)
  ├── Kill Process (via PID)
  ├── Startup Malware Scan (Heuristics Registry run keys)
  ├── Firewall Rules Creator (Block Port / Block App)
  └── Active Connections Mapping (Port/PID/Process name audit)

- [12] Settings
  ├── Swap Color Themes (Matrix, Cyberpunk, Light, Dark)
  ├── Update Toolkit (GitHub pull)
  ├── Reset settings
  └── Configure API / Cloud Keys (Gemini, Supabase credentials)

- [13] Storage & Notes
  ├── Links Manager (URL cards display)
  ├── Github Saved Repos
  ├── Code Snippet Bookkeeper
  ├── Quick Notes
  └── Export Database Backup

- [14] System Information
  ├── CPU, RAM, and GPU diagnostics
  ├── Disk Space & Partitioning
  ├── Battery Health
  ├── Motherboard & BIOS Info
  ├── Top 10 Memory Consuming Processes
  ├── Active Windows Services
  └── WMI Health Diagnostics (SMART drive health)

- [15] User Management
  ├── Add / Delete Local User Accounts
  ├── Promote User to Administrator
  ├── Demote User to Standard
  └── List Local System Users

- [16] Windows Toolkit
  ├── Windows Activation Status check (cscript console slmgr)
  ├── Device Manager UAC Launcher
  ├── Services & Startup Managers
  ├── Windows Repair (SFC + DISM RestoreHealth)
  ├── Environment Variables Editor
  └── Create System Restore Point
```

---

## 🚀 Direct Module Routing
You can bypass the interactive menu and jump straight into a module by passing its name as an argument to the python script:
```powershell
python main.py sysinfo
python main.py downloads
python main.py cleanup
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
