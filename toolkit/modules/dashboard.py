import sys
import os
import psutil
import platform
import subprocess
import socket
import urllib.request
import json
import datetime
import tempfile
import winreg
import ctypes
from toolkit.utils import Colors
from toolkit.db import get_connection

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def get_greeting():
    import datetime
    now = datetime.datetime.now()
    hr = now.hour
    if hr < 12: return "Good Morning 🌅"
    elif hr < 17: return "Good Afternoon ☀️"
    else: return "Good Evening 🌙"

def get_os_caption():
    try:
        output = subprocess.check_output(["wmic", "os", "get", "Caption"], stderr=subprocess.DEVNULL, text=True, errors="ignore")
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            caption = lines[1]
            if caption.startswith("Microsoft "):
                caption = caption[10:]
            return caption
    except Exception:
        pass
    return f"{platform.system()} {platform.release()}"

def check_secure_boot():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\SecureBoot\State")
        val, _ = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
        return "Enabled" if val == 1 else "Disabled"
    except Exception:
        return "Disabled (Not Supported)"

def check_activation_expiry():
    try:
        res = subprocess.run(["cscript", "//NoLogo", "C:\\Windows\\System32\\slmgr.vbs", "/xpr"], capture_output=True, text=True, timeout=8)
        if "permanently activated" in res.stdout.lower():
            return "Never (Digital License)"
        return res.stdout.strip() if res.stdout.strip() else "Never (Digital License)"
    except Exception:
        return "Never (Digital License)"

def check_firewall_status():
    try:
        res = subprocess.run(["netsh", "advfirewall", "show", "allprofiles", "state"], capture_output=True, text=True, timeout=5)
        if "ON" in res.stdout:
            return "ON"
        return "OFF"
    except Exception:
        return "ON (Active)"

def check_bitlocker_status():
    try:
        out = subprocess.check_output(["wmic", "path", "win32_encryptablevolume", "get", "protectionstatus"], stderr=subprocess.DEVNULL, text=True, errors="ignore")
        if "1" in out:
            return "Enabled"
        return "Disabled"
    except Exception:
        return "Disabled"

def check_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        res = s.connect_ex(("127.0.0.1", port))
        s.close()
        return "Running" if res == 0 else "Stopped"
    except Exception:
        return "Stopped"

def check_docker_status():
    try:
        res = subprocess.run(["docker", "info"], capture_output=True, timeout=2)
        return "Running" if res.returncode == 0 else "Stopped"
    except Exception:
        return "Stopped"

def get_docker_stats():
    try:
        c_res = subprocess.run(["docker", "ps", "-a", "-q"], capture_output=True, text=True, timeout=2)
        containers = len(c_res.stdout.strip().split("\n")) if c_res.stdout.strip() else 0
        i_res = subprocess.run(["docker", "images", "-q"], capture_output=True, text=True, timeout=2)
        images = len(set(i_res.stdout.strip().split("\n"))) if i_res.stdout.strip() else 0
        return f"{containers} Containers, {images} Images"
    except Exception:
        return "0 Containers, 0 Images"

