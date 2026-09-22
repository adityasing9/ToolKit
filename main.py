import sys
import argparse
from toolkit.utils import Colors
from toolkit.db import init_db

Colors.init()
init_db()
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

MENU_ITEMS = [
    (1, "AI Assistant"), (2, "Cheat Sheets & Docs"), (3, "Cleanup & Maintenance"),
    (4, "Cloud Workspace"), (5, "Developer Tools"), (6, "Downloads"),
    (7, "Driver Manager"), (8, "File & Folder"), (9, "Gaming Optimizer"),
    (10, "Local Network Dashboard"), (11, "Media Tools"), (12, "Network Monitor"),
    (13, "Networking"), (14, "Process Manager"), (15, "Productivity"),
    (16, "QR / Barcode"), (17, "Remote Device Manager"), (18, "Run Commands"),
    (19, "Security"), (20, "Settings"), (21, "Storage & Notes"),
    (22, "System Information"), (23, "Universal Search"), (24, "User Management"),
    (25, "Windows Analytics"), (26, "Windows Toolkit"), (0, "Exit")
]

TOTAL_MENU_WIDTH = 85

def print_header():
    print(f"{Colors.CYAN}{'=' * TOTAL_MENU_WIDTH}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'⚡ TERMINAL TOOLKIT v1.0'.center(TOTAL_MENU_WIDTH)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * TOTAL_MENU_WIDTH}{Colors.RESET}")

