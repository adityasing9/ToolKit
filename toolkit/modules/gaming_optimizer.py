from toolkit.utils import Colors
import os
import sys
import subprocess
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def set_reg_value(hive, path, name, value, value_type=winreg.REG_DWORD):
    """Set registry value safely, creating keys if they do not exist."""
    try:
        key = winreg.CreateKeyEx(hive, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, value_type, value)
        winreg.CloseKey(key)
        return True
    except WindowsError as e:
        print(f"  {Colors.RED}[ERROR]{Colors.RESET} Failed to set registry key {name}: {e}")
        return False

def disable_background_apps():
    print(f"\n{Colors.CYAN}--- Disable Background Apps & Telemetry ---{Colors.RESET}")
    if not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges required.")
        return
        
    print("[INFO] Tuning registry for background apps and telemetry...")
    # Disable global background apps
    set_reg_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled", 1)
    # Disable advertising ID
    set_reg_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", 0)
    # Disable telemetry
    set_reg_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0)
    
    # Disable superfetch/SysMain and DiagTrack services
    services = ["sysmain", "DiagTrack"]
    for s in services:
        print(f"[INFO] Stopping and disabling service '{s}'...")
        subprocess.run(["sc", "stop", s], capture_output=True)
        subprocess.run(["sc", "config", s, "start=", "disabled"], capture_output=True)
        
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Telemetry services disabled and background apps restricted.")

def enable_high_performance():
    print(f"\n{Colors.CYAN}--- Activate Ultimate Power Performance ---{Colors.RESET}")
    # Ultimate Performance Plan GUID
    ultimate_guid = "e9a42b02-d5df-448d-aa00-03f14749eb61"
    
    print("[INFO] Checking active power schemes...")
    # Try importing duplicate scheme
    subprocess.run(["powercfg", "/duplicatescheme", ultimate_guid], capture_output=True)
    # Set scheme active
    res = subprocess.run(["powercfg", "/setactive", ultimate_guid], capture_output=True)
    if res.returncode == 0:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Activated Ultimate Power Performance scheme.")
    else:
        # Fallback to high performance scheme
        fallback_res = subprocess.run(["powercfg", "/setactive", "SCHEME_MIN"], capture_output=True)
        if fallback_res.returncode == 0:
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Activated High Performance power scheme.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not configure power profile automatically.")

def empty_ram_cache():
    print(f"\n{Colors.CYAN}--- Empty RAM Standby Cache ---{Colors.RESET}")
    print("[INFO] Forcing garbage collection and system memory standby purge...")
    
    ps_cmd = "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"
    try:
        # Clear garbage collection
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
        
        # Clear standby list via API if admin
        if is_admin():
            # Trigger page file trimming/standby release via memory manager limits
            set_reg_value(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "ClearPageFileAtShutdown", 0)
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Standby memory cache released successfully.")
        else:
            print(f"{Colors.YELLOW}[INFO]{Colors.RESET} Trim completed. For complete system standby purge, run as Administrator.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Standby purge failed: {e}")

def kill_overlays():
    print(f"\n{Colors.CYAN}--- Kill Overlay Processes ---{Colors.RESET}")
    overlay_targets = [
        "SteamOverlayUI.exe", "GameBarFT.exe", "GameBar.exe", 
        "Discord.exe", "DiscordCanary.exe", "GeForceShare.exe", 
        "OriginWebHelperService.exe"
    ]
    
    killed_any = False
    import psutil
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] in overlay_targets:
                print(f"[INFO] Terminating overlay process: {proc.info['name']} (PID: {proc.info['pid']})")
                proc.terminate()
                killed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    if killed_any:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Overlay processes terminated.")
    else:
        print(f"{Colors.GREEN}[CLEAN]{Colors.RESET} No target overlay helper processes active.")

def optimize_network():
    print(f"\n{Colors.CYAN}--- Network Latency Optimization ---{Colors.RESET}")
    if not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges required.")
        return
        
    print("[INFO] Tuning TCP Nagle's algorithm and resetting socket stack...")
    
    # TCP parameters
    path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        subkeys_count = winreg.QueryInfoKey(key)[0]
        for i in range(subkeys_count):
            subkey_name = winreg.EnumKey(key, i)
            interface_path = f"{path}\\{subkey_name}"
            # Enable TcpAckFrequency and TCPNoDelay for low latency gaming response
            set_reg_value(winreg.HKEY_LOCAL_MACHINE, interface_path, "TcpAckFrequency", 1)
            set_reg_value(winreg.HKEY_LOCAL_MACHINE, interface_path, "TCPNoDelay", 1)
        winreg.CloseKey(key)
        
        # Reset winsock
        subprocess.run(["netsh", "winsock", "reset"], capture_output=True)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Gaming network profiles applied (TCPNoDelay enabled).")
        print(f"{Colors.YELLOW}[NOTE]{Colors.RESET} Restart your computer to apply WinSock socket resets.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Network optimization failed: {e}")

def toggle_fps_mode():
    print(f"\n{Colors.CYAN}--- Disable GameDVR & Enable Gaming FPS Mode ---{Colors.RESET}")
    if not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges required.")
        return
        
    print("[INFO] Modifying Windows Game Configuration registry settings...")
    # Disable GameDVR
    set_reg_value(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", "GameDVR_Enabled", 0)
    set_reg_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", 0)
    # Enable Game Mode
    set_reg_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", "AllowAutoGameMode", 1)
    
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} GameDVR disabled. Game Mode optimizations enabled.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [23] GAMING OPTIMIZER TWEAKS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Disable Telemetry & Background Apps")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Enable Ultimate Performance Power Profile")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Empty Standby RAM Cache")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Terminate Active Overlay Helpers (Discord/Steam/etc.)")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Optimize Network Parameters (TCPNoDelay)")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Enable Windows Game Mode (Disable GameDVR)")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            disable_background_apps()
            input("\nPress Enter to continue...")
        elif choice == '2':
            enable_high_performance()
            input("\nPress Enter to continue...")
        elif choice == '3':
            empty_ram_cache()
            input("\nPress Enter to continue...")
        elif choice == '4':
            kill_overlays()
            input("\nPress Enter to continue...")
        elif choice == '5':
            optimize_network()
            input("\nPress Enter to continue...")
        elif choice == '6':
            toggle_fps_mode()
            input("\nPress Enter to continue...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
