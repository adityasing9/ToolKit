from toolkit.utils import Colors
import os
import sys
import subprocess

def run_admin_cmd(cmd_list):
    """Run an administrative console command safely, warning if user lacks rights."""
    try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run(cmd_list)
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges are required to perform this action.")
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Target command: {' '.join(cmd_list)}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to execute command: {e}")

def export_drivers():
    print(f"\n{Colors.CYAN}--- Export Drivers (DISM) ---{Colors.RESET}")
    print("This will export all active third-party drivers to a local directory.")
    dest = input("Enter backup directory (default: C:\\Drivers_Export): ").strip().strip('"').strip("'")
    if not dest:
        dest = r"C:\Drivers_Export"
        
    if not os.path.exists(dest):
        try:
            os.makedirs(dest)
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to create directory: {e}")
            return
            
    print(f"[INFO] Exporting drivers to {dest} via DISM...")
    run_admin_cmd(["dism", "/Online", "/Export-Driver", f"/Destination:{dest}"])

def backup_drivers():
    print(f"\n{Colors.CYAN}--- Backup Drivers (PnpUtil) ---{Colors.RESET}")
    print("This will create a structured backup of all system drivers.")
    dest = input("Enter backup directory (default: C:\\Drivers_Backup): ").strip().strip('"').strip("'")
    if not dest:
        dest = r"C:\Drivers_Backup"
        
    if not os.path.exists(dest):
        try:
            os.makedirs(dest)
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to create directory: {e}")
            return
            
    print(f"[INFO] Backing up active drivers to {dest} via PnpUtil...")
    run_admin_cmd(["pnputil", "/export-driver", "*", dest])

def restore_drivers():
    print(f"\n{Colors.CYAN}--- Restore Drivers (PnpUtil) ---{Colors.RESET}")
    print("This will recursively install all .inf drivers from a backup folder.")
    src = input("Enter driver backup folder path: ").strip().strip('"').strip("'")
    if not src or not os.path.exists(src):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid source directory.")
        return
        
    confirm = input("This will install all matched drivers. Proceed? (y/n): ").strip().lower()
    if confirm == 'y':
        print(f"[INFO] Installing drivers recursively from {src}...")
        # Add and install drivers recursively
        run_admin_cmd(["pnputil", "/add-driver", os.path.join(src, "*.inf"), "/subdirs", "/install"])

def check_missing_drivers():
    print(f"\n{Colors.CYAN}--- Scan for Missing / Error Devices ---{Colors.RESET}")
    print("[INFO] Querying WMI for devices reporting errors or missing drivers...")
    
    ps_cmd = "Get-CimInstance Win32_PnPEntity | Where-Object ConfigManagerErrorCode -ne 0 | Select-Object DeviceID, Name, ConfigManagerErrorCode, Status | Format-Table -AutoSize"
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0 and res.stdout.strip():
            print(f"\n{Colors.RED}[WARNING]{Colors.RESET} Found devices with hardware issues or missing drivers:")
            print(res.stdout)
        else:
            print(f"\n{Colors.GREEN}[CLEAN]{Colors.RESET} No hardware devices reporting missing drivers or configuration errors.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Query failed: {e}")

def list_installed_oem_drivers():
    print(f"\n{Colors.CYAN}--- Installed OEM Drivers (PnpUtil List) ---{Colors.RESET}")
    print("[INFO] Querying active third-party system drivers...")
    
    try:
        # Fetch list of third-party oem drivers
        res = subprocess.run(["pnputil", "/enum-drivers"], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0:
            lines = res.stdout.split("\n")
            oem_drivers = []
            current = {}
            for line in lines:
                line = line.strip()
                if not line:
                    if current:
                        oem_drivers.append(current)
                        current = {}
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    current[key.strip()] = val.strip()
                    
            if current:
                oem_drivers.append(current)
                
            if oem_drivers:
                print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Active Third-Party (OEM) Drivers ({len(oem_drivers)}) ==={Colors.RESET}")
                header = f"{'Published Name':<16} | {'Original Name':<20} | {'Provider':<15} | {'Class':<15} | {'Version':<18}"
                border = "-" * len(header)
                print(header)
                print(border)
                for d in oem_drivers[:40]: # Show top 40
                    pub = d.get("Published Name", "N/A")
                    orig = d.get("Original Name", "N/A")
                    prov = d.get("Provider Name", "N/A")
                    cls = d.get("Class Name", "N/A")
                    ver = d.get("Driver Version", "N/A")
                    print(f"{pub:<16} | {orig[:20]:<20} | {prov[:15]:<15} | {cls[:15]:<15} | {ver:<18}")
                print(border)
                if len(oem_drivers) > 40:
                    print(f"  ... and {len(oem_drivers) - 40} more drivers.")
            else:
                print("No third-party OEM drivers could be parsed.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} pnputil enum-drivers failed: {res.stderr}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Query failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [22] SYSTEM DRIVER MANAGER{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Export Active Drivers (DISM)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Backup System Drivers (PnpUtil)")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Restore System Drivers (PnpUtil)")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Scan for Missing or Unconfigured Drivers")
        print(f"{Colors.GREEN}[5]{Colors.RESET} List Installed Third-Party (OEM) Drivers")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            export_drivers()
            input("\nPress Enter to continue...")
        elif choice == '2':
            backup_drivers()
            input("\nPress Enter to continue...")
        elif choice == '3':
            restore_drivers()
            input("\nPress Enter to continue...")
        elif choice == '4':
            check_missing_drivers()
            input("\nPress Enter to continue...")
        elif choice == '5':
            list_installed_oem_drivers()
            input("\nPress Enter to continue...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
