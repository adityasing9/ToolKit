import os

modules_dir = r"C:\Users\AADI\Desktop\My\CODE\ToolKit\toolkit\modules"

modules_data = {
    "users.py": {
        "title": "[3] USER MANAGEMENT",
        "options": ["List Users", "Add User", "Delete User", "Change Password", "Lock User", "Unlock User", "Enable User", "Disable User", "Grant Administrator", "Remove Administrator", "Last Login", "Password Expiry", "Account Information", "Export User List"]
    },
    "security.py": {
        "title": "[4] SECURITY",
        "options": ["Block Website", "Unblock Website", "Firewall", "Windows Defender", "BitLocker", "Hosts File Editor", "Port Scanner", "Kill Process", "Startup Malware Scan", "Windows Security Status"]
    },
    "network.py": {
        "title": "[5] NETWORKING",
        "options": ["Public IP", "Local IP", "MAC Address", "DNS", "Flush DNS", "Ping", "Traceroute", "Port Check", "WiFi Passwords", "Connected Devices", "Open Ports", "Network Speed Test", "Proxy Settings", "VPN Status"]
    },
    "files.py": {
        "title": "[6] FILE & FOLDER",
        "options": ["Hide File", "Unhide File", "Hide Folder", "Unhide Folder", "Secure Folder", "Unlock Folder", "Encrypt Folder", "Decrypt Folder", "Find Large Files", "Duplicate Finder", "Folder Size", "Rename Multiple Files", "Compress", "Extract ZIP", "File Hash", "Secure Delete"]
    },
    "downloads.py": {
        "title": "[7] DOWNLOADS",
        "options": ["YT-DLP", "Download Video", "Download Playlist", "Download Audio", "Download Thumbnail", "Ultra Quality", "4K", "8K", "Subtitles", "Cookies", "FFmpeg", "Download Progress", "History"]
    },
    "developer.py": {
        "title": "[8] DEVELOPER TOOLS",
        "options": ["Git", "Clone Repo", "Commit", "Push", "Pull", "Status", "Branch", "Github URLs", "SSH Keys", "Docker", "Node", "Python", "Java", "Rust", "Go", "Flutter", "Android", "VS Code", "WSL", "VirtualBox", "VMware"]
    },
    "productivity.py": {
        "title": "[9] PRODUCTIVITY",
        "options": ["To-do", "Reminder", "Calendar", "Pomodoro", "Timer", "Stopwatch", "Expense Notes", "Clipboard", "Password Generator", "UUID Generator", "Lorem Ipsum", "Random Data", "Base64", "JSON Formatter", "Markdown Preview"]
    },
    "qr.py": {
        "title": "[10] QR / BARCODE",
        "options": ["Generate QR", "Generate Barcode", "QR from Text", "QR from URL", "WiFi QR", "Email QR", "Phone QR", "Scan QR", "Save PNG", "SVG Export"]
    },
    "sysinfo.py": {
        "title": "[11] SYSTEM INFORMATION",
        "options": ["CPU", "RAM", "GPU", "Disk", "Battery", "Motherboard", "BIOS", "Windows Version", "Installed Programs", "Startup Time", "Processes", "Running Services", "Disk Usage", "Temperature", "Health"]
    },
    "cleanup.py": {
        "title": "[12] CLEANUP & MAINTENANCE",
        "options": ["Temp", "Prefetch", "Windows Temp", "Recycle Bin", "DNS Cache", "Thumbnail Cache", "Recent Files", "PowerShell History", "Browser Cache", "Windows Logs", "Disk Cleanup", "Optimize Drives", "Winget Upgrade", "Winget Repair", "App Repair"]
    },
    "encyclopedia.py": {
        "title": "[13] RUN COMMANDS",
        "options": ["List Commands", "Search Command", "Execute Command", "Add Command", "Delete Command"]
    },
    "cloud.py": {
        "title": "[14] CLOUD WORKSPACE",
        "options": ["Saved Links", "Commands", "Secrets", "SSH Keys", "API Keys", "Environment Variables", "Server List", "Remote Notes", "Projects", "Terminal Chat", "Sync", "Backup", "Restore"]
    },
    "ai.py": {
        "title": "[15] AI ASSISTANT",
        "options": ["Ask AI", "Explain Error", "Explain Command", "Generate Regex", "Generate SQL", "Generate Bash", "Generate PowerShell", "Generate Python", "Summarize Logs", "Fix Error", "Search Docs", "Translate", "OCR"]
    },
    "settings.py": {
        "title": "[16] SETTINGS",
        "options": ["Theme", "Light", "Dark", "Cyberpunk", "Green Matrix", "Purple", "Blue", "Font Size", "Update Toolkit", "Backup", "Restore", "Check Version", "Plugins", "Extensions", "Reset"]
    }
}

for filename, data in modules_data.items():
    filepath = os.path.join(modules_dir, filename)
    title = data["title"]
    options = data["options"]
    
    content = f'''def show_menu():
    while True:
        print("\\n=============================================================")
        print("              {title}")
        print("=============================================================")
'''
    for i, opt in enumerate(options, 1):
        content += f'        print("[{i}] {opt}")\n'
    
    content += '''        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
'''
    for i, opt in enumerate(options, 1):
        content += f'''        elif choice == '{i}':
            print("[INFO] {opt} coming soon...")
'''
    
    content += '''        else:
            print("[ERROR] Invalid choice.")
'''
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filename}")
