from toolkit.utils import Colors
import os
import shutil
import subprocess
import glob

def get_size(path):
    total_size = 0
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
    elif os.path.isdir(path):
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def format_size(bytes):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"
        bytes /= factor
    return "0B"

def clear_directory(path_str):
    """Safely attempts to clear the contents of a directory."""
    path = os.path.expandvars(path_str)
    if not os.path.exists(path):
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Directory {path} does not exist.")
        return
    
    print(f"\n[INFO] Calculating size of {path}...")
    size_before = get_size(path)
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Current Size: {format_size(size_before)}")
    
    confirm = input(f"Are you sure you want to delete contents of {path}? (y/n): ").strip().lower()
    if confirm != 'y':
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cleanup cancelled.")
        return

    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cleaning up...")
    deleted_size = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                size = os.path.getsize(filepath)
                os.remove(filepath)
                deleted_size += size
            except Exception:
                pass
        for name in dirs:
            dirpath = os.path.join(root, name)
            try:
                os.rmdir(dirpath)
            except Exception:
                pass

    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Cleaned {format_size(deleted_size)} from {path}")

def clean_temp():
    clear_directory("%TEMP%")

def clean_prefetch():
    clear_directory("C:\\Windows\\Prefetch")

def clean_windows_temp():
    clear_directory("C:\\Windows\\Temp")

def empty_recycle_bin():
    print("\n[INFO] Emptying Recycle Bin...")
    try:
        # Uses powershell to empty recycle bin without confirmation prompt natively
        subprocess.run(["powershell", "-NoProfile", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"])
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Recycle Bin emptied.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to empty Recycle Bin: {e}")

def flush_dns():
    print("\n[INFO] Flushing DNS Cache...")
    try:
        subprocess.run(["ipconfig", "/flushdns"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to flush DNS: {e}")

def run_disk_cleanup():
    print("\n[INFO] Launching Windows Disk Cleanup Utility...")
    try:
        subprocess.Popen(["cleanmgr", "/sageset:1"])
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please configure the cleanup options in the window that opens.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to launch Disk Cleanup: {e}")

def optimize_drives():
    print("\n[INFO] Launching Drive Optimizer (Defragmenter)...")
    try:
        subprocess.Popen(["dfrgui"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to launch Drive Optimizer: {e}")

def winget_upgrade():
    print("\n[INFO] Checking for package upgrades via Winget...")
    confirm = input("This may take a while. Continue? (y/n): ").strip().lower()
    if confirm == 'y':
        subprocess.run(["winget", "upgrade", "--all"])
    else:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cancelled.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [2] CLEANUP & MAINTENANCE{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Temp")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Prefetch")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Windows Temp")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Recycle Bin")
        print(f"{Colors.GREEN}[5]{Colors.RESET} DNS Cache")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Thumbnail Cache")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Recent Files")
        print(f"{Colors.GREEN}[8]{Colors.RESET} PowerShell History")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Browser Cache")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Windows Logs")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Disk Cleanup")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Optimize Drives")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Winget Upgrade")
        print(f"{Colors.GREEN}[14]{Colors.RESET} Winget Repair")
        print(f"{Colors.GREEN}[15]{Colors.RESET} App Repair")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            clean_temp()
        elif choice == '2':
            clean_prefetch()
        elif choice == '3':
            clean_windows_temp()
        elif choice == '4':
            empty_recycle_bin()
        elif choice == '5':
            flush_dns()
        elif choice == '6':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Thumbnail Cache cleanup coming soon...")
        elif choice == '7':
            clear_directory("%APPDATA%\\Microsoft\\Windows\\Recent")
        elif choice == '8':
            clear_directory("%APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadLine")
        elif choice == '9':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Browser Cache cleanup coming soon...")
        elif choice == '10':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Windows Logs cleanup coming soon...")
        elif choice == '11':
            run_disk_cleanup()
        elif choice == '12':
            optimize_drives()
        elif choice == '13':
            winget_upgrade()
        elif choice == '14':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Winget Repair coming soon...")
        elif choice == '15':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} App Repair coming soon...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
