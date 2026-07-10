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

[1] Storage & Notes          [9] Productivity
[2] Windows Toolkit          [10] QR / Barcode
[3] User Management          [11] System Information
[4] Security                 [12] Cleanup & Maintenance
[5] Networking               [13] Run Commands
[6] File & Folder            [14] Cloud Workspace
[7] Downloads                [15] AI Assistant
[8] Developer Tools          [16] Settings
[0] Exit

Select >
```

---

## 🛠️ Features (16 Core Modules)

1. **Storage & Notes**: Database-backed Links, GitHub Repos, Code Snippets, and Notes.
2. **Windows Toolkit**: One-click DISM/SFC repairs, `chkdsk`, and Restore Point creation.
3. **User Management**: Instant PowerShell wrappers to add/delete users and toggle Administrator rights.
4. **Security**: Multi-threaded TCP Port Scanner, process killer, and local Hosts file blocker.
5. **Networking**: Public/Local IP lookups, saved WiFi password extraction, and ping/tracert wrappers.
6. **File & Folder**: Hide/Unhide files, Large File Finders, ZIP manipulation, and File Hashing.
7. **Downloads**: Full `yt-dlp` integration for 4K/8K Video, MP3 Audio, and YouTube Playlist extraction.
8. **Developer Tools**: Native `git` wrappers, SSH key viewers, and installation checkers for Node, Docker, Java, Go, Rust, etc.
9. **Productivity**: Live Stopwatches/Timers, Password Generators, JSON Formatters, and Base64 encoders.
10. **QR / Barcode**: In-terminal ASCII QR code generation for WiFi setups, Emails, and URLs, with PNG exporting.
11. **System Information**: Real-time `psutil` diagnostics covering CPU, RAM, Disk, Battery, and the Top 10 Memory Consuming Processes.
12. **Cleanup & Maintenance**: One-click cache flushing for Temp, Prefetch, Recycle Bin, DNS, and Winget.
13. **Run Commands**: A dynamic SQLite database pre-loaded with **40+ critical Windows commands** that you can search and execute instantly.
14. **Cloud Workspace**: Cloud synchronization integrations (Coming Soon).
15. **AI Assistant**: Automated terminal AI agent integrations (Coming Soon).
16. **Settings**: Instant terminal Theme swapping (Matrix, Cyberpunk, etc.) and auto-updaters.

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
