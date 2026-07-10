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
        print(f"[INFO] Directory {path} does not exist.")
        return
    
    print(f"\n[INFO] Calculating size of {path}...")
    size_before = get_size(path)
    print(f"[INFO] Current Size: {format_size(size_before)}")
    
    confirm = input(f"Are you sure you want to delete contents of {path}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[INFO] Cleanup cancelled.")
        return

    print("[INFO] Cleaning up...")
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

    print(f"[SUCCESS] Cleaned {format_size(deleted_size)} from {path}")

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
        print("[SUCCESS] Recycle Bin emptied.")
    except Exception as e:
        print(f"[ERROR] Failed to empty Recycle Bin: {e}")

def flush_dns():
    print("\n[INFO] Flushing DNS Cache...")
    try:
        subprocess.run(["ipconfig", "/flushdns"])
    except Exception as e:
        print(f"[ERROR] Failed to flush DNS: {e}")

def run_disk_cleanup():
    print("\n[INFO] Launching Windows Disk Cleanup Utility...")
    try:
        subprocess.Popen(["cleanmgr", "/sageset:1"])
        print("[INFO] Please configure the cleanup options in the window that opens.")
    except Exception as e:
        print(f"[ERROR] Failed to launch Disk Cleanup: {e}")

def optimize_drives():
    print("\n[INFO] Launching Drive Optimizer (Defragmenter)...")
    try:
        subprocess.Popen(["dfrgui"])
    except Exception as e:
        print(f"[ERROR] Failed to launch Drive Optimizer: {e}")

def winget_upgrade():
    print("\n[INFO] Checking for package upgrades via Winget...")
    confirm = input("This may take a while. Continue? (y/n): ").strip().lower()
    if confirm == 'y':
        subprocess.run(["winget", "upgrade", "--all"])
    else:
        print("[INFO] Cancelled.")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [12] CLEANUP & MAINTENANCE")
        print("=============================================================")
        print("[1] Temp")
        print("[2] Prefetch")
        print("[3] Windows Temp")
        print("[4] Recycle Bin")
        print("[5] DNS Cache")
        print("[6] Thumbnail Cache")
        print("[7] Recent Files")
        print("[8] PowerShell History")
        print("[9] Browser Cache")
        print("[10] Windows Logs")
        print("[11] Disk Cleanup")
        print("[12] Optimize Drives")
        print("[13] Winget Upgrade")
        print("[14] Winget Repair")
        print("[15] App Repair")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[INFO] Thumbnail Cache cleanup coming soon...")
        elif choice == '7':
            clear_directory("%APPDATA%\\Microsoft\\Windows\\Recent")
        elif choice == '8':
            clear_directory("%APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadLine")
        elif choice == '9':
            print("[INFO] Browser Cache cleanup coming soon...")
        elif choice == '10':
            print("[INFO] Windows Logs cleanup coming soon...")
        elif choice == '11':
            run_disk_cleanup()
        elif choice == '12':
            optimize_drives()
        elif choice == '13':
            winget_upgrade()
        elif choice == '14':
            print("[INFO] Winget Repair coming soon...")
        elif choice == '15':
            print("[INFO] App Repair coming soon...")
        else:
            print("[ERROR] Invalid choice.")
