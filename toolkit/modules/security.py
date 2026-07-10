def show_menu():
    while True:
        print("\n=============================================================")
        print("              [4] SECURITY")
        print("=============================================================")
        print("[1] Block Website")
        print("[2] Unblock Website")
        print("[3] Firewall")
        print("[4] Windows Defender")
        print("[5] BitLocker")
        print("[6] Hosts File Editor")
        print("[7] Port Scanner")
        print("[8] Kill Process")
        print("[9] Startup Malware Scan")
        print("[10] Windows Security Status")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Block Website coming soon...")
        elif choice == '2':
            print("[INFO] Unblock Website coming soon...")
        elif choice == '3':
            print("[INFO] Firewall coming soon...")
        elif choice == '4':
            print("[INFO] Windows Defender coming soon...")
        elif choice == '5':
            print("[INFO] BitLocker coming soon...")
        elif choice == '6':
            print("[INFO] Hosts File Editor coming soon...")
        elif choice == '7':
            print("[INFO] Port Scanner coming soon...")
        elif choice == '8':
            print("[INFO] Kill Process coming soon...")
        elif choice == '9':
            print("[INFO] Startup Malware Scan coming soon...")
        elif choice == '10':
            print("[INFO] Windows Security Status coming soon...")
        else:
            print("[ERROR] Invalid choice.")
