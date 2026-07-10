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
            print("[INFO] Saved Links coming soon...")
        elif choice == '2':
            print("[INFO] Commands coming soon...")
        elif choice == '3':
            print("[INFO] Secrets coming soon...")
        elif choice == '4':
            print("[INFO] SSH Keys coming soon...")
        elif choice == '5':
            print("[INFO] API Keys coming soon...")
        elif choice == '6':
            print("[INFO] Environment Variables coming soon...")
        elif choice == '7':
            print("[INFO] Server List coming soon...")
        elif choice == '8':
            print("[INFO] Remote Notes coming soon...")
        elif choice == '9':
            print("[INFO] Projects coming soon...")
        elif choice == '10':
            print("[INFO] Terminal Chat coming soon...")
        elif choice == '11':
            print("[INFO] Sync coming soon...")
        elif choice == '12':
            print("[INFO] Backup coming soon...")
        elif choice == '13':
            print("[INFO] Restore coming soon...")
        else:
            print("[ERROR] Invalid choice.")
