import sys
import argparse
from toolkit.utils import Colors
from toolkit.db import init_db

Colors.init()
init_db()
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def print_header():
    print(f"{Colors.CYAN}============================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}              ⚡ TERMINAL TOOLKIT v1.0{Colors.RESET}")
    print(f"{Colors.CYAN}============================================================={Colors.RESET}")

def print_menu():
    print_header()
    print("\n[1] Storage & Notes")
    print(f"{Colors.GREEN}[2]{Colors.RESET} Windows Toolkit")
    print(f"{Colors.GREEN}[3]{Colors.RESET} User Management")
    print(f"{Colors.GREEN}[4]{Colors.RESET} Security")
    print(f"{Colors.GREEN}[5]{Colors.RESET} Networking")
    print(f"{Colors.GREEN}[6]{Colors.RESET} File & Folder")
    print(f"{Colors.GREEN}[7]{Colors.RESET} Downloads")
    print(f"{Colors.GREEN}[8]{Colors.RESET} Developer Tools")
    print(f"{Colors.GREEN}[9]{Colors.RESET} Productivity")
    print(f"{Colors.GREEN}[10]{Colors.RESET} QR / Barcode")
    print(f"{Colors.GREEN}[11]{Colors.RESET} System Information")
    print(f"{Colors.GREEN}[12]{Colors.RESET} Cleanup & Maintenance")
    print(f"{Colors.GREEN}[13]{Colors.RESET} Run Commands")
    print(f"{Colors.GREEN}[14]{Colors.RESET} Cloud Workspace")
    print(f"{Colors.GREEN}[15]{Colors.RESET} AI Assistant")
    print(f"{Colors.GREEN}[16]{Colors.RESET} Settings")
    print(f"{Colors.GREEN}[0]{Colors.RESET} Exit\n")

def main():
    parser = argparse.ArgumentParser(description="Terminal Toolkit CLI")
    parser.add_argument("module", nargs="?", help="Directly launch a specific module (e.g. github, notes, ssh)")
    args = parser.parse_args()

    # Handle direct CLI arguments
    if args.module:
        module_name = args.module.lower()
        if module_name in ['1', 'storage', 'notes']:
            from toolkit.modules import storage
            storage.show_menu()
        elif module_name in ['2', 'windows', 'toolkit']:
            from toolkit.modules import windows_tools
            windows_tools.show_menu()
        elif module_name in ['3', 'user', 'users']:
            from toolkit.modules import users
            users.show_menu()
        elif module_name in ['4', 'security']:
            from toolkit.modules import security
            security.show_menu()
        elif module_name in ['5', 'network', 'networking']:
            from toolkit.modules import network
            network.show_menu()
        elif module_name in ['6', 'file', 'files']:
            from toolkit.modules import files
            files.show_menu()
        elif module_name in ['7', 'download', 'downloads']:
            from toolkit.modules import downloads
            downloads.show_menu()
        elif module_name in ['8', 'dev', 'developer']:
            from toolkit.modules import developer
            developer.show_menu()
        elif module_name in ['9', 'productivity']:
            from toolkit.modules import productivity
            productivity.show_menu()
        elif module_name in ['10', 'qr', 'barcode']:
            from toolkit.modules import qr
            qr.show_menu()
        elif module_name in ['11', 'sysinfo', 'info']:
            from toolkit.modules import sysinfo
            sysinfo.show_menu()
        elif module_name in ['12', 'clean', 'cleanup']:
            from toolkit.modules import cleanup
            cleanup.show_menu()
        elif module_name in ['13', 'commands', 'encyclopedia']:
            from toolkit.modules import encyclopedia
            encyclopedia.show_menu()
        elif module_name in ['14', 'cloud', 'workspace']:
            from toolkit.modules import cloud
            cloud.show_menu()
        elif module_name in ['15', 'ai', 'assistant']:
            from toolkit.modules import ai
            ai.show_menu()
        elif module_name in ['16', 'settings', 'theme']:
            from toolkit.modules import settings
            settings.show_menu()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Unknown module '{module_name}'")
        sys.exit(0)

    # Main Interactive Loop
    while True:
        print_menu()
        try:
            choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if choice == '0':
            print("Exiting...")
            break
        elif choice == '1':
            from toolkit.modules import storage
            storage.show_menu()
        elif choice == '2':
            from toolkit.modules import windows_tools
            windows_tools.show_menu()
        elif choice == '3':
            from toolkit.modules import users
            users.show_menu()
        elif choice == '4':
            from toolkit.modules import security
            security.show_menu()
        elif choice == '5':
            from toolkit.modules import network
            network.show_menu()
        elif choice == '6':
            from toolkit.modules import files
            files.show_menu()
        elif choice == '7':
            from toolkit.modules import downloads
            downloads.show_menu()
        elif choice == '8':
            from toolkit.modules import developer
            developer.show_menu()
        elif choice == '9':
            from toolkit.modules import productivity
            productivity.show_menu()
        elif choice == '10':
            from toolkit.modules import qr
            qr.show_menu()
        elif choice == '11':
            from toolkit.modules import sysinfo
            sysinfo.show_menu()
        elif choice == '12':
            from toolkit.modules import cleanup
            cleanup.show_menu()
        elif choice == '13':
            from toolkit.modules import encyclopedia
            encyclopedia.show_menu()
        elif choice == '14':
            from toolkit.modules import cloud
            cloud.show_menu()
        elif choice == '15':
            from toolkit.modules import ai
            ai.show_menu()
        elif choice == '16':
            from toolkit.modules import settings
            settings.show_menu()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
