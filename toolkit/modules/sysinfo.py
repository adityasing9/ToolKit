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
    print("\n--- CPU Information ---")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores: {psutil.cpu_count(logical=True)}")
    cpufreq = psutil.cpu_freq()
    if cpufreq:
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    print(f"CPU Usage: {psutil.cpu_percent()}%")

def sys_ram():
    print("\n--- RAM Information ---")
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")

def sys_gpu():
    print("\n--- GPU Information ---")
    try:
        output = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "name"], text=True)
        gpus = [line.strip() for line in output.split('\n') if line.strip() and "Name" not in line]
        for gpu in gpus:
            print(f"GPU: {gpu}")
    except Exception as e:
        print(f"[ERROR] Could not fetch GPU info: {e}")

def sys_disk():
    print("\n--- Disk Information ---")
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
    print("\n--- Battery Information ---")
    if not hasattr(psutil, "sensors_battery"):
        print("[INFO] Battery information not available.")
        return
    battery = psutil.sensors_battery()
    if battery is None:
        print("[INFO] No battery detected.")
    else:
        print(f"Charge: {battery.percent}%")
        print(f"Plugged In: {'Yes' if battery.power_plugged else 'No'}")
        if not battery.power_plugged:
            # seconds to hours and minutes
            import datetime
            time_left = str(datetime.timedelta(seconds=battery.secsleft))
            print(f"Time Left: {time_left}")

def sys_motherboard():
    print("\n--- Motherboard Information ---")
    try:
        output = subprocess.check_output(["wmic", "baseboard", "get", "product,Manufacturer,version,serialnumber"], text=True)
        print(output.strip())
    except Exception as e:
        print(f"[ERROR] Could not fetch Motherboard info: {e}")

def sys_bios():
    print("\n--- BIOS Information ---")
    try:
        output = subprocess.check_output(["wmic", "bios", "get", "name,version,smbiosbiosversion"], text=True)
        print(output.strip())
    except Exception as e:
        print(f"[ERROR] Could not fetch BIOS info: {e}")

def sys_windows_version():
    print("\n--- Windows Version ---")
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

def sys_processes():
    print("\n--- Top 10 Memory Consuming Processes ---")
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
        print("\n=============================================================")
        print("              [11] SYSTEM INFORMATION")
        print("=============================================================")
        print("[1] CPU")
        print("[2] RAM")
        print("[3] GPU")
        print("[4] Disk")
        print("[5] Battery")
        print("[6] Motherboard")
        print("[7] BIOS")
        print("[8] Windows Version")
        print("[9] Installed Programs")
        print("[10] Startup Time")
        print("[11] Processes")
        print("[12] Running Services")
        print("[13] Disk Usage")
        print("[14] Temperature")
        print("[15] Health")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[INFO] Installed Programs coming soon...")
        elif choice == '10':
            import datetime
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
            print(f"\nSystem Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        elif choice == '11':
            sys_processes()
        elif choice == '12':
            print("[INFO] Running Services coming soon...")
        elif choice == '13':
            sys_disk()
        elif choice == '14':
            print("[INFO] Hardware Temperature coming soon...")
        elif choice == '15':
            print("[INFO] System Health Check coming soon...")
        else:
            print("[ERROR] Invalid choice.")
