from toolkit.utils import Colors
def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [14] CLOUD WORKSPACE{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Saved Links")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Commands")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Secrets")
        print(f"{Colors.GREEN}[4]{Colors.RESET} SSH Keys")
        print(f"{Colors.GREEN}[5]{Colors.RESET} API Keys")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Environment Variables")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Server List")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Remote Notes")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Projects")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Terminal Chat")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Sync")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Backup")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Restore")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use [1] Storage & Notes for Saved Links.")
        elif choice == '2':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use [13] Run Commands for local commands.")
        elif choice == '3' or choice == '5':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Secrets and API Key management coming soon in Cloud Sync.")
        elif choice == '4':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use [8] Developer Tools for SSH Keys.")
        elif choice == '6':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use [2] Windows Toolkit for local Environment Variables.")
        elif choice == '7':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Remote Server management (SSH) coming soon.")
        elif choice == '8':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use [1] Storage & Notes for local notes.")
        elif choice == '9' or choice == '10':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cloud Projects and Terminal Chat coming in v2.0.")
        elif choice == '11':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cloud Sync requires an active account. Coming soon.")
        elif choice == '12':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cloud Backup coming soon.")
        elif choice == '13':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cloud Restore coming soon.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
