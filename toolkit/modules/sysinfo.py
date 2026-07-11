from toolkit.utils import Colors
import psutil
import platform
import subprocess
import os

def get_size(bytes, suffix="B"):
    """Scale bytes to its proper format."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def sys_cpu():
    print(f"\n{Colors.CYAN}--- CPU Information ---{Colors.RESET}")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores: {psutil.cpu_count(logical=True)}")
    cpufreq = psutil.cpu_freq()
    if cpufreq:
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    print(f"CPU Usage: {psutil.cpu_percent()}%")

def sys_ram():
    print(f"\n{Colors.CYAN}--- RAM Information ---{Colors.RESET}")
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")

def sys_gpu():
    print(f"\n{Colors.CYAN}--- GPU Information ---{Colors.RESET}")
    try:
        output = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "name"], text=True)
        gpus = [line.strip() for line in output.split('\n') if line.strip() and "Name" not in line]
        for gpu in gpus:
            print(f"GPU: {gpu}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch GPU info: {e}")

def sys_disk():
    print(f"\n{Colors.CYAN}--- Disk Information ---{Colors.RESET}")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Device: {partition.device}")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total Size: {get_size(partition_usage.total)}")
            print(f"  Used: {get_size(partition_usage.used)}")
            print(f"  Free: {get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        except PermissionError:
            print("  [ERROR] Access Denied")
        print()

def sys_battery():
    print(f"\n{Colors.CYAN}--- Battery Information ---{Colors.RESET}")
    if not hasattr(psutil, "sensors_battery"):
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Battery information not available.")
        return
    battery = psutil.sensors_battery()
    if battery is None:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No battery detected (or desktop system).")
    else:
        print(f"Charge Level: {battery.percent}%")
        print(f"Plugged In:   {'Yes' if battery.power_plugged else 'No'}")
        if not battery.power_plugged:
            import datetime
            if battery.secsleft == -1:
                print("Time Left:    Unlimited (Plugged In)")
            elif battery.secsleft == -2:
                print("Time Left:    Calculating...")
            else:
                time_left = str(datetime.timedelta(seconds=battery.secsleft))
                print(f"Time Left:    {time_left}")
        else:
            print("Time Left:    Unlimited (Plugged In)")
            
        # Natively parse and show Battery Health and Cycles
        import tempfile
        temp_xml = os.path.join(tempfile.gettempdir(), "bat_temp.xml")
        try:
            import xml.etree.ElementTree as ET
            # Run powercfg XML output silently, writing to system Temp folder
            res = subprocess.run(["powercfg", "/batteryreport", "/xml", "/output", temp_xml], capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(temp_xml):
                tree = ET.parse(temp_xml)
                root = tree.getroot()
                battery_node = root.find(".//Battery")
                if battery_node is not None:
                    design_cap = battery_node.find("DesignCapacity")
                    full_cap = battery_node.find("FullChargeCapacity")
                    cycles = battery_node.find("CycleCount")
                    
                    if design_cap is not None and full_cap is not None:
                        d = int(design_cap.text)
                        f = int(full_cap.text)
                        if d > 0:
                            health = min(100.0, round((f / d) * 100, 2))
                            print(f"Battery Health: {health}% (Full Capacity vs. Design)")
                    if cycles is not None and cycles.text != "0":
                        print(f"Cycle Count:    {cycles.text} cycles")
                else:
                    print(f"{Colors.BLUE}[INFO]{Colors.RESET} No battery details found in system report.")
                os.remove(temp_xml)
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not retrieve battery health: {res.stderr.strip()}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not retrieve battery health: {e}")
            if os.path.exists(temp_xml):
                try:
                    os.remove(temp_xml)
                except:
                    pass

        print(f"\n{Colors.GREEN}[1]{Colors.RESET} Generate Full HTML Battery Report")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Skip")
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '1':
            print("\n[INFO] Generating battery report...")
            report_path = os.path.join(os.getcwd(), "battery-report.html")
            try:
                subprocess.run(["powercfg", "/batteryreport", "/output", report_path], check=True, capture_output=True)
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Battery report generated at: {report_path}")
                print("Opening report in your browser...")
                os.startfile(report_path)
            except Exception as e:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to generate report: {e}")

def sys_motherboard():
    print(f"\n{Colors.CYAN}--- Motherboard Information ---{Colors.RESET}")
    try:
        output = subprocess.check_output(["wmic", "baseboard", "get", "product,Manufacturer,version,serialnumber"], text=True)
        print(output.strip())
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch Motherboard info: {e}")

def sys_bios():
    print(f"\n{Colors.CYAN}--- BIOS Information ---{Colors.RESET}")
    try:
        output = subprocess.check_output(["wmic", "bios", "get", "name,version,smbiosbiosversion"], text=True)
        print(output.strip())
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not fetch BIOS info: {e}")

def sys_windows_version():
    print(f"\n{Colors.CYAN}--- Windows Version ---{Colors.RESET}")
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

def sys_processes():
    print(f"\n{Colors.CYAN}--- Top 10 Memory Consuming Processes ---{Colors.RESET}")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort by memory usage
    processes = sorted(processes, key=lambda p: p['memory_info'].rss, reverse=True)
    print(f"{'PID':<8} | {'Name':<25} | Memory Usage")
    print("-" * 55)
    for p in processes[:10]:
        print(f"{p['pid']:<8} | {str(p['name'])[:25]:<25} | {get_size(p['memory_info'].rss)}")

def sys_health_wmi():
    print(f"\n{Colors.CYAN}--- System & Storage Health Check (WMI) ---{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Storage SMART Drive Status:{Colors.RESET}")
    try:
        output = subprocess.check_output(["wmic", "diskdrive", "get", "model,status"], text=True, errors="ignore")
        print(output.strip())
    except Exception as e:
        print(f"  Failed to retrieve disk health: {e}")
        
    print(f"\n{Colors.BOLD}Windows System Integrity Status:{Colors.RESET}")
    try:
        output = subprocess.check_output(["wmic", "os", "get", "status,numberofprocesses,FreePhysicalMemory"], text=True, errors="ignore")
        lines = [l.strip() for l in output.strip().split("\n") if l.strip()]
        if len(lines) > 1:
            headers = lines[0].split()
            # Split values safely handling whitespace
            values = re.split(r'\s{2,}', lines[1])
            # If length mismatch, just print the raw lines
            if len(headers) == len(values):
                for h, v in zip(headers, values):
                    if h == "FreePhysicalMemory":
                        mb = int(v) // 1024
                        print(f"  Free Physical Memory: {mb} MB")
                    else:
                        print(f"  {h}: {v}")
            else:
                print(f"  OS Health Status: {lines[1]}")
        else:
            print("  Unable to parse OS status.")
    except Exception as e:
        print(f"  Failed to retrieve OS health: {e}")

def list_running_services():
    print(f"\n{Colors.CYAN}--- Active Windows Services ---{Colors.RESET}")
    print(f"{'Service Name':<30} | {'Display Name':<40} | Status")
    print("-" * 85)
    
    try:
        services = list(psutil.win_service_iter())
        running_services = [s for s in services if s.status() == "running"]
        running_services.sort(key=lambda s: s.name())
        
        for s in running_services[:30]:
            print(f"{s.name()[:30]:<30} | {s.display_name()[:40]:<40} | {s.status()}")
        print(f"\n[INFO] Displayed {min(len(running_services), 30)} out of {len(running_services)} running services.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to fetch services: {e}")

import re

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [14] SYSTEM INFORMATION{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} CPU")
        print(f"{Colors.GREEN}[2]{Colors.RESET} RAM")
        print(f"{Colors.GREEN}[3]{Colors.RESET} GPU")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Disk")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Battery")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Motherboard")
        print(f"{Colors.GREEN}[7]{Colors.RESET} BIOS")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Windows Version")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Installed Programs")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Startup Time")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Processes")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Running Services")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Disk Usage")
        print(f"{Colors.GREEN}[14]{Colors.RESET} Temperature")
        print(f"{Colors.GREEN}[15]{Colors.RESET} Health (WMI)")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            sys_cpu()
        elif choice == '2':
            sys_ram()
        elif choice == '3':
            sys_gpu()
        elif choice == '4':
            sys_disk()
        elif choice == '5':
            sys_battery()
        elif choice == '6':
            sys_motherboard()
        elif choice == '7':
            sys_bios()
        elif choice == '8':
            sys_windows_version()
        elif choice == '9':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Installed Programs coming soon...")
        elif choice == '10':
            import datetime
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
            print(f"\nSystem Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        elif choice == '11':
            sys_processes()
        elif choice == '12':
            list_running_services()
        elif choice == '13':
            sys_disk()
        elif choice == '14':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Hardware Temperature coming soon...")
        elif choice == '15':
            sys_health_wmi()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
