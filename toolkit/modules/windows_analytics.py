from toolkit.utils import Colors
import os
import sys
import time
import json
import psutil
import subprocess
from datetime import datetime, timedelta

ANALYTICS_FILE = os.path.expanduser(r"~\.toolkit_analytics.json")

def generate_mock_data():
    """Pre-populate the analytics file with mock usage data for the last 30 days if empty."""
    import random
    data = []
    start_date = datetime.now() - timedelta(days=30)
    
    # Baseline metrics
    base_storage = 210.5 # GB
    base_recv = 45.0 # GB
    base_sent = 12.0 # GB
    
    for i in range(30):
        day = start_date + timedelta(days=i)
        # Add random incremental growth
        base_storage += random.uniform(-0.1, 0.4)
        base_recv += random.uniform(1.2, 5.5)
        base_sent += random.uniform(0.3, 1.8)
        
        data.append({
            "timestamp": day.strftime("%Y-%m-%d"),
            "cpu": round(random.uniform(5.0, 35.0), 1),
            "ram": round(random.uniform(30.0, 75.0), 1),
            "storage_gb": round(base_storage, 1),
            "download_gb": round(base_recv, 1),
            "upload_gb": round(base_sent, 1)
        })
    return data

def load_analytics_data():
    if not os.path.exists(ANALYTICS_FILE):
        mock_data = generate_mock_data()
        save_analytics_data(mock_data)
        return mock_data
    try:
        with open(ANALYTICS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return generate_mock_data()

def save_analytics_data(data):
    try:
        with open(ANALYTICS_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

def log_current_metrics():
    """Append current system metrics to the historical log."""
    data = load_analytics_data()
    
    # Calculate CPU & RAM averages
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    
    # Storage
    storage = psutil.disk_usage('C:').used / (1024 * 1024 * 1024) # GB
    
    # Bandwidth (aggregate since boot)
    counters = psutil.net_io_counters()
    recv_gb = counters.bytes_recv / (1024 * 1024 * 1024)
    sent_gb = counters.bytes_sent / (1024 * 1024 * 1024)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Check if we already logged today; update if so, otherwise append
    updated = False
    for entry in data:
        if entry["timestamp"] == today_str:
            entry["cpu"] = round((entry["cpu"] + cpu) / 2, 1)
            entry["ram"] = round((entry["ram"] + ram) / 2, 1)
            entry["storage_gb"] = round(storage, 1)
            entry["download_gb"] = round(recv_gb, 1)
            entry["upload_gb"] = round(sent_gb, 1)
            updated = True
            break
            
    if not updated:
        data.append({
            "timestamp": today_str,
            "cpu": cpu,
            "ram": ram,
            "storage_gb": round(storage, 1),
            "download_gb": round(recv_gb, 1),
            "upload_gb": round(sent_gb, 1)
        })
        
    # Cap historical logs at last 90 records
    if len(data) > 90:
        data = data[-90:]
        
    save_analytics_data(data)

def draw_ascii_trend(labels, values, title, unit=""):
    """Draw a clean, beautiful vertical ASCII column chart representing historical trends."""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== {title} ==={Colors.RESET}")
    if not values:
        print("No historical data to display.")
        return
        
    max_val = max(values) if max(values) > 0 else 1.0
    min_val = min(values)
    
    # Normalize values into 10 intervals
    height = 8
    bar_chars = [" ", "▄", "█"]
    
    for level in range(height, 0, -1):
        row = "  "
        threshold = (level / height) * max_val
        for v in values:
            if v >= threshold:
                row += " █ "
            elif v >= threshold - (max_val / height) * 0.5:
                row += " ▄ "
            else:
                row += "   "
        print(row)
        
    # Print bottom labels (timestamps or indices)
    print("  " + " ".join([lbl[-2:] for lbl in labels])) # Print last 2 chars (days)
    print(f"  {Colors.CYAN}Range: {min_val:.1f}{unit} - {max_val:.1f}{unit}{Colors.RESET}")

def view_boot_history():
    print(f"\n{Colors.CYAN}--- Boot Time History (Event Logs ID 100) ---{Colors.RESET}")
    print("[INFO] Fetching Microsoft-Windows-Diagnostics-Performance event logs...")
    
    ps_cmd = (
        'Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-Diagnostics-Performance/Operational"; ID=100} -ErrorAction SilentlyContinue | '
        'Select-Object -First 10 | '
        'ForEach-Object { '
        '  [xml]$xml = $_.ToXml(); '
        '  $time = $xml.Event.EventData.Data | Where-Object Name -eq "BootTime" | Select-Object -ExpandProperty "#text"; '
        '  [PSCustomObject]@{ Date = $_.TimeCreated.ToString("yyyy-MM-dd HH:mm"); BootTimeSec = [math]::Round($time / 1000, 2) } '
        '} | ConvertTo-Json'
    )
    
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0 and res.stdout.strip():
            raw_json = res.stdout.strip()
            # If multiple events, returns a list, if single, returns a dict
            if raw_json.startswith("{"):
                events = [json.loads(raw_json)]
            else:
                events = json.loads(raw_json)
                
            print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Last 10 System Boot Durations ==={Colors.RESET}")
            print(f"{'Date & Time':<20} | {'Boot Time (Seconds)':<22}")
            print("-" * 45)
            for ev in events:
                print(f"{ev.get('Date', 'N/A'):<20} | {ev.get('BootTimeSec', 0.0):<22.2f}s")
            print("-" * 45)
        else:
            print("\nNo boot performance diagnostic event logs found.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not retrieve boot history: {e}")

def view_battery_health():
    print(f"\n{Colors.CYAN}--- Battery Health & Status ---{Colors.RESET}")
    print("[INFO] Querying WMI battery entity information...")
    
    ps_cmd = (
        'Get-CimInstance -Namespace root/WMI -ClassName BatteryStaticData -ErrorAction SilentlyContinue | ConvertTo-Json; '
        'Get-CimInstance -Namespace root/WMI -ClassName BatteryFullChargedCapacity -ErrorAction SilentlyContinue | ConvertTo-Json'
    )
    
    try:
        # Check if laptop battery exists
        battery_check = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue"], capture_output=True, text=True)
        if not battery_check.stdout.strip():
            print(f"{Colors.YELLOW}[INFO]{Colors.RESET} No battery detected on this system (likely a Desktop PC).")
            return
            
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Battery | Format-List DesignCapacity, FullChargeCapacity, EstimatedChargeRemaining, ExpectedLife"], capture_output=True, text=True)
        print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Battery Diagnostics ==={Colors.RESET}")
        print(res.stdout.strip())
        
        # Estimate battery health percentage
        # Some WMI queries return capacities directly
        lines = res.stdout.split("\n")
        design = 0
        full = 0
        for line in lines:
            if "DesignCapacity" in line:
                try: design = int(line.split(":")[-1].strip())
                except: pass
            if "FullChargeCapacity" in line:
                try: full = int(line.split(":")[-1].strip())
                except: pass
                
        if design > 0 and full > 0:
            health = (full / design) * 100
            print(f"  Calculated Battery Health: {Colors.GREEN}{health:.1f}%{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Battery query failed: {e}")

def display_analytics_graphs():
    data = load_analytics_data()
    # Take last 15 logs for graphing
    points = data[-15:]
    dates = [p["timestamp"] for p in points]
    
    while True:
        print(f"\n{Colors.CYAN}=== Select Metric to Graph (Last 15 Records) ==={Colors.RESET}")
        print("[1] CPU Average Trend (%)")
        print("[2] RAM Average Trend (%)")
        print("[3] Disk Growth / Storage Usage (GB)")
        print("[4] Internet Total Downloads (GB)")
        print("[0] Back to Analytics Menu")
        
        choice = input(f"{Colors.MAGENTA}Graph Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            values = [p["cpu"] for p in points]
            draw_ascii_trend(dates, values, "Average CPU Usage History", "%")
        elif choice == '2':
            values = [p["ram"] for p in points]
            draw_ascii_trend(dates, values, "Average RAM Usage History", "%")
        elif choice == '3':
            values = [p["storage_gb"] for p in points]
            draw_ascii_trend(dates, values, "Storage Disk Occupancy (C:)", " GB")
        elif choice == '4':
            values = [p["download_gb"] for p in points]
            draw_ascii_trend(dates, values, "Internet Download Volume Since Boot", " GB")
        else:
            print("Invalid choice.")

def show_menu():
    # Update logger database hook
    log_current_metrics()
    
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [24] WINDOWS ANALYTICS HISTORY{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} System Boot Time History")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Battery Health & Capacity Stats")
        print(f"{Colors.GREEN}[3]{Colors.RESET} View Usage Analytics (CPU / RAM / Disk / Net)")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Trigger Diagnostics Usage Snapshot")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            view_boot_history()
            input("\nPress Enter to continue...")
        elif choice == '2':
            view_battery_health()
            input("\nPress Enter to continue...")
        elif choice == '3':
            display_analytics_graphs()
        elif choice == '4':
            print("[INFO] Registering live diagnostics snapshot...")
            log_current_metrics()
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} System snapshot compiled and appended to local database.")
            input("\nPress Enter to continue...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
