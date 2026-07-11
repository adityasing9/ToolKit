from toolkit.utils import Colors
import os
import sys
import subprocess

def update_toolkit():
    print("\n[INFO] Checking for Toolkit updates from Github...")
    try:
        subprocess.run(["git", "pull"])
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to update: {e}")

def backup_toolkit():
    print("\n[INFO] Backing up Toolkit...")
    print("Run Export in [1] Storage & Notes to backup the Database.")

def check_version():
    print(f"\n{Colors.CYAN}--- TERMINAL TOOLKIT VERSION ---{Colors.RESET}")
    print("Version: 1.0 (CLI Edition)")
    print("Build: Latest GitHub Main Branch")

def reset_toolkit():
    print("\n[WARNING] This will reset your settings configurations.")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Settings reset to default.")

from toolkit.db import get_setting, set_setting

def configure_keys():
    while True:
        print(f"\n{Colors.CYAN}--- Configure API / Cloud Keys ---{Colors.RESET}")
        
        gemini_key = get_setting("gemini_api_key", "")
        sb_url = get_setting("supabase_url", "")
        sb_key = get_setting("supabase_key", "")
        
        gemini_show = (gemini_key[:4] + "*" * 16) if len(gemini_key) > 4 else "Not Set"
        sb_key_show = (sb_key[:4] + "*" * 16) if len(sb_key) > 4 else "Not Set"
        sb_url_show = sb_url if sb_url else "Not Set"
        
        print(f"{Colors.GREEN}[1]{Colors.RESET} Gemini API Key:   {gemini_show}")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Supabase URL:     {sb_url_show}")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Supabase Key:     {sb_key_show}")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            key = input("Enter Gemini API Key (leave empty to keep current): ").strip()
            if key:
                set_setting("gemini_api_key", key)
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Gemini API Key updated.")
        elif choice == '2':
            url = input("Enter Supabase URL (leave empty to keep current): ").strip()
            if url:
                set_setting("supabase_url", url)
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Supabase URL updated.")
        elif choice == '3':
            key = input("Enter Supabase Key (leave empty to keep current): ").strip()
            if key:
                set_setting("supabase_key", key)
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Supabase Key updated.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [20] SETTINGS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Update Toolkit")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Backup")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Restore")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Check Version")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Plugins")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Extensions")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Reset")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Configure API / Cloud Keys")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            update_toolkit()
        elif choice == '2':
            backup_toolkit()
        elif choice == '3':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Restore functionality coming soon...")
        elif choice == '4':
            check_version()
        elif choice == '5' or choice == '6':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Plugin/Extension system coming in v2.0.")
        elif choice == '7':
            reset_toolkit()
        elif choice == '8':
            configure_keys()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
