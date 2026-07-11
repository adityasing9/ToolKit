from toolkit.utils import Colors
import os
import sys
import time
import psutil
import subprocess

# Global historical list for bandwidth graphing (holds up to 15 data points)
download_history = [0.0] * 15
upload_history = [0.0] * 15

def get_bandwidth_speeds():
    """Calculate upload and download speed over a 1-second interval in KB/s."""
    net1 = psutil.net_io_counters()
    time.sleep(1.0)
    net2 = psutil.net_io_counters()
    
    down_speed = (net2.bytes_recv - net1.bytes_recv) / 1024.0 # KB/s
    up_speed = (net2.bytes_sent - net1.bytes_sent) / 1024.0 # KB/s
    return down_speed, up_speed

def get_dns_servers():
    """Query active DNS servers configured on the system."""
    dns_servers = []
    try:
        ps_cmd = "Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object ServerAddresses -ne $null | Select-Object -ExpandProperty ServerAddresses"
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0:
            dns_servers = [line.strip() for line in res.stdout.split("\n") if line.strip()]
    except Exception:
        pass
    
    if not dns_servers:
        # Fallback to ipconfig parse
        try:
            res = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, errors="ignore")
            for line in res.stdout.split("\n"):
                if "DNS Servers" in line:
                    dns = line.split(":")[-1].strip()
                    if dns: dns_servers.append(dns)
        except Exception:
            pass
            
    return list(set(dns_servers))

def detect_vpn():
    """Scan active interfaces for indicators of active VPN tunnels."""
    vpn_indicators = ["tap", "tun", "vpn", "wireguard", "openvpn", "nord", "forticlient", "tailscale", "zerotier"]
    active_vpns = []
    
    stats = psutil.net_if_stats()
    for interface, stat in stats.items():
        if stat.isup:
            for indicator in vpn_indicators:
                if indicator in interface.lower():
                    active_vpns.append(interface)
                    break
    return active_vpns

def get_blocked_hosts():
    """Scan the local Hosts file for blocked (redirected) web domains."""
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    blocked = []
    if os.path.exists(hosts_path):
        try:
            with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split()
                        if len(parts) >= 2:
                            ip, domain = parts[0], parts[1]
                            if ip in ("127.0.0.1", "0.0.0.0"):
                                blocked.append(domain)
        except Exception:
            pass
    return blocked

def get_ping_latency(host="1.1.1.1"):
    """Ping a host and return round-trip latency in milliseconds."""
    try:
        # Ping once on Windows
        res = subprocess.run(["ping", "-n", "1", "-w", "1000", host], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0:
            for line in res.stdout.split("\n"):
                if "Average =" in line or "time=" in line:
                    parts = line.split()
                    for p in parts:
                        if "time=" in p:
                            return float(p.split("=")[-1].replace("ms", ""))
                        if "Average" in p:
                            # Average = 20ms
                            return float(parts[parts.index(p)+2].replace("ms", "").replace("ms", ""))
    except Exception:
        pass
    return None

def show_top_network_apps():
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Top Apps with Active Connections ==={Colors.RESET}")
    print(f"{'PID':<8} | {'Process Name':<25} | {'Local Connection':<22} | {'Remote Address':<22} | {'Status':<12}")
    print("-" * 95)
    
    try:
        connections = psutil.net_connections(kind='inet')
        displayed = 0
        for conn in connections:
            if conn.raddr and displayed < 25:
                pid = conn.pid
                name = "N/A"
                if pid:
                    try:
                        name = psutil.Process(pid).name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                local = f"{conn.laddr.ip}:{conn.laddr.port}"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}"
                
                print(f"{pid or 'N/A':<8} | {name[:25]:<25} | {local:<22} | {remote:<22} | {conn.status:<12}")
                displayed += 1
        if displayed == 0:
            print("No active remote internet connections found.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not query connections: {e}")

