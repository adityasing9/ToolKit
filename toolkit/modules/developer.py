def show_menu():
    while True:
        print("\n=============================================================")
        print("              [8] DEVELOPER TOOLS")
        print("=============================================================")
        print("[1] Git")
        print("[2] Clone Repo")
        print("[3] Commit")
        print("[4] Push")
        print("[5] Pull")
        print("[6] Status")
        print("[7] Branch")
        print("[8] Github URLs")
        print("[9] SSH Keys")
        print("[10] Docker")
        print("[11] Node")
        print("[12] Python")
        print("[13] Java")
        print("[14] Rust")
        print("[15] Go")
        print("[16] Flutter")
        print("[17] Android")
        print("[18] VS Code")
        print("[19] WSL")
        print("[20] VirtualBox")
        print("[21] VMware")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Git coming soon...")
        elif choice == '2':
            print("[INFO] Clone Repo coming soon...")
        elif choice == '3':
            print("[INFO] Commit coming soon...")
        elif choice == '4':
            print("[INFO] Push coming soon...")
        elif choice == '5':
            print("[INFO] Pull coming soon...")
        elif choice == '6':
            print("[INFO] Status coming soon...")
        elif choice == '7':
            print("[INFO] Branch coming soon...")
        elif choice == '8':
            print("[INFO] Github URLs coming soon...")
        elif choice == '9':
            print("[INFO] SSH Keys coming soon...")
        elif choice == '10':
            print("[INFO] Docker coming soon...")
        elif choice == '11':
            print("[INFO] Node coming soon...")
        elif choice == '12':
            print("[INFO] Python coming soon...")
        elif choice == '13':
            print("[INFO] Java coming soon...")
        elif choice == '14':
            print("[INFO] Rust coming soon...")
        elif choice == '15':
            print("[INFO] Go coming soon...")
        elif choice == '16':
            print("[INFO] Flutter coming soon...")
        elif choice == '17':
            print("[INFO] Android coming soon...")
        elif choice == '18':
            print("[INFO] VS Code coming soon...")
        elif choice == '19':
            print("[INFO] WSL coming soon...")
        elif choice == '20':
            print("[INFO] VirtualBox coming soon...")
        elif choice == '21':
            print("[INFO] VMware coming soon...")
        else:
            print("[ERROR] Invalid choice.")
