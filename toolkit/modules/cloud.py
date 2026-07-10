def show_menu():
    while True:
        print("\n=============================================================")
        print("              [14] CLOUD WORKSPACE")
        print("=============================================================")
        print("[1] Saved Links")
        print("[2] Commands")
        print("[3] Secrets")
        print("[4] SSH Keys")
        print("[5] API Keys")
        print("[6] Environment Variables")
        print("[7] Server List")
        print("[8] Remote Notes")
        print("[9] Projects")
        print("[10] Terminal Chat")
        print("[11] Sync")
        print("[12] Backup")
        print("[13] Restore")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Please use [1] Storage & Notes for Saved Links.")
        elif choice == '2':
            print("[INFO] Please use [13] Run Commands for local commands.")
        elif choice == '3' or choice == '5':
            print("[INFO] Secrets and API Key management coming soon in Cloud Sync.")
        elif choice == '4':
            print("[INFO] Please use [8] Developer Tools for SSH Keys.")
        elif choice == '6':
            print("[INFO] Please use [2] Windows Toolkit for local Environment Variables.")
        elif choice == '7':
            print("[INFO] Remote Server management (SSH) coming soon.")
        elif choice == '8':
            print("[INFO] Please use [1] Storage & Notes for local notes.")
        elif choice == '9' or choice == '10':
            print("[INFO] Cloud Projects and Terminal Chat coming in v2.0.")
        elif choice == '11':
            print("[INFO] Cloud Sync requires an active account. Coming soon.")
        elif choice == '12':
            print("[INFO] Cloud Backup coming soon.")
        elif choice == '13':
            print("[INFO] Cloud Restore coming soon.")
        else:
            print("[ERROR] Invalid choice.")
