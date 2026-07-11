from toolkit.utils import Colors
import os
import sys
import time
import psutil
import winreg

def list_running_processes(sort_by='memory', limit=40):
    print(f"\n[INFO] Gathering running processes (Sorted by {sort_by})...")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
            info = proc.info
            cpu = info['cpu_percent'] if info['cpu_percent'] is not None else 0.0
            mem = info['memory_info'].rss / (1024 * 1024) if info['memory_info'] is not None else 0.0
            processes.append({
                'pid': info['pid'],
                'name': info['name'] or 'N/A',
                'username': info['username'] or 'N/A',
                'cpu': cpu,
                'memory': mem,
                'status': info['status'] or 'N/A'
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Sort processes
    if sort_by == 'cpu':
        processes.sort(key=lambda x: x['cpu'], reverse=True)
    else:
        processes.sort(key=lambda x: x['memory'], reverse=True)

    # Display Table
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Active System Processes (Top {limit}) ==={Colors.RESET}")
    header = f"{'PID':<8} | {'Process Name':<30} | {'CPU %':<8} | {'RAM (MB)':<10} | {'Status':<12} | {'User':<20}"
    border = "-" * len(header)
    print(header)
    print(border)

    for p in processes[:limit]:
        user_clean = p['username'].split('\\')[-1] if '\\' in p['username'] else p['username']
        row = f"{p['pid']:<8} | {p['name'][:30]:<30} | {p['cpu']:<8.1f} | {p['memory']:<10.1f} | {p['status']:<12} | {user_clean:<20}"
        print(row)
    print(border)

def kill_process():
    print(f"\n{Colors.CYAN}--- Kill Process ---{Colors.RESET}")
    target = input("Enter Process PID or Name to terminate: ").strip()
    if not target:
        return
        
    force = input("Force terminate process? (y/n, default n): ").strip().lower() == 'y'
    
    killed = False
    if target.isdigit():
        pid = int(target)
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            if force:
                proc.kill()
            else:
                proc.terminate()
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Process {name} (PID: {pid}) terminated.")
            killed = True
        except psutil.NoSuchProcess:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} No process found with PID: {pid}")
        except psutil.AccessDenied:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Access denied. Run as Administrator.")
    else:
        # Kill by name
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == target.lower():
                    if force:
                        proc.kill()
                    else:
                        proc.terminate()
                    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Process {proc.info['name']} (PID: {proc.info['pid']}) terminated.")
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        if not killed:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} No active process matched name: '{target}'")

def restart_process():
    print(f"\n{Colors.CYAN}--- Restart Process ---{Colors.RESET}")
    pid_in = input("Enter Process PID to restart: ").strip()
    if not pid_in or not pid_in.isdigit():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid PID.")
        return
        
    pid = int(pid_in)
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        cmdline = proc.cmdline()
        cwd = proc.cwd()
        
        if not cmdline:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not retrieve startup command arguments for this process.")
            return
            
        print(f"[INFO] Stopping process {name} (PID: {pid})...")
        proc.terminate()
        proc.wait(timeout=3)
        
        print(f"[INFO] Launching new instance of {name}...")
        import subprocess
        subprocess.Popen(cmdline, cwd=cwd, shell=True)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Process {name} restarted successfully.")
    except psutil.TimeoutExpired:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Process failed to stop in time.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Restart failed: {e}")

def draw_process_tree():
    print(f"\n{Colors.CYAN}--- Process Tree ---{Colors.RESET}")
    pid_in = input("Enter Root PID to map (leave blank for current terminal root): ").strip()
    
    root_pid = None
    if pid_in.isdigit():
        root_pid = int(pid_in)
    else:
        root_pid = os.getppid()  # Parent of current Python script
        
    try:
        root_proc = psutil.Process(root_pid)
    except psutil.NoSuchProcess:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Root PID {root_pid} not found.")
        return
        
    print(f"\nMapping parent tree starting from PID {root_pid} ({root_proc.name()})...")
    
    # Map parent PIDs to children list
    tree = {}
    for proc in psutil.process_iter(['pid', 'ppid', 'name']):
        try:
            pid = proc.info['pid']
            ppid = proc.info['ppid']
            name = proc.info['name']
            if ppid not in tree:
                tree[ppid] = []
            tree[ppid].append((pid, name))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    def print_node(pid, name, indent=""):
        print(f"{indent}├── [{pid}] {name}")
        if pid in tree:
            for child_pid, child_name in tree[pid]:
                print_node(child_pid, child_name, indent + "    ")
                
    print_node(root_proc.pid, root_proc.name())

