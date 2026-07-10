import os
import sys
import subprocess

def apply_theme(color_code):
    print(f"\n[INFO] Applying Theme...")
    try:
        # Changes standard windows cmd color globally
        os.system(f"color {color_code}")
        print("[SUCCESS] Theme applied.")
    except Exception as e:
        print(f"[ERROR] Could not apply theme: {e}")

def change_font_size():
    print("\n[INFO] Font size cannot be changed programmatically in all terminals.")
    print("Please use 'Ctrl + Mouse Wheel' or Terminal settings to change font size.")

def update_toolkit():
    print("\n[INFO] Checking for Toolkit updates from Github...")
    try:
        subprocess.run(["git", "pull"])
    except Exception as e:
        print(f"[ERROR] Failed to update: {e}")

def backup_toolkit():
    print("\n[INFO] Backing up Toolkit...")
    print("Run Export in [1] Storage & Notes to backup the Database.")

def check_version():
    print("\n--- TERMINAL TOOLKIT VERSION ---")
    print("Version: 1.0 (CLI Edition)")
    print("Build: Latest GitHub Main Branch")

def reset_toolkit():
    print("\n[WARNING] This will reset your theme and settings.")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        os.system("color 07")
        print("[SUCCESS] Settings reset to default.")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [16] SETTINGS")
        print("=============================================================")
        print("[1] Theme (Current)")
        print("[2] Theme: Light")
        print("[3] Theme: Dark")
        print("[4] Theme: Cyberpunk")
        print("[5] Theme: Green Matrix")
        print("[6] Theme: Purple")
        print("[7] Theme: Blue")
        print("[8] Font Size")
        print("[9] Update Toolkit")
        print("[10] Backup")
        print("[11] Restore")
        print("[12] Check Version")
        print("[13] Plugins")
        print("[14] Extensions")
        print("[15] Reset")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Use options 2-7 to change the theme.")
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
            print("[INFO] Restore functionality coming soon...")
        elif choice == '12':
            check_version()
        elif choice == '13' or choice == '14':
            print("[INFO] Plugin/Extension system coming in v2.0.")
        elif choice == '15':
            reset_toolkit()
        else:
            print("[ERROR] Invalid choice.")
