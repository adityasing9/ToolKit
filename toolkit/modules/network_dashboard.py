from toolkit.utils import Colors
import os
import sys
import time
import socket
import psutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Common MAC OUI prefixes to identify vendors
MAC_VENDORS = {
    "00:00:0c": "Cisco",
    "00:01:42": "Cisco",
    "00:03:93": "Apple",
    "00:05:02": "Apple",
    "00:0d:93": "Apple",
    "00:11:24": "Apple",
    "00:17:f2": "Apple",
    "00:1c:b3": "Apple",
    "00:1e:c2": "Apple",
    "00:23:12": "Apple",
    "00:25:00": "Apple",
    "00:26:08": "Apple",
    "00:26:b0": "Apple",
    "1c:1a:c0": "Apple",
    "1c:ab:a7": "Apple",
    "28:cf:e9": "Apple",
    "3c:07:54": "Apple",
    "3c:15:c2": "Apple",
    "40:30:04": "Apple",
    "48:d7:05": "Apple",
    "5c:96:9d": "Apple",
    "60:c5:47": "Apple",
    "7c:d1:c3": "Apple",
    "8c:fe:57": "Apple",
    "a4:77:33": "Apple",
    "b8:c7:5d": "Apple",
    "c8:bc:c8": "Apple",
    "d8:a2:5e": "Apple",
    "e0:c9:7a": "Apple",
    "e4:25:e7": "Apple",
    "f0:18:98": "Apple",
    "f4:0f:24": "Apple",
    "fc:fc:48": "Apple",
    "00:00:f0": "Samsung",
    "00:07:ab": "Samsung",
    "00:09:c3": "Samsung",
    "00:0f:73": "Samsung",
    "00:12:47": "Samsung",
    "00:12:fb": "Samsung",
    "00:15:b9": "Samsung",
    "00:17:c9": "Samsung",
    "00:18:af": "Samsung",
    "00:1a:8a": "Samsung",
    "00:1c:c6": "Samsung",
    "00:1d:25": "Samsung",
    "00:1e:7d": "Samsung",
    "00:1f:df": "Samsung",
    "00:21:19": "Samsung",
    "00:21:d2": "Samsung",
    "00:23:3a": "Samsung",
    "00:23:d6": "Samsung",
    "00:24:54": "Samsung",
    "00:24:90": "Samsung",
    "00:25:14": "Samsung",
    "00:25:67": "Samsung",
    "00:26:37": "Samsung",
    "00:27:3d": "Samsung",
    "1c:5a:3e": "Samsung",
    "24:f5:aa": "Samsung",
    "38:2d:e8": "Samsung",
    "40:2b:a1": "Samsung",
    "48:5a:3f": "Samsung",
    "50:56:a8": "Samsung",
    "5c:a3:9d": "Samsung",
    "84:51:84": "Samsung",
    "ac:5f:3e": "Samsung",
    "c4:73:1e": "Samsung",
    "d0:22:be": "Samsung",
    "e4:7c:f5": "Samsung",
    "f0:e7:7e": "Samsung",
    "f4:f5:db": "Samsung",
    "00:00:e2": "Acer",
    "00:01:e6": "Hewlett-Packard",
    "00:08:02": "Hewlett-Packard",
    "00:0f:20": "Hewlett-Packard",
    "00:10:83": "Hewlett-Packard",
    "00:11:0a": "Hewlett-Packard",
    "00:11:85": "Hewlett-Packard",
    "00:12:79": "Hewlett-Packard",
    "00:13:21": "Hewlett-Packard",
    "00:14:38": "Hewlett-Packard",
    "00:15:60": "Hewlett-Packard",
    "00:16:35": "Hewlett-Packard",
    "00:17:08": "Hewlett-Packard",
    "00:18:71": "Hewlett-Packard",
    "00:19:bb": "Hewlett-Packard",
    "00:1a:4b": "Hewlett-Packard",
    "00:1b:78": "Hewlett-Packard",
    "00:1c:c4": "Hewlett-Packard",
    "00:1e:0b": "Hewlett-Packard",
    "00:1f:29": "Hewlett-Packard",
    "00:21:f6": "Hewlett-Packard",
    "00:22:64": "Hewlett-Packard",
    "00:23:7d": "Hewlett-Packard",
    "00:24:81": "Hewlett-Packard",
    "00:25:b3": "Hewlett-Packard",
    "00:26:55": "Hewlett-Packard",
    "2c:59:e5": "Hewlett-Packard",
    "3c:d9:2b": "Hewlett-Packard",
    "3c:a8:2a": "Hewlett-Packard",
    "40:a8:f0": "Hewlett-Packard",
    "48:0f:cf": "Hewlett-Packard",
    "5c:b9:01": "Hewlett-Packard",
    "70:5a:b6": "Hewlett-Packard",
    "88:51:fb": "Hewlett-Packard",
    "9c:b6:54": "Hewlett-Packard",
    "a4:5d:36": "Hewlett-Packard",
    "b8:38:61": "Hewlett-Packard",
    "c8:d9:fc": "Hewlett-Packard",
    "d4:c9:ef": "Hewlett-Packard",
    "e0:db:55": "Hewlett-Packard",
    "e8:39:35": "Hewlett-Packard",
    "f4:30:b9": "Hewlett-Packard",
    "fc:15:b4": "Hewlett-Packard",
    "00:03:ff": "Microsoft",
    "00:0d:3a": "Microsoft",
    "00:12:5a": "Microsoft",
    "00:15:5d": "Microsoft",
    "00:17:fa": "Microsoft",
    "00:1d:d8": "Microsoft",
    "00:22:48": "Microsoft",
    "00:25:ae": "Microsoft",
    "00:50:f2": "Microsoft",
    "28:18:78": "Microsoft",
    "30:59:b7": "Microsoft",
    "48:51:b7": "Microsoft",
    "58:82:a8": "Microsoft",
    "60:45:bd": "Microsoft",
    "7c:ed:8d": "Microsoft",
    "94:9b:2c": "Microsoft",
    "9c:aa:1b": "Microsoft",
    "b8:31:b5": "Microsoft",
    "c4:9a:02": "Microsoft",
    "e8:9d:87": "Microsoft",
    "f0:1f:af": "Microsoft",
    "f4:a8:0d": "Microsoft",
    "f8:86:a8": "Microsoft",
    "fc:db:b3": "Microsoft",
    "00:0c:29": "VMware",
    "00:50:56": "VMware",
    "00:05:69": "VMware",
    "00:1c:14": "VMware",
    "00:10:fa": "Sony",
    "00:13:15": "Sony",
    "00:19:c5": "Sony",
    "00:1d:ba": "Sony",
    "00:1e:dc": "Sony",
    "00:24:be": "Sony",
    "00:25:4d": "Sony",
    "28:0d:fc": "Sony",
    "3c:07:71": "Sony",
    "70:9e:29": "Sony",
    "78:84:3c": "Sony",
    "a4:70:d6": "Sony",
    "b4:c4:fc": "Sony",
    "c4:36:6c": "Sony",
    "d0:17:c2": "Sony",
    "d8:c4:6a": "Sony",
    "e4:22:fb": "Sony",
    "e8:04:10": "Sony",
    "fc:0f:e6": "Sony",
    "00:08:9b": "Synology",
    "00:11:32": "Synology",
    "00:11:3f": "Synology",
    "00:22:4c": "Synology",
    "00:07:89": "Synology",
    "00:08:a1": "Synology",
    "90:09:d0": "Synology",
    "00:07:3b": "Tenovis",
    "00:17:88": "Philips",
    "00:1c:25": "Intel",
    "00:1d:e0": "Intel",
    "00:1e:64": "Intel",
    "00:1e:65": "Intel",
    "00:1f:3c": "Intel",
    "00:21:5c": "Intel",
    "00:21:6a": "Intel",
    "00:21:6b": "Intel",
    "00:22:fa": "Intel",
    "00:23:14": "Intel",
    "00:23:15": "Intel",
    "00:24:d6": "Intel",
    "00:24:d7": "Intel",
    "00:27:0e": "Intel",
    "00:27:10": "Intel",
    "30:b4:9e": "Intel",
    "3c:58:c2": "Intel",
    "40:25:c2": "Intel",
    "48:51:c5": "Intel",
    "58:91:cf": "Intel",
    "5c:51:4f": "Intel",
    "70:77:81": "Intel",
    "7c:5c:f8": "Intel",
    "88:b1:11": "Intel",
    "94:e9:79": "Intel",
    "a4:34:d9": "Intel",
    "b8:70:f4": "Intel",
    "c8:5b:76": "Intel",
    "d0:7e:35": "Intel",
    "e4:a7:a0": "Intel",
    "f8:16:54": "Intel",
    "fc:aa:14": "Intel",
    "00:03:2f": "Linksys",
    "00:06:25": "Linksys",
    "00:0c:41": "Linksys",
    "00:0f:66": "Linksys",
    "00:14:bf": "Linksys",
    "00:18:39": "Linksys",
    "00:18:f8": "Linksys",
    "00:21:29": "Linksys",
    "00:22:6b": "Linksys",
    "00:23:69": "Linksys",
    "00:25:9c": "Linksys",
    "00:14:6c": "Linksys",
    "00:1c:10": "Cisco Linksys",
    "00:1d:7e": "Cisco Linksys",
    "00:22:6c": "Cisco Linksys",
    "00:01:38": "Xerox",
    "00:03:68": "Canon",
    "00:17:08": "Canon",
    "00:1e:8f": "Canon",
    "00:00:86": "Megahertz",
    "00:00:f8": "DEC",
    "00:00:39": "Toshiba",
    "00:08:c7": "HP",
    "00:0b:cd": "HP",
    "00:0c:6e": "HP",
    "00:0d:9d": "HP",
    "00:0e:7f": "HP",
    "00:0f:3d": "HP",
    "00:10:1f": "HP",
    "00:11:43": "HP",
    "00:12:79": "HP",
    "00:13:21": "HP",
    "00:14:38": "HP",
    "00:15:60": "HP",
    "00:16:35": "HP",
    "00:17:08": "HP",
    "00:18:71": "HP",
    "00:19:bb": "HP",
    "00:1a:4b": "HP",
    "00:1b:78": "HP",
    "00:1c:c4": "HP",
    "00:1e:0b": "HP",
    "00:1f:29": "HP",
    "00:21:f6": "HP",
    "00:22:64": "HP",
    "00:23:7d": "HP",
    "00:24:81": "HP",
    "00:25:b3": "HP",
    "00:26:55": "HP",
    "00:18:fe": "Hewlett Packard",
    "00:1a:0b": "Hewlett Packard",
    "00:22:c2": "Hewlett Packard",
    "00:24:0b": "Hewlett Packard",
    "00:25:31": "Hewlett Packard",
    "00:25:61": "Hewlett Packard",
    "00:26:f2": "Hewlett Packard",
    "00:27:0e": "Hewlett Packard",
    "00:27:0f": "Hewlett Packard",
    "00:30:c1": "Hewlett Packard",
    "00:02:b3": "Intel",
    "00:03:47": "Intel",
    "00:04:23": "Intel",
    "00:08:74": "Intel",
    "00:0c:f1": "Intel",
    "00:0e:0c": "Intel",
    "00:11:75": "Intel",
    "00:13:02": "Intel",
    "00:13:20": "Intel",
    "00:13:72": "Intel",
    "00:15:00": "Intel",
    "00:15:c5": "Intel",
    "00:16:76": "Intel",
    "00:16:eb": "Intel",
    "00:17:c4": "Intel",
    "00:18:de": "Intel",
    "00:19:d1": "Intel",
    "00:1a:11": "Intel",
    "00:1b:21": "Intel",
    "00:1b:77": "Intel",
    "00:1b:fc": "Intel",
    "00:1c:bf": "Intel",
    "00:1c:c0": "Intel",
    "00:1c:c1": "Intel",
    "00:1c:c2": "Intel",
    "00:1d:09": "Intel",
    "00:1d:60": "Intel",
    "00:1d:73": "Intel",
    "00:1d:92": "Intel",
    "00:1d:c9": "Intel",
    "00:00:b4": "Edimax",
    "00:0e:a6": "Asustek",
    "00:0f:ea": "Asustek",
    "00:11:d8": "Asustek",
    "00:13:d4": "Asustek",
    "00:15:f2": "Asustek",
    "00:17:31": "Asustek",
    "00:18:f3": "Asustek",
    "00:1a:92": "Asustek",
    "00:1b:fc": "Asustek",
    "00:1c:c0": "Asustek",
    "00:1c:c1": "Asustek",
    "00:1c:c2": "Asustek",
    "00:1d:60": "Asustek",
    "00:1d:73": "Asustek",
    "00:1d:92": "Asustek",
    "00:1d:c9": "Asustek",
    "00:1e:8c": "Asustek",
    "00:1f:c6": "Asustek",
    "00:22:15": "Asustek",
    "00:23:54": "Asustek",
    "00:24:8c": "Asustek",
    "00:26:18": "Asustek",
    "1c:87:2c": "Asustek",
    "38:2c:4a": "Asustek",
    "50:46:5d": "Asustek",
    "a0:1b:29": "Asustek",
    "ac:22:0b": "Asustek",
    "b0:6e:bf": "Asustek",
    "c8:60:00": "Asustek",
    "d8:50:e6": "Asustek",
    "e0:3f:49": "Asustek",
    "e8:9a:8f": "Asustek",
    "f0:79:59": "Asustek",
    "fc:c2:de": "Asustek",
    "00:0d:0b": "Netgear",
    "00:0e:2e": "Netgear",
    "00:0f:b5": "Netgear",
    "00:14:6c": "Netgear",
    "00:18:4d": "Netgear",
    "00:1b:2f": "Netgear",
    "00:1e:2a": "Netgear",
    "00:1f:33": "Netgear",
    "00:22:3f": "Netgear",
    "00:24:b2": "Netgear",
    "00:26:f2": "Netgear",
    "00:30:91": "Netgear",
    "20:4e:7f": "Netgear",
    "28:80:88": "Netgear",
    "3c:37:86": "Netgear",
    "44:94:fc": "Netgear",
    "50:6a:03": "Netgear",
    "78:d6:f0": "Netgear",
    "84:1b:5e": "Netgear",
    "9c:c9:eb": "Netgear",
    "a0:04:60": "Netgear",
    "b0:7f:b9": "Netgear",
    "c0:3f:0e": "Netgear",
    "e0:46:9a": "Netgear",
    "e0:91:f5": "Netgear",
    "f0:7d:68": "Netgear",
    "fc:ec:da": "Netgear",
    "00:0a:eb": "TP-Link",
    "00:14:78": "TP-Link",
    "00:1d:0f": "TP-Link",
    "00:21:27": "TP-Link",
    "00:23:cd": "TP-Link",
    "00:25:86": "TP-Link",
    "14:cf:92": "TP-Link",
    "18:a6:f7": "TP-Link",
    "18:d6:c7": "TP-Link",
    "30:b5:c2": "TP-Link",
    "3c:46:d8": "TP-Link",
    "3c:84:3d": "TP-Link",
    "40:16:9f": "TP-Link",
    "44:d9:e7": "TP-Link",
    "50:3e:aa": "TP-Link",
    "50:c7:bf": "TP-Link",
    "60:e3:27": "TP-Link",
    "70:4f:57": "TP-Link",
    "74:da:38": "TP-Link",
    "7c:8b:ca": "TP-Link",
    "84:16:f9": "TP-Link",
    "8c:21:0a": "TP-Link",
    "90:f6:52": "TP-Link",
    "98:de:d0": "TP-Link",
    "a0:f3:c1": "TP-Link",
    "b0:48:7a": "TP-Link",
    "b0:95:75": "TP-Link",
    "c0:25:e9": "TP-Link",
    "c0:4a:00": "TP-Link",
    "e8:94:f6": "TP-Link",
    "ec:08:6b": "TP-Link",
    "f4:ec:38": "TP-Link",
    "f8:1a:67": "TP-Link",
    "fc:d7:33": "TP-Link"
}

