from toolkit.utils import Colors
import os
import sys
import subprocess
import socket
import psutil

HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"

def is_admin():
    try:
        # Requires Windows to check for admin rights
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_website():
    if not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Blocking websites requires Administrator privileges. Please run as Admin.")
        return
    site = input("Enter website domain to block (e.g. facebook.com): ").strip()
    if not site:
        return
    try:
        with open(HOSTS_FILE, 'a') as f:
            f.write(f"\n127.0.0.1\t{site}")
            f.write(f"\n127.0.0.1\twww.{site}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {site} has been blocked via Hosts file.")
        # Flush DNS for immediate effect
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not write to hosts file: {e}")

def unblock_website():
    if not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Unblocking websites requires Administrator privileges. Please run as Admin.")
        return
    site = input("Enter website domain to unblock (e.g. facebook.com): ").strip()
    if not site:
        return
    try:
        with open(HOSTS_FILE, 'r') as f:
            lines = f.readlines()
        with open(HOSTS_FILE, 'w') as f:
            for line in lines:
                if site not in line:
                    f.write(line)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {site} has been unblocked.")
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not modify hosts file: {e}")

def scan_ports():
    print(f"\n{Colors.CYAN}--- Port Scanner ---{Colors.RESET}")
    target = input("Enter target IP or Domain (default localhost): ").strip() or "127.0.0.1"
    start_port = input("Start Port (default 1): ").strip()
    end_port = input("End Port (default 1024): ").strip()
    
    start_port = int(start_port) if start_port.isdigit() else 1
    end_port = int(end_port) if end_port.isdigit() else 1024
    
    print(f"\n[INFO] Scanning {target} from port {start_port} to {end_port}...")
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not resolve host: {target}")
        return
        
    open_ports = []
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"[✓] Port {port} is OPEN")
            open_ports.append(port)
        s.close()
    
    if not open_ports:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No open ports found in range.")
    else:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Found {len(open_ports)} open ports.")

def kill_process():
    print(f"\n{Colors.CYAN}--- Kill Process ---{Colors.RESET}")
    pid = input("Enter Process ID (PID) to kill: ").strip()
    if not pid.isdigit():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid PID.")
        return
    try:
        p = psutil.Process(int(pid))
        p.terminate()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Process {pid} terminated.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not kill process: {e}")

def open_windows_security():
    print("\n[INFO] Opening Windows Security Center...")
    try:
        subprocess.Popen(["windowsdefender:"])
    except:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not launch Windows Security.")

def run_startup_scan():
    print(f"\n{Colors.CYAN}--- Startup Malware Scan ---{Colors.RESET}")
    print("[INFO] Querying Registry run keys and Startup folders...")
    
    suspicious_entries = []
    all_entries = []
    
    # 1. Read Registry Run Keys
    import winreg
    reg_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU\\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM\\Run")
    ]
    
    for hkey, subkey, label in reg_paths:
        try:
            key = winreg.OpenKey(hkey, subkey)
            idx = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, idx)
                    all_entries.append((label, name, val))
                    idx += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass

    # 2. Read Startup Folders
    startup_paths = []
    if 'APPDATA' in os.environ:
        startup_paths.append((os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs\Startup"), "User Startup Folder"))
    if 'ProgramData' in os.environ:
        startup_paths.append((os.path.join(os.environ['ProgramData'], r"Microsoft\Windows\Start Menu\Programs\StartUp"), "Common Startup Folder"))
        
    for path, label in startup_paths:
        if os.path.exists(path):
            try:
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path):
                        all_entries.append((label, f, full_path))
            except Exception:
                pass

    if not all_entries:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No startup entries found to scan.")
        return

    print(f"\nScanning {len(all_entries)} entries against security heuristics...")
    
    suspicious_keywords = ["temp", "tmp", "appdata\\local\\temp", "cmd.exe", "powershell.exe", "wscript.exe", "mshta.exe"]
    suspicious_exts = [".vbs", ".js", ".bat", ".cmd", ".scr", ".pif"]

    for source, name, command in all_entries:
        reasons = []
        cmd_lower = command.lower()
        
        # Heuristic 1: Run from Temp folders
        if "temp" in cmd_lower or "tmp" in cmd_lower:
            reasons.append("Launches from a Temporary directory")
            
        # Heuristic 2: Suspicious extensions
        for ext in suspicious_exts:
            if ext in cmd_lower:
                reasons.append(f"Launches a script file directly ({ext})")
                
        # Heuristic 3: LOLBins / Script engines
        if "wscript.exe" in cmd_lower or "cscript.exe" in cmd_lower:
            reasons.append("Uses Windows Script Host engine")
        if "mshta.exe" in cmd_lower:
            reasons.append("Uses HTA engine to run web applications")
            
        # Heuristic 4: Obfuscated or random name lengths in user directories
        if "appdata" in cmd_lower and len(name) > 15 and name.isalnum():
            # Long alphanumeric name without spaces
            reasons.append("Suspiciously long randomized alphanumeric registry entry name")
            
        if reasons:
            suspicious_entries.append((source, name, command, reasons))

    # Print results
    if not suspicious_entries:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Scan complete! No suspicious startup entries detected.")
    else:
        print(f"\n{Colors.RED}[WARNING] Found {len(suspicious_entries)} potentially suspicious startup entries:{Colors.RESET}")
        for source, name, cmd, reasons in suspicious_entries:
            print(f"\n[{source}] Name: {Colors.BOLD}{name}{Colors.RESET}")
            print(f"  Command: {cmd}")
            print("  Reasons:")
            for r in reasons:
                print(f"    - {Colors.RED}{r}{Colors.RESET}")
                
    input("\nPress Enter to return...")

def manage_firewall_rules():
    if not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Firewall rules management requires Administrator privileges.")
        return
        
    while True:
        print(f"\n{Colors.CYAN}--- Firewall Rules Manager ---{Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Block Port")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Block Application")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            port = input("Enter port number to block: ").strip()
            proto = input("Protocol (TCP/UDP, default TCP): ").strip().upper() or "TCP"
            direction = input("Direction (Inbound/Outbound/Both, default Both): ").strip().lower() or "both"
            
            if not port.isdigit():
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid port.")
                continue
                
            dirs = ["in", "out"] if direction == "both" else ["in"] if direction == "inbound" else ["out"]
            
            try:
                for d in dirs:
                    rule_name = f"Toolkit_Block_Port_{port}_{proto}_{d.upper()}"
                    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 
                           f"name={rule_name}", "dir=" + d, "action=block", f"protocol={proto}", f"localport={port}"]
                    subprocess.run(cmd, check=True)
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Port {port} ({proto}) blocked successfully.")
            except Exception as e:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to add rule: {e}")
                
        elif choice == '2':
            app_path = input("Enter absolute path to Application (.exe): ").strip().replace('"', '')
            if not os.path.exists(app_path):
                print(f"{Colors.RED}[ERROR]{Colors.RESET} File path does not exist.")
                continue
                
            direction = input("Direction (Inbound/Outbound/Both, default Both): ").strip().lower() or "both"
            dirs = ["in", "out"] if direction == "both" else ["in"] if direction == "inbound" else ["out"]
            
            try:
                app_name = os.path.basename(app_path)
                for d in dirs:
                    rule_name = f"Toolkit_Block_App_{app_name}_{d.upper()}"
                    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 
                           f"name={rule_name}", "dir=" + d, "action=block", f"program={app_path}"]
                    subprocess.run(cmd, check=True)
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Application {app_name} blocked successfully.")
            except Exception as e:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to add rule: {e}")

