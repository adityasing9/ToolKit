def show_menu():
    while True:
        print("\n=============================================================")
        print("              [13] RUN COMMANDS")
        print("=============================================================")
        print("[1] List Commands")
        print("[2] Search Command")
        print("[3] Execute Command")
        print("[4] Add Command")
        print("[5] Delete Command")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] List Commands coming soon...")
        elif choice == '2':
            print("[INFO] Search Command coming soon...")
        elif choice == '3':
            print("[INFO] Execute Command coming soon...")
        elif choice == '4':
            print("[INFO] Add Command coming soon...")
        elif choice == '5':
            print("[INFO] Delete Command coming soon...")
        else:
            print("[ERROR] Invalid choice.")