def print_menu():
    print_header()
    col1 = MENU_ITEMS[0:9]
    col2 = MENU_ITEMS[9:18]
    col3 = MENU_ITEMS[18:27]

    def format_item(num, title, width):
        text = f"[{num}] {title}"
        colored = f"{Colors.GREEN}[{num}]{Colors.RESET} {title}"
        padding = " " * max(0, width - len(text))
        return colored + padding

    w1, w2, w3 = 29, 31, 25
    print()
    for i in range(9):
        c1 = format_item(*col1[i], w1)
        c2 = format_item(*col2[i], w2)
        c3 = format_item(*col3[i], w3)
        print(f"{c1}{c2}{c3}")
    print()

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
        elif module_name in ['2', 'docs', 'cheat', 'cheatsheet', 'git', 'sql', 'regex', 'markdown']:
            from toolkit.modules import docs_cheatsheets
            docs_cheatsheets.show_menu()
        elif module_name in ['3', 'clean', 'cleanup', 'flush', 'clear', 'purge']:
            from toolkit.modules import cleanup
            cleanup.show_menu()
        elif module_name in ['4', 'cloud', 'workspace', 'supabase', 'sync', 'backup', 'restore']:
            from toolkit.modules import cloud
            cloud.show_menu()
        elif module_name in ['5', 'dev', 'developer', 'ssh', 'env', 'sdk']:
            from toolkit.modules import developer
            developer.show_menu()
        elif module_name in ['6', 'download', 'downloads', 'youtube', 'yt', 'ytdl', 'video', 'mp3']:
            from toolkit.modules import downloads
            downloads.show_menu()
        elif module_name in ['7', 'driver', 'drivers', 'pnputil', 'dism-driver', 'backup-drivers']:
            from toolkit.modules import driver_manager
            driver_manager.show_menu()
        elif module_name in ['8', 'file', 'files', 'folder', 'folders', 'shred', 'zip', 'hash', 'timestamp']:
            from toolkit.modules import files
            files.show_menu()
        elif module_name in ['9', 'gameopt', 'fps', 'optimize-game', 'game', 'gaming']:
            from toolkit.modules import gaming_optimizer
            gaming_optimizer.show_menu()
        elif module_name in ['10', 'networkdashboard', 'netdash', 'subnet', 'discover', 'devices', 'arp']:
            from toolkit.modules import network_dashboard
            network_dashboard.show_menu()
        elif module_name in ['11', 'media', 'image', 'pdf', 'ocr', 'audio', 'video', 'convert', 'resize', 'optimize']:
            from toolkit.modules import media_tools
            media_tools.show_menu()
        elif module_name in ['12', 'networkmonitor', 'netmon', 'traffic', 'bandwidth', 'latency', 'dns', 'vpn']:
            from toolkit.modules import network_monitor
            network_monitor.show_menu()
        elif module_name in ['13', 'network', 'networking', 'ip', 'ping', 'wifi', 'speed', 'speedtest', 'whois']:
            from toolkit.modules import network
            network.show_menu()
        elif module_name in ['14', 'process', 'proc', 'kill', 'taskmgr', 'monitor', 'pstree', 'startup']:
            from toolkit.modules import process_manager
            process_manager.show_menu()
        elif module_name in ['15', 'productivity', 'timer', 'stopwatch', 'password', 'json', 'base64']:
            from toolkit.modules import productivity
            productivity.show_menu()
        elif module_name in ['16', 'qr', 'barcode', 'wifiqr']:
            from toolkit.modules import qr
            qr.show_menu()
        elif module_name in ['17', 'remote', 'agent', 'pair', 'rterminal', 'rconnect', 'remotemanager']:
            from toolkit.modules import remote_manager
            remote_manager.show_menu()
        elif module_name in ['18', 'commands', 'cmd', 'run', 'encyclopedia', 'catalog']:
            from toolkit.modules import encyclopedia
            encyclopedia.show_menu()
        elif module_name in ['19', 'security', 'firewall', 'ports', 'hosts', 'bitlocker']:
            from toolkit.modules import security
            security.show_menu()
        elif module_name in ['20', 'settings', 'theme', 'config']:
            from toolkit.modules import settings
            settings.show_menu()
        elif module_name in ['21', 'storage', 'notes', 'links', 'snippets', 'db']:
            from toolkit.modules import storage
            storage.show_menu()
        elif module_name in ['deep', 'inspect', 'specs', 'spec', 'audit', 'hardware', 'fullspecs']:
            from toolkit.modules import deep_inspect
            deep_inspect.run_deep_inspection()
        elif module_name in ['22', 'sysinfo', 'info', 'temp', 'temperature', 'cpu', 'ram', 'gpu', 'battery', 'dashboard', 'dash', 'status']:
            if module_name in ['dashboard', 'dash', 'status']:
                from toolkit.modules import dashboard
                dashboard.show_dashboard()
            else:
                from toolkit.modules import sysinfo
                sysinfo.show_menu()
        elif module_name in ['23', 'search', 'find', 'query', 'ask']:
            from toolkit.modules import dashboard
            print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}              🔍 UNIVERSAL SEARCH ENGINE{Colors.RESET}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            query = input(f"{Colors.MAGENTA}Search Anything... > {Colors.RESET}").strip()
            if query:
                dashboard.search_everything(query)
        elif module_name in ['24', 'user', 'users', 'admin', 'accounts']:
            from toolkit.modules import users
            users.show_menu()
        elif module_name in ['25', 'analytics', 'telemetry', 'boothistory', 'battery', 'history', 'usage']:
            from toolkit.modules import windows_analytics
            windows_analytics.show_menu()
        elif module_name in ['26', 'windows', 'toolkit', 'sfc', 'dism', 'restorepoint', 'activate', 'activation']:
            from toolkit.modules import windows_tools
            windows_tools.show_menu()
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
        elif choice.lower() in ['deep', 'inspect', 'specs', 'spec', 'audit', 'hardware', 'fullspecs']:
            from toolkit.modules import deep_inspect
            deep_inspect.run_deep_inspection()
        elif choice == '1':
            from toolkit.modules import ai
            ai.show_menu()
        elif choice == '2':
            from toolkit.modules import docs_cheatsheets
            docs_cheatsheets.show_menu()
        elif choice == '3':
            from toolkit.modules import cleanup
            cleanup.show_menu()
        elif choice == '4':
            from toolkit.modules import cloud
            cloud.show_menu()
        elif choice == '5':
            from toolkit.modules import developer
            developer.show_menu()
        elif choice == '6':
            from toolkit.modules import downloads
            downloads.show_menu()
        elif choice == '7':
            from toolkit.modules import driver_manager
            driver_manager.show_menu()
        elif choice == '8':
            from toolkit.modules import files
            files.show_menu()
        elif choice == '9':
            from toolkit.modules import gaming_optimizer
            gaming_optimizer.show_menu()
        elif choice == '10':
            from toolkit.modules import network_dashboard
            network_dashboard.show_menu()
        elif choice == '11':
            from toolkit.modules import media_tools
            media_tools.show_menu()
        elif choice == '12':
            from toolkit.modules import network_monitor
            network_monitor.show_menu()
        elif choice == '13':
            from toolkit.modules import network
            network.show_menu()
        elif choice == '14':
            from toolkit.modules import process_manager
            process_manager.show_menu()
        elif choice == '15':
            from toolkit.modules import productivity
            productivity.show_menu()
        elif choice == '16':
            from toolkit.modules import qr
            qr.show_menu()
        elif choice == '17':
            from toolkit.modules import remote_manager
            remote_manager.show_menu()
        elif choice == '18':
            from toolkit.modules import encyclopedia
            encyclopedia.show_menu()
        elif choice == '19':
            from toolkit.modules import security
            security.show_menu()
        elif choice == '20':
            from toolkit.modules import settings
            settings.show_menu()
        elif choice == '21':
            from toolkit.modules import storage
            storage.show_menu()
        elif choice == '22':
            from toolkit.modules import sysinfo
            sysinfo.show_menu()
        elif choice == '23':
            from toolkit.modules import dashboard
            print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}              🔍 UNIVERSAL SEARCH ENGINE{Colors.RESET}")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
            query = input(f"{Colors.MAGENTA}Search Anything... > {Colors.RESET}").strip()
            if query:
                dashboard.search_everything(query)
        elif choice == '24':
            from toolkit.modules import users
            users.show_menu()
        elif choice == '25':
            from toolkit.modules import windows_analytics
            windows_analytics.show_menu()
        elif choice == '26':
            from toolkit.modules import windows_tools
            windows_tools.show_menu()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
