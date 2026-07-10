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
        print("[ERROR] Blocking websites requires Administrator privileges. Please run as Admin.")
        return
    site = input("Enter website domain to block (e.g. facebook.com): ").strip()
    if not site:
        return
    try:
        with open(HOSTS_FILE, 'a') as f:
            f.write(f"\n127.0.0.1\t{site}")
            f.write(f"\n127.0.0.1\twww.{site}")
        print(f"[SUCCESS] {site} has been blocked via Hosts file.")
        # Flush DNS for immediate effect
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    except Exception as e:
        print(f"[ERROR] Could not write to hosts file: {e}")

def unblock_website():
    if not is_admin():
        print("[ERROR] Unblocking websites requires Administrator privileges. Please run as Admin.")
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
        print(f"[SUCCESS] {site} has been unblocked.")
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    except Exception as e:
        print(f"[ERROR] Could not modify hosts file: {e}")

def scan_ports():
    print("\n--- Port Scanner ---")
    target = input("Enter target IP or Domain (default localhost): ").strip() or "127.0.0.1"
    start_port = input("Start Port (default 1): ").strip()
    end_port = input("End Port (default 1024): ").strip()
    
    start_port = int(start_port) if start_port.isdigit() else 1
    end_port = int(end_port) if end_port.isdigit() else 1024
    
    print(f"\n[INFO] Scanning {target} from port {start_port} to {end_port}...")
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[ERROR] Could not resolve host: {target}")
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
        print("[INFO] No open ports found in range.")
    else:
        print(f"[SUCCESS] Found {len(open_ports)} open ports.")

def kill_process():
    print("\n--- Kill Process ---")
    pid = input("Enter Process ID (PID) to kill: ").strip()
    if not pid.isdigit():
        print("[ERROR] Invalid PID.")
        return
    try:
        p = psutil.Process(int(pid))
        p.terminate()
        print(f"[SUCCESS] Process {pid} terminated.")
    except Exception as e:
        print(f"[ERROR] Could not kill process: {e}")

def open_windows_security():
    print("\n[INFO] Opening Windows Security Center...")
    try:
        subprocess.Popen(["windowsdefender:"])
    except:
        print("[ERROR] Could not launch Windows Security.")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [4] SECURITY")
        print("=============================================================")
        print("[1] Block Website")
        print("[2] Unblock Website")
        print("[3] Firewall Settings")
        print("[4] Windows Defender")
        print("[5] BitLocker Status")
        print("[6] Hosts File Editor")
        print("[7] Port Scanner")
        print("[8] Kill Process")
        print("[9] Startup Malware Scan")
        print("[10] Windows Security Status")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            block_website()
        elif choice == '2':
            unblock_website()
        elif choice == '3':
            subprocess.Popen(["firewall.cpl"])
        elif choice == '4':
            open_windows_security()
        elif choice == '5':
            subprocess.Popen(["control", "/name", "Microsoft.BitLockerDriveEncryption"])
        elif choice == '6':
            if is_admin():
                subprocess.Popen(["notepad", HOSTS_FILE])
            else:
                print("[ERROR] Editing hosts file requires Administrator privileges.")
        elif choice == '7':
            scan_ports()
        elif choice == '8':
            kill_process()
        elif choice == '9':
            print("[INFO] Startup Malware Scan coming soon...")
        elif choice == '10':
            open_windows_security()
        else:
            print("[ERROR] Invalid choice.")
