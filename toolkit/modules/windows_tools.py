from toolkit.utils import Colors
import os
import subprocess

def run_admin_cmd(cmd_list):
    """Attempt to run a command that requires admin rights."""
    try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run(cmd_list)
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges required for this action.")
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Command: {' '.join(cmd_list)}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not execute command: {e}")

def check_activation():
    print("\n[INFO] Checking Windows Activation Status...")
    subprocess.run(["cscript", "//NoLogo", r"C:\Windows\System32\slmgr.vbs", "/xpr"])

def open_driver_manager():
    print("\n[INFO] Opening Device Manager...")
    try:
        subprocess.Popen(["mmc.exe", "devmgmt.msc"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to open Device Manager: {e}")

def check_windows_update():
    print("\n[INFO] Opening Windows Update...")
    try:
        subprocess.Popen(["control", "update"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to open Windows Update: {e}")

def open_services():
    print("\n[INFO] Opening Services Manager...")
    try:
        subprocess.Popen(["mmc.exe", "services.msc"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to open Services Manager: {e}")

def open_startup_apps():
    print("\n[INFO] Opening Startup Apps Manager...")
    try:
        subprocess.Popen(["taskmgr", "/0", "/startup"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to open Startup Apps: {e}")

def open_installed_apps():
    print("\n[INFO] Opening Add/Remove Programs...")
    try:
        subprocess.Popen(["control", "appwiz.cpl"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to open Add/Remove Programs: {e}")

def repair_windows():
    print(f"\n{Colors.CYAN}--- Repair Windows ---{Colors.RESET}")
    print("This will run DISM RestoreHealth and SFC ScanNow.")
    confirm = input("This process takes time and requires Admin. Continue? (y/n): ").strip().lower()
    if confirm == 'y':
        print("\n[1/2] Running DISM...")
        run_admin_cmd(["dism", "/Online", "/Cleanup-Image", "/RestoreHealth"])
        print("\n[2/2] Running SFC...")
        run_admin_cmd(["sfc", "/scannow"])

def run_dism_scan():
    print("\n[INFO] Running DISM ScanHealth...")
    run_admin_cmd(["dism", "/Online", "/Cleanup-Image", "/ScanHealth"])

def run_sfc_scan():
    print("\n[INFO] Running SFC Scan...")
    run_admin_cmd(["sfc", "/scannow"])

def run_chkdsk():
    print(f"\n{Colors.CYAN}--- Disk Check (chkdsk) ---{Colors.RESET}")
    drive = input("Enter drive letter (e.g. C): ").strip().upper()
    if drive:
        if not drive.endswith(":"):
            drive += ":"
        run_admin_cmd(["chkdsk", drive, "/f"])

def create_restore_point():
    print(f"\n{Colors.CYAN}--- Create System Restore Point ---{Colors.RESET}")
    desc = input("Enter description for restore point: ").strip()
    if not desc:
        desc = "Toolkit_Manual_Restore"
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Creating restore point...")
    ps_cmd = f'Checkpoint-Computer -Description "{desc}" -RestorePointType "MODIFY_SETTINGS"'
    try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd])
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Restore point created.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges required.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to create restore point: {e}")

def open_env_vars():
    print("\n[INFO] Opening Environment Variables...")
    subprocess.Popen(["rundll32", "sysdm.cpl,EditEnvironmentVariables"])

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [2] WINDOWS TOOLKIT{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Activation Status")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Drivers Manager")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Windows Update")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Services")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Startup Apps")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Installed Apps")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Repair Windows (DISM + SFC)")
        print(f"{Colors.GREEN}[8]{Colors.RESET} DISM Scan")
        print(f"{Colors.GREEN}[9]{Colors.RESET} SFC Scan")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Disk Check (chkdsk)")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Create Restore Point")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Environment Variables")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            check_activation()
        elif choice == '2':
            open_driver_manager()
        elif choice == '3':
            check_windows_update()
        elif choice == '4':
            open_services()
        elif choice == '5':
            open_startup_apps()
        elif choice == '6':
            open_installed_apps()
        elif choice == '7':
            repair_windows()
        elif choice == '8':
            run_dism_scan()
        elif choice == '9':
            run_sfc_scan()
        elif choice == '10':
            run_chkdsk()
        elif choice == '11':
            create_restore_point()
        elif choice == '12':
            open_env_vars()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