def view_startup_processes():
    print(f"\n{Colors.CYAN}--- Startup Applications Registry ---{Colors.RESET}")
    print("Reading registry locations where startup applications are registered:")
    
    reg_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "User Run Registry"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "System Run Registry")
    ]
    
    found = False
    for hive, path, desc in reg_paths:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}[{desc}]{Colors.RESET}")
        try:
            key = winreg.OpenKey(hive, path, 0, winreg.KEY_READ)
            num_values = winreg.QueryInfoKey(key)[1]
            if num_values == 0:
                print("  No apps registered in this key.")
            for i in range(num_values):
                name, val, _ = winreg.EnumValue(key, i)
                print(f"  - {Colors.GREEN}{name:<25}{Colors.RESET} : {val}")
                found = True
            winreg.CloseKey(key)
        except WindowsError as e:
            print(f"  {Colors.RED}[ERROR]{Colors.RESET} Could not access registry path: {e}")
            
    if not found:
        print("\nNo registered startup processes found.")

def detect_high_utilization(metric='cpu', threshold=5.0):
    print(f"\n[INFO] Filtering processes utilizing high {metric.upper()}...")
    processes = []
    
    # Force evaluation of CPU percents
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # First query sets baseline
            proc.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    time.sleep(0.5) # Wait for delta
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username']):
        try:
            info = proc.info
            cpu = proc.cpu_percent()
            mem = info['memory_info'].rss / (1024 * 1024) if info['memory_info'] else 0.0
            
            if metric == 'cpu' and cpu >= threshold:
                processes.append((info['pid'], info['name'], cpu, mem, info['username'] or 'N/A'))
            elif metric == 'ram' and mem >= threshold:
                processes.append((info['pid'], info['name'], cpu, mem, info['username'] or 'N/A'))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    if not processes:
        print(f"\n{Colors.GREEN}[CLEAN]{Colors.RESET} No processes found exceeding {threshold} {('percent' if metric == 'cpu' else 'MB')}.")
        return
        
    print(f"\n{Colors.BOLD}{Colors.RED}=== High {metric.upper()} Processes (Threshold: {threshold}) ==={Colors.RESET}")
    print(f"{'PID':<8} | {'Process Name':<30} | {'CPU %':<8} | {'RAM (MB)':<10} | {'User':<20}")
    print("-" * 80)
    for pid, name, cpu, mem, user in processes:
        user_clean = user.split('\\')[-1] if '\\' in user else user
        print(f"{pid:<8} | {name[:30]:<30} | {cpu:<8.1f} | {mem:<10.1f} | {user_clean:<20}")

def live_task_monitor():
    print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Starting Live Monitor. Press Ctrl+C to stop.")
    time.sleep(1.5)
    
    try:
        while True:
            # Clear console
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Fetch load statistics
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}                    ⚡ LIVE PROCESS MONITOR{Colors.RESET}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"  CPU Total: [{Colors.GREEN}{cpu_usage:<4}%{Colors.RESET}]   |   RAM Total: [{Colors.GREEN}{ram_usage:<4}%{Colors.RESET}]")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            
            # Print top 15 processes by memory
            list_running_processes(sort_by='memory', limit=15)
            
            print(f"\n{Colors.BLUE}Press Ctrl+C to terminate monitor and return to menu.{Colors.RESET}")
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n[INFO] Live Monitor stopped.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [20] SYSTEM PROCESS MANAGER{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} View Active Running Processes (RAM Sorted)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} View Active Running Processes (CPU Sorted)")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Terminate (Kill) Process")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Restart Active Process")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Draw Parent-Child Process Tree")
        print(f"{Colors.GREEN}[6]{Colors.RESET} View Registry Startup Processes")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Scan for High CPU Utilization (> 5%)")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Scan for High RAM Utilization (> 150 MB)")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Launch Live Refreshing Task Monitor")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            list_running_processes(sort_by='memory')
            input("\nPress Enter to continue...")
        elif choice == '2':
            list_running_processes(sort_by='cpu')
            input("\nPress Enter to continue...")
        elif choice == '3':
            kill_process()
            input("\nPress Enter to continue...")
        elif choice == '4':
            restart_process()
            input("\nPress Enter to continue...")
        elif choice == '5':
            draw_process_tree()
            input("\nPress Enter to continue...")
        elif choice == '6':
            view_startup_processes()
            input("\nPress Enter to continue...")
        elif choice == '7':
            detect_high_utilization(metric='cpu', threshold=5.0)
            input("\nPress Enter to continue...")
        elif choice == '8':
            detect_high_utilization(metric='ram', threshold=150.0)
            input("\nPress Enter to continue...")
        elif choice == '9':
            live_task_monitor()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
