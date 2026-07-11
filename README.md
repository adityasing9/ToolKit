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
