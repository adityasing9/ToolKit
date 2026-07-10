def show_menu():
    while True:
        print("\n=============================================================")
        print("              [5] NETWORKING")
        print("=============================================================")
        print("[1] Public IP")
        print("[2] Local IP")
        print("[3] MAC Address")
        print("[4] DNS")
        print("[5] Flush DNS")
        print("[6] Ping")
        print("[7] Traceroute")
        print("[8] Port Check")
        print("[9] WiFi Passwords")
        print("[10] Connected Devices")
        print("[11] Open Ports")
        print("[12] Network Speed Test")
        print("[13] Proxy Settings")
        print("[14] VPN Status")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Public IP coming soon...")
        elif choice == '2':
            print("[INFO] Local IP coming soon...")
        elif choice == '3':
            print("[INFO] MAC Address coming soon...")
        elif choice == '4':
            print("[INFO] DNS coming soon...")
        elif choice == '5':
            print("[INFO] Flush DNS coming soon...")
        elif choice == '6':
            print("[INFO] Ping coming soon...")
        elif choice == '7':
            print("[INFO] Traceroute coming soon...")
        elif choice == '8':
            print("[INFO] Port Check coming soon...")
        elif choice == '9':
            print("[INFO] WiFi Passwords coming soon...")
        elif choice == '10':
            print("[INFO] Connected Devices coming soon...")
        elif choice == '11':
            print("[INFO] Open Ports coming soon...")
        elif choice == '12':
            print("[INFO] Network Speed Test coming soon...")
        elif choice == '13':
            print("[INFO] Proxy Settings coming soon...")
        elif choice == '14':
            print("[INFO] VPN Status coming soon...")
        else:
            print("[ERROR] Invalid choice.")