def process_port_mapping():
    print(f"\n{Colors.CYAN}--- Active Network Connections & PIDs ---{Colors.RESET}")
    print(f"{'Proto':<5} | {'Local Address':<21} | {'Remote Address':<21} | {'Status':<12} | {'PID':<5} | Process")
    print("-" * 90)
    
    try:
        connections = psutil.net_connections(kind="inet")
        connections.sort(key=lambda x: x.laddr.port if x.laddr else 0)
        
        for conn in connections:
            proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "*"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "*"
            status = conn.status
            pid = conn.pid or "-"
            
            pname = "-"
            if conn.pid:
                try:
                    p = psutil.Process(conn.pid)
                    pname = p.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pname = "[Access Denied]"
                    
            print(f"{proto:<5} | {laddr:<21} | {raddr:<21} | {status:<12} | {pid:<5} | {pname}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to audit network connections: {e}")

def check_bitlocker_status():
    print(f"\n{Colors.CYAN}--- BitLocker Encryption Status ---{Colors.RESET}")
    # PowerShell is the most reliable way to check BitLocker status
    ps_cmd = "Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, EncryptionPercentage, ProtectionStatus | Format-Table -AutoSize"
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0 and res.stdout.strip():
            print(res.stdout)
        else:
            # Fallback to WMIC path win32_encryptablevolume which is available in Windows Pro
            output = subprocess.check_output(["wmic", "path", "win32_encryptablevolume", "get", "driveletter,protectionstatus"], text=True, errors="ignore")
            lines = [l.strip() for l in output.strip().split("\n") if l.strip()]
            if len(lines) > 1:
                print(output.strip())
            else:
                print(f"{Colors.BLUE}[INFO]{Colors.RESET} BitLocker is not supported on this Windows edition (e.g., Windows Home) or requires Administrator privileges.")
    except Exception:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} BitLocker is not supported on this Windows edition (e.g., Windows Home) or requires Administrator privileges.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [11] SECURITY{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Block Website")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Unblock Website")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Firewall Settings")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Windows Defender")
        print(f"{Colors.GREEN}[5]{Colors.RESET} BitLocker Status")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Hosts File Editor")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Port Scanner")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Kill Process")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Startup Malware Scan")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Windows Security Status")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Firewall Rules Creator")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Active Connections Mapping")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            block_website()
        elif choice == '2':
            unblock_website()
        elif choice == '3':
            subprocess.Popen(["control", "firewall.cpl"])
        elif choice == '4':
            open_windows_security()
        elif choice == '5':
            check_bitlocker_status()
        elif choice == '6':
            if is_admin():
                subprocess.Popen(["notepad", HOSTS_FILE])
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Editing hosts file requires Administrator privileges.")
        elif choice == '7':
            scan_ports()
        elif choice == '8':
            kill_process()
        elif choice == '9':
            run_startup_scan()
        elif choice == '10':
            open_windows_security()
        elif choice == '11':
            manage_firewall_rules()
        elif choice == '12':
            process_port_mapping()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
