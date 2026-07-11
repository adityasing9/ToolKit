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
    print(f"\n{Colors.GREEN}[1]{Colors.RESET} AI Assistant")
    print(f"{Colors.GREEN}[2]{Colors.RESET} Cleanup & Maintenance")
    print(f"{Colors.GREEN}[3]{Colors.RESET} Cloud Workspace")
    print(f"{Colors.GREEN}[4]{Colors.RESET} Developer Tools")
    print(f"{Colors.GREEN}[5]{Colors.RESET} Downloads")
    print(f"{Colors.GREEN}[6]{Colors.RESET} File & Folder")
    print(f"{Colors.GREEN}[7]{Colors.RESET} Networking")
    print(f"{Colors.GREEN}[8]{Colors.RESET} Productivity")
    print(f"{Colors.GREEN}[9]{Colors.RESET} QR / Barcode")
    print(f"{Colors.GREEN}[10]{Colors.RESET} Run Commands")
    print(f"{Colors.GREEN}[11]{Colors.RESET} Security")
    print(f"{Colors.GREEN}[12]{Colors.RESET} Settings")
    print(f"{Colors.GREEN}[13]{Colors.RESET} Storage & Notes")
    print(f"{Colors.GREEN}[14]{Colors.RESET} System Information")
    print(f"{Colors.GREEN}[15]{Colors.RESET} User Management")
    print(f"{Colors.GREEN}[16]{Colors.RESET} Windows Toolkit")
    print(f"{Colors.GREEN}[17]{Colors.RESET} Universal Search")
    print(f"{Colors.GREEN}[18]{Colors.RESET} Media Tools")
    print(f"{Colors.GREEN}[19]{Colors.RESET} Cheat Sheets & Docs")
    print(f"{Colors.GREEN}[20]{Colors.RESET} Process Manager")
    print(f"{Colors.GREEN}[21]{Colors.RESET} Network Monitor")
    print(f"{Colors.GREEN}[22]{Colors.RESET} Driver Manager")
    print(f"{Colors.GREEN}[23]{Colors.RESET} Gaming Optimizer")
    print(f"{Colors.GREEN}[24]{Colors.RESET} Windows Analytics")
    print(f"{Colors.GREEN}[25]{Colors.RESET} Local Network Dashboard")
    print(f"{Colors.GREEN}[0]{Colors.RESET} Exit\n")

