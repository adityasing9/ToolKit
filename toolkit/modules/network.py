from toolkit.utils import Colors
import os
import socket
import subprocess
import requests

def get_public_ip():
    print("\n[INFO] Fetching Public IP...")
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip = response.json().get("ip")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Public IP: {ip}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch Public IP: {e}")

def get_local_ip():
    print("\n[INFO] Fetching Local IP...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Local IP: {ip}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch Local IP: {e}")

def get_mac_address():
    print("\n[INFO] Fetching MAC Addresses...")
    try:
        output = subprocess.check_output(["getmac"], text=True)
        print(output.strip())
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch MAC Address: {e}")

def run_ping():
    host = input("Enter host to ping (e.g. google.com): ").strip()
    if host:
        subprocess.run(["ping", host])

def run_traceroute():
    host = input("Enter host for traceroute (e.g. google.com): ").strip()
    if host:
        subprocess.run(["tracert", host])

def check_wifi_passwords():
    print(f"\n{Colors.CYAN}--- Saved WiFi Passwords ---{Colors.RESET}")
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], text=True)
        profiles = []
        for line in output.split('\n'):
            if "All User Profile" in line:
                profiles.append(line.split(":")[1].strip())
        
        if not profiles:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No saved WiFi profiles found.")
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
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch WiFi passwords: {e}")

def check_open_ports():
    print(f"\n{Colors.CYAN}--- Active Connections & Open Ports ---{Colors.RESET}")
    try:
        subprocess.run(["netstat", "-ano"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not run netstat: {e}")

def dns_whois_lookup():
    domain = input("Enter domain name (e.g. google.com): ").strip()
    if not domain:
        return
        
    print(f"\n{Colors.CYAN}--- DNS Lookup ({domain}) ---{Colors.RESET}")
    try:
        ips = socket.gethostbyname_ex(domain)
        print(f"Hostname: {ips[0]}")
        if ips[1]:
            print(f"Aliases:  {', '.join(ips[1])}")
        print(f"IPs:      {', '.join(ips[2])}")
    except Exception as e:
        print(f"DNS lookup failed: {e}")
        
    print(f"\n{Colors.CYAN}--- WHOIS/RDAP Registration Info ---{Colors.RESET}")
    try:
        import requests
        url = f"https://rdap.org/domain/{domain}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            events = data.get("events", [])
            for event in events:
                action = event.get("eventAction", "")
                date = event.get("eventDate", "")
                print(f"  {action.capitalize()}: {date}")
                
            entities = data.get("entities", [])
            for ent in entities:
                roles = ent.get("roles", [])
                if "registrar" in roles:
                    print(f"  Registrar: {ent.get('handle')}")
        else:
            print(f"  No WHOIS data found or server returned error code {r.status_code}.")
    except Exception as e:
        print(f"  WHOIS lookup failed: {e}")

import time
import urllib.request

def run_speed_test():
    print(f"\n{Colors.CYAN}--- Network Speed Test ---{Colors.RESET}")
    print("[INFO] Downloading a 10MB test file from Cloudflare speed test server...")
    url = "https://speed.cloudflare.com/__down?bytes=10000000"
    start_time = time.time()
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            _ = r.read()
        duration = time.time() - start_time
        speed_mbps = (10 * 8) / duration
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Download Speed: {speed_mbps:.2f} Mbps")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Speed test failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [7] NETWORKING{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Public IP")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Local IP")
        print(f"{Colors.GREEN}[3]{Colors.RESET} MAC Address")
        print(f"{Colors.GREEN}[4]{Colors.RESET} DNS Configuration")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Flush DNS")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Ping")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Traceroute")
        print(f"{Colors.GREEN}[8]{Colors.RESET} DNS & WHOIS Lookup")
        print(f"{Colors.GREEN}[9]{Colors.RESET} WiFi Passwords")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Connected Devices")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Open Ports")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Network Speed Test")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Proxy Settings")
        print(f"{Colors.GREEN}[14]{Colors.RESET} VPN Status")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
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
            dns_whois_lookup()
        elif choice == '9':
            check_wifi_passwords()
        elif choice == '10':
            subprocess.run(["arp", "-a"])
        elif choice == '11':
            check_open_ports()
        elif choice == '12':
            run_speed_test()
        elif choice == '13':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Proxy Settings coming soon...")
        elif choice == '14':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} VPN Status coming soon...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
