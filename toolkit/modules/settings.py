from toolkit.utils import Colors
import os
import sys
import subprocess

def apply_theme(color_code):
    print(f"\n[INFO] Applying Theme...")
    try:
        # Changes standard windows cmd color globally
        os.system(f"color {color_code}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Theme applied.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not apply theme: {e}")

def change_font_size():
    print("\n[INFO] Font size cannot be changed programmatically in all terminals.")
    print("Please use 'Ctrl + Mouse Wheel' or Terminal settings to change font size.")

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
    print("\n[WARNING] This will reset your theme and settings.")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        os.system("color 07")
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
        print(f"{Colors.BOLD}{Colors.YELLOW}              [12] SETTINGS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Theme (Current)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Theme: Light")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Theme: Dark")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Theme: Cyberpunk")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Theme: Green Matrix")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Theme: Purple")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Theme: Blue")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Font Size")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Update Toolkit")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Backup")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Restore")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Check Version")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Plugins")
        print(f"{Colors.GREEN}[14]{Colors.RESET} Extensions")
        print(f"{Colors.GREEN}[15]{Colors.RESET} Reset")
        print(f"{Colors.GREEN}[16]{Colors.RESET} Configure API / Cloud Keys")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Use options 2-7 to change the theme.")
        elif choice == '2':
            apply_theme("F0") # White bg, black text
        elif choice == '3':
            apply_theme("07") # Black bg, white text
        elif choice == '4':
            apply_theme("0D") # Black bg, Light Magenta text
        elif choice == '5':
            apply_theme("0A") # Black bg, Light Green text
        elif choice == '6':
            apply_theme("05") # Black bg, Purple text
        elif choice == '7':
            apply_theme("09") # Black bg, Light Blue text
        elif choice == '8':
            change_font_size()
        elif choice == '9':
            update_toolkit()
        elif choice == '10':
            backup_toolkit()
        elif choice == '11':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Restore functionality coming soon...")
        elif choice == '12':
            check_version()
        elif choice == '13' or choice == '14':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Plugin/Extension system coming in v2.0.")
        elif choice == '15':
            reset_toolkit()
        elif choice == '16':
            configure_keys()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