def draw_ascii_graph(history, label):
    """Draw a clean horizontal ASCII sparkline/graph representing bandwidth historical data points."""
    max_val = max(history) if max(history) > 0 else 1.0
    print(f"\n{Colors.BOLD}{Colors.CYAN}[{label} History]{Colors.RESET} (Peak: {max_val:.1f} KB/s)")
    
    # 5 levels of bars
    bar_chars = [" ", "░", "▒", "▓", "█"]
    
    # Render ASCII graph rows
    for level in range(4, -1, -1):
        row_str = "  "
        threshold = (level / 4.0) * max_val
        for val in history:
            if val >= threshold and val > 0:
                row_str += bar_chars[level] + "  "
            else:
                row_str += "   "
        print(row_str)
    print("  " + "  ".join([str(i) for i in range(len(history))]))

def show_network_summary():
    print(f"\n{Colors.CYAN}--- Networking Summary ---{Colors.RESET}")
    print("[INFO] Computing speeds (1s check)...")
    down, up = get_bandwidth_speeds()
    dns = get_dns_servers()
    vpns = detect_vpn()
    latency = get_ping_latency()
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Network Interface Status ==={Colors.RESET}")
    print(f"  Live Download: {Colors.GREEN}{down:.1f} KB/s{Colors.RESET}")
    print(f"  Live Upload:   {Colors.GREEN}{up:.1f} KB/s{Colors.RESET}")
    print(f"  DNS Servers:   {', '.join(dns) if dns else 'N/A'}")
    print(f"  VPN Adapter:   {Colors.MAGENTA if vpns else Colors.RESET}{', '.join(vpns) if vpns else 'None Detected'}{Colors.RESET}")
    print(f"  Ping Latency:  {f'{latency:.1f} ms' if latency else 'Request Timed Out'}")

def show_blocked_connections():
    print(f"\n{Colors.CYAN}--- Blocked Connections (Hosts Redirects) ---{Colors.RESET}")
    blocked = get_blocked_hosts()
    if blocked:
        print(f"{Colors.RED}[WARNING]{Colors.RESET} The following domains are redirected/blocked in your hosts file:")
        for idx, domain in enumerate(blocked[:30], 1):
            print(f"  {idx}. {domain}")
        if len(blocked) > 30:
            print(f"  ... and {len(blocked) - 30} more.")
    else:
        print(f"{Colors.GREEN}[CLEAN]{Colors.RESET} No blocked domain entries found in local hosts file.")

def live_network_monitor():
    global download_history, upload_history
    print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Starting Live Network Monitor. Press Ctrl+C to exit.")
    time.sleep(1.5)
    
    try:
        while True:
            # Measure delta speed
            down, up = get_bandwidth_speeds()
            
            # Shift historical arrays
            download_history.pop(0)
            download_history.append(down)
            upload_history.pop(0)
            upload_history.append(up)
            
            # Check pings & interfaces
            latency = get_ping_latency()
            vpns = detect_vpn()
            dns = get_dns_servers()
            
            # Clear console
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}                    🌎 LIVE NETWORK MONITOR{Colors.RESET}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"  Download Speed : {Colors.GREEN}{down:<10.1f} KB/s{Colors.RESET}")
            print(f"  Upload Speed   : {Colors.GREEN}{up:<10.1f} KB/s{Colors.RESET}")
            print(f"  Ping Latency   : {Colors.GREEN}{f'{latency:.1f} ms' if latency else 'Timed Out':<10}{Colors.RESET}")
            print(f"  Active VPN     : {Colors.MAGENTA}{vpns[0] if vpns else 'None':<15}{Colors.RESET}")
            print(f"  Configured DNS : {', '.join(dns[:2]) if dns else 'N/A'}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            
            # Draw ASCII Sparklines
            draw_ascii_graph(download_history, "Download Bandwidth")
            draw_ascii_graph(upload_history, "Upload Bandwidth")
            
            print(f"\n{Colors.BLUE}Press Ctrl+C to terminate monitor and return to menu.{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n[INFO] Live Network Monitor stopped.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [21] NETWORK MONITOR{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Live Network Speed & Ping Summary")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Top Apps & Active Connections")
        print(f"{Colors.GREEN}[3]{Colors.RESET} View Blocked Domains (Hosts Scan)")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Launch Live Graphical Bandwidth Monitor")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            show_network_summary()
            input("\nPress Enter to continue...")
        elif choice == '2':
            show_top_network_apps()
            input("\nPress Enter to continue...")
        elif choice == '3':
            show_blocked_connections()
            input("\nPress Enter to continue...")
        elif choice == '4':
            live_network_monitor()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