def get_local_subnet():
    """Retrieve the primary local IPv4 address and calculate the scanning range."""
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        # Check active interfaces
        stats = psutil.net_if_stats().get(interface)
        if stats and stats.isup:
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    ip = addr.address
                    netmask = addr.netmask
                    if netmask == "255.255.255.0": # /24 Subnet
                        prefix = ".".join(ip.split(".")[:3])
                        return prefix, ip
    # Fallback default
    return "192.168.1", "192.168.1.1"

def ping_ip(ip):
    """Ping a single IP address to populate the local ARP table."""
    try:
        # Run brief ping sweep
        res = subprocess.run(["ping", "-n", "1", "-w", "150", ip], capture_output=True, text=True)
        if res.returncode == 0:
            return ip
    except Exception:
        pass
    return None

def parse_arp_table():
    """Execute 'arp -a' and parse the results mapping IPs to MACs."""
    arp_map = {}
    try:
        res = subprocess.run(["arp", "-a"], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0:
            for line in res.stdout.split("\n"):
                parts = line.strip().split()
                if len(parts) >= 3:
                    ip = parts[0]
                    mac = parts[1].replace("-", ":").lower()
                    # Validate IP & MAC format
                    if mac.count(":") == 5:
                        arp_map[ip] = mac
    except Exception:
        pass
    return arp_map

def resolve_hostname(ip):
    """Retrieve hostname via reverse DNS lookup."""
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return host
    except Exception:
        return "N/A"

def resolve_vendor(mac):
    """Look up manufacturer/vendor based on MAC OUI prefix."""
    prefix = ":".join(mac.split(":")[:3]).lower()
    for key, vendor in MAC_VENDORS.items():
        if key.lower() == prefix:
            return vendor
    return "Unknown Vendor"

def classify_device(ip, hostname, vendor):
    """Classify the device category by analyzing hostname and vendor labels."""
    comb = f"{hostname} {vendor}".lower()
    
    # Router check (typically .1 or .254)
    if ip.endswith(".1") or ip.endswith(".254") or "router" in comb or "gateway" in comb:
        return "Router"
    
    # TV / Media
    if any(k in comb for k in ["sony", "lg", "tcl", "tv", "vizio", "chromecast", "firestick", "roku", "shield"]):
        return "TV/Media"
        
    # Phone / Tablet
    if any(k in comb for k in ["iphone", "ipad", "android", "samsung", "galaxy", "oneplus", "xiaomi", "mobile", "phone"]):
        return "Phone"
        
    # Printer
    if any(k in comb for k in ["printer", "hp", "epson", "canon", "brother", "lexmark", "laserjet"]):
        return "Printer"
        
    # NAS
    if any(k in comb for k in ["synology", "qnap", "nas", "unraid", "truenas", "storage"]):
        return "NAS"
        
    # Fallback to Laptop/PC
    return "Laptop/PC"

def get_ping_latency(ip):
    """Check response latency for active device."""
    try:
        t1 = time.perf_counter()
        socket.create_connection((ip, 80), timeout=0.15)
        return f"{round((time.perf_counter() - t1) * 1000, 1)} ms"
    except Exception:
        # Fallback ICMP
        try:
            res = subprocess.run(["ping", "-n", "1", "-w", "150", ip], capture_output=True, text=True)
            if res.returncode == 0:
                for line in res.stdout.split("\n"):
                    if "time=" in line:
                        t = line.split("time=")[-1].split()[0].replace("ms", "")
                        return f"{t} ms"
        except Exception:
            pass
    return "< 5 ms"

def scan_network():
    print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}              🌎 LOCAL NETWORK DEVICE DISCOVERY{Colors.RESET}")
    print(f"{Colors.CYAN}============================================================={Colors.RESET}")
    
    prefix, local_ip = get_local_subnet()
    print(f"[INFO] Local Subnet Detected: {Colors.GREEN}{prefix}.0/24{Colors.RESET} (Local IP: {local_ip})")
    print("[INFO] Launching multithreaded ping sweep (254 targets)... Please wait.")
    
    # Scan 1 to 254
    targets = [f"{prefix}.{i}" for i in range(1, 255)]
    active_ips = []
    
    # Thread pool sweep
    with ThreadPoolExecutor(max_workers=65) as executor:
        results = executor.map(ping_ip, targets)
        for ip in results:
            if ip:
                active_ips.append(ip)
                
    print(f"[INFO] Ping sweep completed. Parsing dynamic ARP caches...")
    time.sleep(0.5) # Wait for cache mappings
    arp_map = parse_arp_table()
    
    # Compile discovered devices
    devices = []
    print("[INFO] Resolving hostnames and hardware manufacturers...")
    
    # Include localhost PC details
    local_mac = "N/A"
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                local_mac = addr.address.replace("-", ":").lower()
                
    devices.append({
        "ip": local_ip,
        "mac": local_mac,
        "vendor": "Local PC",
        "hostname": socket.gethostname(),
        "type": "Laptop/PC",
        "ping": "Localhost"
    })
    
    for ip in active_ips:
        if ip == local_ip:
            continue
        mac = arp_map.get(ip, "Unknown MAC")
        vendor = resolve_vendor(mac) if mac != "Unknown MAC" else "Unknown"
        hostname = resolve_hostname(ip)
        dtype = classify_device(ip, hostname, vendor)
        latency = get_ping_latency(ip)
        
        devices.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor,
            "hostname": hostname,
            "type": dtype,
            "ping": latency
        })
        
    # Render table dashboard
    print(f"\n{Colors.BOLD}{Colors.GREEN}=== Discovered Network Devices ({len(devices)}) ==={Colors.RESET}")
    header = f"{'Device Type':<12} | {'IP Address':<15} | {'MAC Address':<17} | {'Ping':<10} | {'Manufacturer / Vendor':<20} | {'Hostname':<20}"
    border = "-" * len(header)
    print(header)
    print(border)
    
    # Print sorted by device type then IP
    devices.sort(key=lambda x: (x["type"], x["ip"]))
    for d in devices:
        row = f"{d['type']:<12} | {d['ip']:<15} | {d['mac']:<17} | {d['ping']:<10} | {d['vendor'][:20]:<20} | {d['hostname'][:20]:<20}"
        print(row)
    print(border)

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [25] LOCAL NETWORK DASHBOARD{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Scan Local Subnet Devices")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            scan_network()
            input("\nPress Enter to continue...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
