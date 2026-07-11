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
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No battery detected.")
    else:
        print(f"Charge: {battery.percent}%")
        print(f"Plugged In: {'Yes' if battery.power_plugged else 'No'}")
        if not battery.power_plugged:
            # seconds to hours and minutes
            import datetime
            time_left = str(datetime.timedelta(seconds=battery.secsleft))
            print(f"Time Left: {time_left}")

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
        print(f"{Colors.GREEN}[15]{Colors.RESET} Health")
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
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Running Services coming soon...")
        elif choice == '13':
            sys_disk()
        elif choice == '14':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Hardware Temperature coming soon...")
        elif choice == '15':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} System Health Check coming soon...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
