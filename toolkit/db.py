import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toolkit.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create commands table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            command TEXT NOT NULL,
            description TEXT,
            category TEXT,
            risk_level TEXT,
            purpose TEXT
        )
    ''')

    # Create notes table (strictly private)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create links table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create github repos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS github_repos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create snippets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

def get_setting(key, default=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row['value']
    except Exception:
        pass
    return default

def set_setting(key, value):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
    except Exception:
        pass

    # Seed initial data for commands if empty
    cursor.execute("SELECT COUNT(*) FROM commands")
    if cursor.fetchone()[0] == 0:
        seed_data = [
            ("Add/Remove Programs", "appwiz.cpl", "Programs and Features", "System", "Low", "Uninstall apps"),
            ("Windows Features", "optionalfeatures", "Turn Windows features on or off", "System", "Medium", "Manage OS features"),
            ("Device Manager", "devmgmt.msc", "Hardware device manager", "System", "Medium", "Manage drivers"),
            ("Event Viewer", "eventvwr", "View system logs", "System", "Low", "Troubleshoot errors"),
            ("Disk Management", "diskmgmt.msc", "Manage hard drives", "System", "High", "Partition drives"),
            ("Services", "services.msc", "Manage background services", "System", "Medium", "Start/stop services"),
            ("Task Manager", "taskmgr", "Manage running processes", "System", "Low", "Kill processes"),
            ("Resource Monitor", "resmon", "Detailed resource usage", "System", "Low", "Monitor CPU/RAM"),
            ("Performance Monitor", "perfmon", "System performance data", "System", "Low", "Analyze performance"),
            ("Group Policy", "gpedit.msc", "Local Group Policy Editor", "System", "High", "Edit OS policies"),
            ("Registry Editor", "regedit", "Windows Registry Editor", "System", "High", "Edit registry keys"),
            ("System Configuration", "msconfig", "Boot configuration", "System", "High", "Manage boot options"),
            ("Control Panel", "control", "Legacy control panel", "System", "Low", "System settings"),
            ("Windows Firewall", "firewall.cpl", "Manage firewall rules", "Security", "Medium", "Network security"),
            ("Network Connections", "ncpa.cpl", "Manage adapters", "Networking", "Medium", "Network settings"),
            ("Internet Properties", "inetcpl.cpl", "Internet options", "Networking", "Low", "Browser settings"),
            ("Power Options", "powercfg.cpl", "Manage power plans", "System", "Low", "Battery/Power settings"),
            ("DiskPart", "diskpart", "Command-line disk partitioning", "Storage", "High", "Format/manage disks"),
            ("System Properties", "sysdm.cpl", "Advanced system settings", "System", "Medium", "Env vars/Computer name"),
            ("Computer Management", "compmgmt.msc", "System management tools", "System", "Medium", "Admin tools"),
            ("Malware Removal Tool", "mrt", "Windows Malicious Software Removal", "Security", "Low", "Scan for malware"),
            ("Diagnostics Tool", "msdt", "Microsoft Support Diagnostic Tool", "System", "Low", "Troubleshoot OS"),
            ("Memory Diagnostic", "mdsched", "Windows Memory Diagnostic", "System", "Medium", "Test RAM"),
            ("Disk Cleanup", "cleanmgr", "Disk Cleanup Utility", "Storage", "Low", "Removes temporary files"),
            ("DirectX Diagnostic", "dxdiag", "DirectX Info", "System", "Low", "View GPU/Audio details"),
            ("Windows Version", "winver", "About Windows", "System", "Low", "View OS build"),
            ("Command Prompt", "cmd", "Windows Terminal", "Terminal", "Low", "CLI"),
            ("PowerShell", "powershell", "Windows PowerShell", "Terminal", "Low", "Advanced CLI"),
            ("Windows Terminal", "wt", "Modern Terminal", "Terminal", "Low", "Tabbed CLI"),
            ("File Explorer", "explorer", "Windows Explorer", "Files", "Low", "Browse files"),
            ("Notepad", "notepad", "Text Editor", "Productivity", "Low", "Edit text files"),
            ("Calculator", "calc", "Windows Calculator", "Productivity", "Low", "Math"),
            ("On-Screen Keyboard", "osk", "Virtual Keyboard", "Accessibility", "Low", "Type without physical keyboard"),
            ("Magnifier", "magnify", "Screen Magnifier", "Accessibility", "Low", "Zoom in on screen"),
            ("Snipping Tool", "snippingtool", "Screen capture", "Productivity", "Low", "Take screenshots"),
            ("Startup Folder", "shell:startup", "User startup items", "System", "Low", "Manage startup apps"),
            ("SendTo Folder", "shell:sendto", "Send To context menu", "System", "Low", "Manage SendTo menu"),
            ("Temp Folder (User)", "explorer %temp%", "User temporary files", "Files", "Low", "View user temp files"),
            ("Temp Folder (System)", "explorer C:\\Windows\\Temp", "System temporary files", "Files", "Medium", "View system temp files"),
            ("Prefetch Folder", "explorer C:\\Windows\\Prefetch", "Windows prefetch data", "Files", "Medium", "View prefetch cache")
        ]
        cursor.executemany(
            "INSERT INTO commands (name, command, description, category, risk_level, purpose) VALUES (?, ?, ?, ?, ?, ?)",
            seed_data
        )
        conn.commit()

    conn.close()