def main():
    parser = argparse.ArgumentParser(description="Terminal Toolkit CLI")
    parser.add_argument("module", nargs="?", help="Directly launch a specific module (e.g. github, notes, ssh)")
    args = parser.parse_args()

    # Handle direct CLI arguments
    if args.module:
        module_name = args.module.lower()
        if module_name in ['1', 'ai', 'assistant', 'gpt', 'gemini', 'chat', 'bot']:
            from toolkit.modules import ai
            ai.show_menu()
        elif module_name in ['2', 'clean', 'cleanup', 'flush', 'clear', 'purge']:
            from toolkit.modules import cleanup
            cleanup.show_menu()
        elif module_name in ['3', 'cloud', 'workspace', 'supabase', 'sync', 'backup', 'restore']:
            from toolkit.modules import cloud
            cloud.show_menu()
        elif module_name in ['4', 'dev', 'developer', 'git', 'ssh', 'env', 'sdk']:
            from toolkit.modules import developer
            developer.show_menu()
        elif module_name in ['5', 'download', 'downloads', 'youtube', 'yt', 'ytdl', 'video', 'mp3']:
            from toolkit.modules import downloads
            downloads.show_menu()
        elif module_name in ['6', 'file', 'files', 'folder', 'folders', 'shred', 'zip', 'hash', 'timestamp']:
            from toolkit.modules import files
            files.show_menu()
        elif module_name in ['7', 'network', 'networking', 'ip', 'ping', 'wifi', 'speed', 'speedtest', 'dns', 'whois']:
            from toolkit.modules import network
            network.show_menu()
        elif module_name in ['8', 'productivity', 'timer', 'stopwatch', 'password', 'json', 'base64']:
            from toolkit.modules import productivity
            productivity.show_menu()
        elif module_name in ['9', 'qr', 'barcode', 'wifiqr']:
            from toolkit.modules import qr
            qr.show_menu()
        elif module_name in ['10', 'commands', 'cmd', 'run', 'encyclopedia', 'catalog']:
            from toolkit.modules import encyclopedia
            encyclopedia.show_menu()
        elif module_name in ['11', 'security', 'firewall', 'ports', 'hosts', 'bitlocker']:
            from toolkit.modules import security
            security.show_menu()
        elif module_name in ['12', 'settings', 'theme', 'config']:
            from toolkit.modules import settings
            settings.show_menu()
        elif module_name in ['13', 'storage', 'notes', 'links', 'snippets', 'db']:
            from toolkit.modules import storage
            storage.show_menu()
        elif module_name in ['14', 'sysinfo', 'info', 'specs', 'temp', 'temperature', 'cpu', 'ram', 'gpu', 'battery', 'dashboard', 'dash', 'status']:
            if module_name in ['dashboard', 'dash', 'status']:
                from toolkit.modules import dashboard
                dashboard.show_dashboard()
            else:
                from toolkit.modules import sysinfo
                sysinfo.show_menu()
        elif module_name in ['15', 'user', 'users', 'admin', 'accounts']:
            from toolkit.modules import users
            users.show_menu()
        elif module_name in ['16', 'windows', 'toolkit', 'sfc', 'dism', 'restorepoint', 'activate', 'activation']:
            from toolkit.modules import windows_tools
            windows_tools.show_menu()
        elif module_name in ['17', 'search', 'find', 'query', 'ask']:
            from toolkit.modules import dashboard
            print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}              🔍 UNIVERSAL SEARCH ENGINE{Colors.RESET}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            query = input(f"{Colors.MAGENTA}Search Anything... > {Colors.RESET}").strip()
            if query:
                dashboard.search_everything(query)
        elif module_name in ['18', 'media', 'image', 'pdf', 'ocr', 'audio', 'video', 'convert', 'resize', 'optimize']:
            from toolkit.modules import media_tools
            media_tools.show_menu()
        elif module_name in ['19', 'docs', 'cheat', 'cheatsheet', 'git', 'sql', 'regex', 'markdown']:
            from toolkit.modules import docs_cheatsheets
            docs_cheatsheets.show_menu()
        elif module_name in ['20', 'process', 'proc', 'kill', 'taskmgr', 'monitor', 'pstree', 'startup']:
            from toolkit.modules import process_manager
            process_manager.show_menu()
        elif module_name in ['21', 'networkmonitor', 'netmon', 'traffic', 'bandwidth', 'latency', 'dns', 'vpn']:
            from toolkit.modules import network_monitor
            network_monitor.show_menu()
        elif module_name in ['22', 'driver', 'drivers', 'pnputil', 'dism-driver', 'backup-drivers']:
            from toolkit.modules import driver_manager
            driver_manager.show_menu()
        elif module_name in ['23', 'gameopt', 'fps', 'optimize-game', 'game', 'gaming']:
            from toolkit.modules import gaming_optimizer
            gaming_optimizer.show_menu()
        elif module_name in ['24', 'analytics', 'telemetry', 'boothistory', 'battery', 'history', 'usage']:
            from toolkit.modules import windows_analytics
            windows_analytics.show_menu()
        elif module_name in ['25', 'networkdashboard', 'netdash', 'subnet', 'discover', 'devices', 'arp']:
            from toolkit.modules import network_dashboard
            network_dashboard.show_menu()
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
            from toolkit.modules import ai
            ai.show_menu()
        elif choice == '2':
            from toolkit.modules import cleanup
            cleanup.show_menu()
        elif choice == '3':
            from toolkit.modules import cloud
            cloud.show_menu()
        elif choice == '4':
            from toolkit.modules import developer
            developer.show_menu()
        elif choice == '5':
            from toolkit.modules import downloads
            downloads.show_menu()
        elif choice == '6':
            from toolkit.modules import files
            files.show_menu()
        elif choice == '7':
            from toolkit.modules import network
            network.show_menu()
        elif choice == '8':
            from toolkit.modules import productivity
            productivity.show_menu()
        elif choice == '9':
            from toolkit.modules import qr
            qr.show_menu()
        elif choice == '10':
            from toolkit.modules import encyclopedia
            encyclopedia.show_menu()
        elif choice == '11':
            from toolkit.modules import security
            security.show_menu()
        elif choice == '12':
            from toolkit.modules import settings
            settings.show_menu()
        elif choice == '13':
            from toolkit.modules import storage
            storage.show_menu()
        elif choice == '14':
            from toolkit.modules import sysinfo
            sysinfo.show_menu()
        elif choice == '15':
            from toolkit.modules import users
            users.show_menu()
        elif choice == '16':
            from toolkit.modules import windows_tools
            windows_tools.show_menu()
        elif choice == '17':
            from toolkit.modules import dashboard
            print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}              🔍 UNIVERSAL SEARCH ENGINE{Colors.RESET}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            query = input(f"{Colors.MAGENTA}Search Anything... > {Colors.RESET}").strip()
            if query:
                dashboard.search_everything(query)
        elif choice == '18':
            from toolkit.modules import media_tools
            media_tools.show_menu()
        elif choice == '19':
            from toolkit.modules import docs_cheatsheets
            docs_cheatsheets.show_menu()
        elif choice == '20':
            from toolkit.modules import process_manager
            process_manager.show_menu()
        elif choice == '21':
            from toolkit.modules import network_monitor
            network_monitor.show_menu()
        elif choice == '22':
            from toolkit.modules import driver_manager
            driver_manager.show_menu()
        elif choice == '23':
            from toolkit.modules import gaming_optimizer
            gaming_optimizer.show_menu()
        elif choice == '24':
            from toolkit.modules import windows_analytics
            windows_analytics.show_menu()
        elif choice == '25':
            from toolkit.modules import network_dashboard
            network_dashboard.show_menu()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
