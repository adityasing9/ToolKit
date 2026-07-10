def show_menu():
    while True:
        print("\n=============================================================")
        print("              [2] WINDOWS TOOLKIT")
        print("=============================================================")
        print("[1] Activation")
        print("[2] Drivers")
        print("[3] Windows Update")
        print("[4] Services")
        print("[5] Startup Apps")
        print("[6] Installed Apps")
        print("[7] Repair Windows")
        print("[8] DISM Scan")
        print("[9] SFC Scan")
        print("[10] Disk Check")
        print("[11] Restore Point")
        print("[12] Environment Variables")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Activation tools coming soon...")
        elif choice == '2':
            print("[INFO] Drivers tools coming soon...")
        elif choice == '3':
            print("[INFO] Windows Update coming soon...")
        elif choice == '4':
            print("[INFO] Services coming soon...")
        elif choice == '5':
            print("[INFO] Startup Apps coming soon...")
        elif choice == '6':
            print("[INFO] Installed Apps coming soon...")
        elif choice == '7':
            print("[INFO] Repair Windows coming soon...")
        elif choice == '8':
            import subprocess
            print("[INFO] Running DISM Scan...")
            try:
                subprocess.run(["dism", "/Online", "/Cleanup-Image", "/ScanHealth"])
            except Exception as e:
                print(f"[ERROR] {e}")
        elif choice == '9':
            import subprocess
            print("[INFO] Running SFC Scan...")
            try:
                subprocess.run(["sfc", "/scannow"])
            except Exception as e:
                print(f"[ERROR] {e}")
        elif choice == '10':
            print("[INFO] Disk Check coming soon...")
        elif choice == '11':
            print("[INFO] Restore Point coming soon...")
        elif choice == '12':
            print("[INFO] Environment Variables coming soon...")
        else:
            print("[ERROR] Invalid choice.")
