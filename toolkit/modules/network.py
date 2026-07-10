import os
import socket
import subprocess
import requests

def get_public_ip():
    print("\n[INFO] Fetching Public IP...")
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip = response.json().get("ip")
        print(f"[SUCCESS] Public IP: {ip}")
    except Exception as e:
        print(f"[ERROR] Could not fetch Public IP: {e}")

def get_local_ip():
    print("\n[INFO] Fetching Local IP...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"[SUCCESS] Local IP: {ip}")
    except Exception as e:
        print(f"[ERROR] Could not fetch Local IP: {e}")

def get_mac_address():
    print("\n[INFO] Fetching MAC Addresses...")
    try:
        output = subprocess.check_output(["getmac"], text=True)
        print(output.strip())
    except Exception as e:
        print(f"[ERROR] Could not fetch MAC Address: {e}")

def run_ping():
    host = input("Enter host to ping (e.g. google.com): ").strip()
    if host:
        subprocess.run(["ping", host])

def run_traceroute():
    host = input("Enter host for traceroute (e.g. google.com): ").strip()
    if host:
        subprocess.run(["tracert", host])

def check_wifi_passwords():
    print("\n--- Saved WiFi Passwords ---")
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], text=True)
        profiles = []
        for line in output.split('\n'):
            if "All User Profile" in line:
                profiles.append(line.split(":")[1].strip())
        
        if not profiles:
            print("[INFO] No saved WiFi profiles found.")
            return

        for profile in profiles:
            try:
                prof_output = subprocess.check_output(["netsh", "wlan", "show", "profile", f'name="{profile}"', "key=clear"], text=True)
                password = "None"
                for pline in prof_output.split('\n'):
                    if "Key Content" in pline:
                        password = pline.split(":")[1].strip()
                        break
                print(f"Network: {profile:<20} | Password: {password}")
            except subprocess.CalledProcessError:
                print(f"Network: {profile:<20} | Password: [ERROR READING]")
    except Exception as e:
        print(f"[ERROR] Could not fetch WiFi passwords: {e}")

def check_open_ports():
    print("\n--- Active Connections & Open Ports ---")
    try:
        subprocess.run(["netstat", "-ano"])
    except Exception as e:
        print(f"[ERROR] Could not run netstat: {e}")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [5] NETWORKING")
        print("=============================================================")
        print("[1] Public IP")
        print("[2] Local IP")
        print("[3] MAC Address")
        print("[4] DNS Configuration")
        print("[5] Flush DNS")
        print("[6] Ping")
        print("[7] Traceroute")
        print("[8] Port Check")
        print("[9] WiFi Passwords")
        print("[10] Connected Devices")
        print("[11] Open Ports")
        print("[12] Network Speed Test")
        print("[13] Proxy Settings")
        print("[14] VPN Status")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            get_public_ip()
        elif choice == '2':
            get_local_ip()
        elif choice == '3':
            get_mac_address()
        elif choice == '4':
            subprocess.run(["ipconfig", "/all"])
        elif choice == '5':
            subprocess.run(["ipconfig", "/flushdns"])
        elif choice == '6':
            run_ping()
        elif choice == '7':
            run_traceroute()
        elif choice == '8':
            print("[INFO] Use the Port Scanner in the [4] Security module.")
        elif choice == '9':
            check_wifi_passwords()
        elif choice == '10':
            subprocess.run(["arp", "-a"])
        elif choice == '11':
            check_open_ports()
        elif choice == '12':
            print("[INFO] Network Speed Test coming soon...")
        elif choice == '13':
            print("[INFO] Proxy Settings coming soon...")
        elif choice == '14':
            print("[INFO] VPN Status coming soon...")
        else:
            print("[ERROR] Invalid choice.")
