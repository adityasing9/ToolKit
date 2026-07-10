def show_menu():
    while True:
        print("\n=============================================================")
        print("              [11] SYSTEM INFORMATION")
        print("=============================================================")
        print("[1] CPU")
        print("[2] RAM")
        print("[3] GPU")
        print("[4] Disk")
        print("[5] Battery")
        print("[6] Motherboard")
        print("[7] BIOS")
        print("[8] Windows Version")
        print("[9] Installed Programs")
        print("[10] Startup Time")
        print("[11] Processes")
        print("[12] Running Services")
        print("[13] Disk Usage")
        print("[14] Temperature")
        print("[15] Health")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] CPU coming soon...")
        elif choice == '2':
            print("[INFO] RAM coming soon...")
        elif choice == '3':
            print("[INFO] GPU coming soon...")
        elif choice == '4':
            print("[INFO] Disk coming soon...")
        elif choice == '5':
            print("[INFO] Battery coming soon...")
        elif choice == '6':
            print("[INFO] Motherboard coming soon...")
        elif choice == '7':
            print("[INFO] BIOS coming soon...")
        elif choice == '8':
            print("[INFO] Windows Version coming soon...")
        elif choice == '9':
            print("[INFO] Installed Programs coming soon...")
        elif choice == '10':
            print("[INFO] Startup Time coming soon...")
        elif choice == '11':
            print("[INFO] Processes coming soon...")
        elif choice == '12':
            print("[INFO] Running Services coming soon...")
        elif choice == '13':
            print("[INFO] Disk Usage coming soon...")
        elif choice == '14':
            print("[INFO] Temperature coming soon...")
        elif choice == '15':
            print("[INFO] Health coming soon...")
        else:
            print("[ERROR] Invalid choice.")
