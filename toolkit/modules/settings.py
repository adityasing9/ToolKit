def show_menu():
    while True:
        print("\n=============================================================")
        print("              [16] SETTINGS")
        print("=============================================================")
        print("[1] Theme")
        print("[2] Light")
        print("[3] Dark")
        print("[4] Cyberpunk")
        print("[5] Green Matrix")
        print("[6] Purple")
        print("[7] Blue")
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
            print("[INFO] Theme coming soon...")
        elif choice == '2':
            print("[INFO] Light coming soon...")
        elif choice == '3':
            print("[INFO] Dark coming soon...")
        elif choice == '4':
            print("[INFO] Cyberpunk coming soon...")
        elif choice == '5':
            print("[INFO] Green Matrix coming soon...")
        elif choice == '6':
            print("[INFO] Purple coming soon...")
        elif choice == '7':
            print("[INFO] Blue coming soon...")
        elif choice == '8':
            print("[INFO] Font Size coming soon...")
        elif choice == '9':
            print("[INFO] Update Toolkit coming soon...")
        elif choice == '10':
            print("[INFO] Backup coming soon...")
        elif choice == '11':
            print("[INFO] Restore coming soon...")
        elif choice == '12':
            print("[INFO] Check Version coming soon...")
        elif choice == '13':
            print("[INFO] Plugins coming soon...")
        elif choice == '14':
            print("[INFO] Extensions coming soon...")
        elif choice == '15':
            print("[INFO] Reset coming soon...")
        else:
            print("[ERROR] Invalid choice.")