def get_vms_status():
    wsl = "Stopped"
    try:
        res = subprocess.run(["wsl", "-l", "--running"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0 and res.stdout.strip():
            wsl = "Running"
    except Exception:
        wsl = "Stopped"
        
    hyperv = "Stopped"
    try:
        if psutil.win_service_get("vmms").status() == "running":
            hyperv = "Running"
    except Exception:
        pass
        
    vbox = "Stopped"
    for p in psutil.process_iter(["name"]):
        if p.info["name"] and "vbox" in p.info["name"].lower():
            vbox = "Running"
            break
            
    vmware = "Stopped"
    for p in psutil.process_iter(["name"]):
        if p.info["name"] and "vmware" in p.info["name"].lower():
            vmware = "Running"
            break
    return wsl, hyperv, vbox, vmware

def is_tool_installed(name):
    from shutil import which
    return "Installed" if which(name) is not None else "Not Installed"

def get_weather():
    try:
        req = urllib.request.Request("https://wttr.in/?format=j1", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode())
            current = data["current_condition"][0]
            temp = current["temp_C"]
            humidity = current["humidity"]
            wind = current["windspeedKmph"]
            desc = current["weatherDesc"][0]["value"]
            area = data["nearest_area"][0]["areaName"][0]["value"]
            return f"{area}: {desc} | Temp: {temp}°C | Hum: {humidity}% | Wind: {wind} km/h"
    except Exception:
        return "Offline / Weather Data N/A"

def get_cleanup_suggestions():
    temp_size = 0
    try:
        tdir = tempfile.gettempdir()
        for entry in os.scandir(tdir):
            if entry.is_file():
                temp_size += entry.stat().st_size
    except Exception:
        pass
        
    downloads_size = 0
    try:
        down_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        for entry in os.scandir(down_dir):
            if entry.is_file():
                downloads_size += entry.stat().st_size
    except Exception:
        pass
    
    suggest = f"{temp_size / (1024**3):.1f} GB Temp Files"
    if downloads_size > 0:
        suggest += f" | {downloads_size / (1024**3):.1f} GB Downloads"
    return suggest

def get_connected_devices():
    usb_count = 0
    try:
        out = subprocess.check_output(["wmic", "path", "Win32_USBControllerDevice", "get", "Dependent"], stderr=subprocess.DEVNULL, text=True, errors="ignore")
        usb_count = len([line for line in out.split("\n") if line.strip()]) - 1
    except Exception:
        pass
    return f"{usb_count if usb_count > 0 else 'N/A'} USB Devices"

def get_top_processes():
    top_cpu = "N/A"
    top_ram = "N/A"
    try:
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            procs.append(p.info)
        procs_ram = sorted(procs, key=lambda x: x.get("memory_percent") or 0, reverse=True)
        if procs_ram:
            top_ram = f"{procs_ram[0]['name']} ({round(procs_ram[0]['memory_percent'], 1)}%)"
        procs_cpu = sorted(procs, key=lambda x: x.get("cpu_percent") or 0, reverse=True)
        if procs_cpu:
            top_cpu = f"{procs_cpu[0]['name']} ({round(procs_cpu[0]['cpu_percent'], 1)}%)"
    except Exception:
        pass
    return top_cpu, top_ram

def get_size(bytes):
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < 1024: return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def search_everything(query):
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Search Commands
    c.execute("SELECT name, command, description FROM commands WHERE name LIKE ? OR command LIKE ? OR description LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
    cmds = c.fetchall()
    
    # 2. Search Notes
    c.execute("SELECT title, content FROM notes WHERE title LIKE ? OR content LIKE ?", (f"%{query}%", f"%{query}%"))
    notes = c.fetchall()
    
    # 3. Search Links
    c.execute("SELECT title, url FROM links WHERE title LIKE ? OR url LIKE ?", (f"%{query}%", f"%{query}%"))
    links = c.fetchall()
    
    # 4. Search Snippets
    c.execute("SELECT title, code, language FROM snippets WHERE title LIKE ? OR code LIKE ?", (f"%{query}%", f"%{query}%"))
    snippets = c.fetchall()
    
    # 5. Search Repos
    c.execute("SELECT name, url, description FROM github_repos WHERE name LIKE ? OR url LIKE ? OR description LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
    repos = c.fetchall()
    conn.close()
    
    print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}              🔍 UNIVERSAL SEARCH RESULTS: '{query}'{Colors.RESET}")
    print(f"{Colors.CYAN}============================================================={Colors.RESET}")
    
    found = False
    if cmds:
        found = True
        print(f"\n{Colors.BOLD}{Colors.GREEN}[Commands]{Colors.RESET}")
        for row in cmds[:5]:
            print(f"  - {row['name']} ({row['command']}): {row['description']}")
            
    if notes:
        found = True
        print(f"\n{Colors.BOLD}{Colors.GREEN}[Notes]{Colors.RESET}")
        for row in notes[:5]:
            print(f"  - {row['title']}: {row['content']}")
            
    if links:
        found = True
        print(f"\n{Colors.BOLD}{Colors.GREEN}[Bookmarks]{Colors.RESET}")
        for row in links[:5]:
            print(f"  - {row['title']} ({row['url']})")
            
    if snippets:
        found = True
        print(f"\n{Colors.BOLD}{Colors.GREEN}[Snippets ({snippets[0]['language']})]{Colors.RESET}")
        for row in snippets[:5]:
            print(f"  - {row['title']}: {row['code'][:100]}...")
            
    if repos:
        found = True
        print(f"\n{Colors.BOLD}{Colors.GREEN}[GitHub Repos]{Colors.RESET}")
        for row in repos[:5]:
            print(f"  - {row['name']} ({row['url']}): {row['description']}")
            
    if not found:
        print(f"  No items matched your search query in notes, commands, links, or snippets.")
    print(f"{Colors.CYAN}============================================================={Colors.RESET}")
    input("\nPress Enter to return to Main Menu...")

def show_dashboard():
    # Gathering Data
    uname = platform.uname()
    now = datetime.datetime.now()
    greeting = get_greeting()
    user_name = os.getlogin()
    
    # System details
    os_name = get_os_caption()
    secure_boot = check_secure_boot()
    bitlocker = check_bitlocker_status()
    firewall = check_firewall_status()
    expiry = check_activation_expiry()
    admin_status = "Admin Mode" if is_admin() else "Standard Mode"
    working_dir = os.getcwd()
    
    # CPU, Memory, Disk
    cpu_usage = psutil.cpu_percent()
    cpufreq = psutil.cpu_freq()
    freq_str = f" @ {cpufreq.current/1000:.2f} GHz" if cpufreq else ""
    cores = psutil.cpu_count(logical=True)
    
    svmem = psutil.virtual_memory()
    disk_desc = "N/A"
    disk_sub = ""
    try:
        c_usage = psutil.disk_usage("C:\\")
        disk_desc = f"Disk C:  {get_size(c_usage.used)} / {get_size(c_usage.total)}"
        disk_bar_len = 8
        disk_blocks = int(c_usage.percent / (100 / disk_bar_len))
        disk_bar = "█" * disk_blocks + "░" * (disk_bar_len - disk_blocks)
        disk_sub = f"         [{disk_bar}] {c_usage.percent}%"
    except Exception:
        pass
        
    # GPU
    gpus_str = "N/A"
    try:
        gpu_out = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "name"], text=True, errors="ignore")
        gpus = [g.strip() for g in gpu_out.split('\n')[1:] if g.strip()]
        if gpus:
            gpus_str = ", ".join(gpus).replace("NVIDIA GeForce ", "Nvidia ").replace("Intel(R) ", "Intel ").split(",")[0].strip()
    except Exception:
        pass
        
    # Temperature
    cpu_temp_val = "N/A"
    try:
        ps_cmd = "Get-Counter -Counter '\\Thermal Zone Information(*)\\Temperature' -ErrorAction Stop | Select-Object -ExpandProperty CounterSamples | ForEach-Object { $_.CookedValue } | Select-Object -First 1"
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0 and res.stdout.strip():
            k_temp = float(res.stdout.strip())
            cpu_temp_val = f"{round(k_temp - 273.15, 1)}°C"
    except Exception:
        pass
        
    gpu_temp_val = "N/A"
    try:
        gpu_temp = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"], text=True, errors="ignore").strip()
        if gpu_temp.isdigit():
            gpu_temp_val = f"{gpu_temp}°C"
    except Exception:
        pass
        
    # Network / Internet
    local_ip = "N/A"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    public_ip = "Fetching..."
    try:
        req = urllib.request.Request("https://api.ipify.org?format=json", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            public_ip = json.loads(resp.read().decode())["ip"]
    except Exception:
        public_ip = "Offline"
        
    # Weather
    weather_info = get_weather()
    
    # VM Statuses
    wsl_status, hyperv_status, vbox_status, vmware_status = get_vms_status()
    
    # Packages
    winget = is_tool_installed("winget")
    npm = is_tool_installed("npm")
    pip = is_tool_installed("pip")
    cargo = is_tool_installed("cargo")
    go = is_tool_installed("go")
    
    # Active server ports check
    docker_status = check_docker_status()
    mysql_status = check_port(3306)
    postgres_status = check_port(5432)
    mongo_status = check_port(27017)
    redis_status = check_port(6379)
    ssh_status = check_port(22)
    apache_status = check_port(80)
    
    # Top CPU / RAM processes
    top_cpu_proc, top_ram_proc = get_top_processes()
    
    # Cleanup recommendations
    cleanup_sugg = get_cleanup_suggestions()
    
    # Device counts
    dev_count = get_connected_devices()

    # Draw double-pane layout grid
    def print_row(left_str, right_str):
        l_padded = f"{left_str:<36}"[:36]
        r_padded = f"{right_str:<36}"[:36]
        print(f"{Colors.CYAN}│{Colors.RESET} {l_padded} {Colors.CYAN}│{Colors.RESET} {r_padded} {Colors.CYAN}│{Colors.RESET}")

    # Header
    print(f"\n{Colors.CYAN}┌──────────────────────────────────────┬──────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET} Welcome back, {Colors.BOLD}{Colors.YELLOW}{user_name:<21}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {Colors.GREEN}{greeting:<36}{Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET} {now.strftime('%A, %d %B %Y %H:%M:%S'):<36} {Colors.CYAN}│{Colors.RESET} Dir: {working_dir[:30]:<31} {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  ⚙️ SYSTEM STATUS & IDENTITY           {Colors.RESET}{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🖥️ HARDWARE TELEMETRY & UTILIZATION  {Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    
    # OS info & CPU
    print_row(f"OS:      {os_name}", f"CPU:     {cores} Logical Cores")
    
    cpu_bar_len = 8
    num_blocks = int(cpu_usage / (100 / cpu_bar_len))
    cpu_bar = "█" * num_blocks + "░" * (cpu_bar_len - num_blocks)
    
    cpu_temp_str = f" | Temp: {cpu_temp_val}" if cpu_temp_val != "N/A" else ""
    print_row(f"Expiry:  {expiry}", f"Load:    [{cpu_bar}] {cpu_usage}%{freq_str}{cpu_temp_str}")
    
    gpu_desc = f"GPU:     {gpus_str}"
    if gpu_temp_val != "N/A":
        gpu_desc += f" | Temp: {gpu_temp_val}"
    print_row(f"Mode:    {admin_status}", gpu_desc)
    
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🛡️ SECURITY & DIAGNOSTICS            {Colors.RESET}{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  💾 MEMORY & STORAGE SPACE            {Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    
    # Security check & Storage space
    print_row(f"Firewall:   {firewall}", f"RAM:     {get_size(svmem.used)} / {get_size(svmem.total)}")
    
    ram_bar_len = 8
    ram_blocks = int(svmem.percent / (100 / ram_bar_len))
    ram_bar = "█" * ram_blocks + "░" * (ram_bar_len - ram_blocks)
    print_row(f"SecureBoot: {secure_boot}", f"         [{ram_bar}] {svmem.percent}%")
    print_row(f"BitLocker:  {bitlocker}", disk_desc)
    print_row("", disk_sub)
    
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🌐 NETWORK & ENVIRONMENT             {Colors.RESET}{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🗄️ LOCAL SERVERS & DATABASES         {Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    
    # Network IP & Databases
    print_row(f"Local IP:  {local_ip}", f"Docker:  {docker_status} ({get_docker_stats()})")
    print_row(f"Public IP: {public_ip}", f"MySQL:   {mysql_status} | PostgreSQL: {postgres_status}")
    print_row(f"Weather:   {weather_info}", f"MongoDB: {mongo_status} | Redis:      {redis_status}")
    print_row("", f"Apache:  {apache_status} | SSH:        {ssh_status}")
    
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🖥️ VIRTUAL MACHINES                  {Colors.RESET}{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  📦 ENVIRONMENTS & SDKS               {Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    
    # Virtual Machines & SDKs
    print_row(f"WSL Distributions: {wsl_status}", f"Winget:  {winget}")
    print_row(f"Hyper-V Status:    {hyperv_status}", f"Node.js: {npm}")
    print_row(f"VMware Workstatn:  {vmware_status}", f"Python:  {pip}")
    print_row(f"VirtualBox VMs:    {vbox_status}", f"Cargo:   {cargo} | Go: {go}")
    
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🔥 ACTIVE LOAD SENSORS               {Colors.RESET}{Colors.CYAN}│{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}  🧹 MAINTENANCE SUGGESTIONS          {Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├──────────────────────────────────────┼──────────────────────────────────────┤{Colors.RESET}")
    
    # Running processes & Cleanups
    print_row(f"Top CPU: {top_cpu_proc}", f"Clean:   {cleanup_sugg}")
    print_row(f"Top RAM: {top_ram_proc}", f"Devices: {dev_count}")
    
    print(f"{Colors.CYAN}└──────────────────────────────────────┴──────────────────────────────────────┘{Colors.RESET}")
    input("\nPress Enter to return to Main Menu...")
