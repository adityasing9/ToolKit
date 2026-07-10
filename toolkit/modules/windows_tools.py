import os
import subprocess

def run_admin_cmd(cmd_list):
    """Attempt to run a command that requires admin rights."""
    try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run(cmd_list)
        else:
            print("[ERROR] Administrator privileges required for this action.")
            print(f"[INFO] Command: {' '.join(cmd_list)}")
    except Exception as e:
        print(f"[ERROR] Could not execute command: {e}")

def check_activation():
    print("\n[INFO] Checking Windows Activation Status...")
    subprocess.run(["slmgr", "/xpr"])

def open_driver_manager():
    print("\n[INFO] Opening Device Manager...")
    subprocess.Popen(["devmgmt.msc"])

def check_windows_update():
    print("\n[INFO] Opening Windows Update...")
    subprocess.Popen(["control", "update"])

def open_services():
    print("\n[INFO] Opening Services Manager...")
    subprocess.Popen(["services.msc"])

def open_startup_apps():
    print("\n[INFO] Opening Startup Apps Manager...")
    subprocess.Popen(["taskmgr", "/0", "/startup"])

def open_installed_apps():
    print("\n[INFO] Opening Add/Remove Programs...")
    subprocess.Popen(["appwiz.cpl"])

def repair_windows():
    print("\n--- Repair Windows ---")
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
    print("\n--- Disk Check (chkdsk) ---")
    drive = input("Enter drive letter (e.g. C): ").strip().upper()
    if drive:
        if not drive.endswith(":"):
            drive += ":"
        run_admin_cmd(["chkdsk", drive, "/f"])

def create_restore_point():
    print("\n--- Create System Restore Point ---")
    desc = input("Enter description for restore point: ").strip()
    if not desc:
        desc = "Toolkit_Manual_Restore"
    print("[INFO] Creating restore point...")
    ps_cmd = f'Checkpoint-Computer -Description "{desc}" -RestorePointType "MODIFY_SETTINGS"'
    try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd])
            print("[SUCCESS] Restore point created.")
        else:
            print("[ERROR] Administrator privileges required.")
    except Exception as e:
        print(f"[ERROR] Failed to create restore point: {e}")

def open_env_vars():
    print("\n[INFO] Opening Environment Variables...")
    subprocess.Popen(["rundll32", "sysdm.cpl,EditEnvironmentVariables"])

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [2] WINDOWS TOOLKIT")
        print("=============================================================")
        print("[1] Activation Status")
        print("[2] Drivers Manager")
        print("[3] Windows Update")
        print("[4] Services")
        print("[5] Startup Apps")
        print("[6] Installed Apps")
        print("[7] Repair Windows (DISM + SFC)")
        print("[8] DISM Scan")
        print("[9] SFC Scan")
        print("[10] Disk Check (chkdsk)")
        print("[11] Create Restore Point")
        print("[12] Environment Variables")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[ERROR] Invalid choice.")
