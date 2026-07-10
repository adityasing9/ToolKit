def show_menu():
    while True:
        print("\n=============================================================")
        print("              [1] STORAGE & NOTES")
        print("=============================================================")
        print("[1] Links")
        print("[2] Github")
        print("[3] Commands")
        print("[4] Snippets")
        print("[5] Clipboard History")
        print("[6] Quick Notes")
        print("[7] Bookmarks")
        print("[8] Favorites")
        print("[9] Tags")
        print("[10] Import / Export")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Links module coming soon...")
        elif choice == '2':
            print("[INFO] Github module coming soon...")
        elif choice == '3':
            print("[INFO] Commands module coming soon...")
        elif choice == '4':
            print("[INFO] Snippets module coming soon...")
        elif choice == '5':
            print("[INFO] Clipboard History coming soon...")
        elif choice == '6':
            print("[INFO] Quick Notes coming soon...")
        elif choice == '7':
            print("[INFO] Bookmarks coming soon...")
        elif choice == '8':
            print("[INFO] Favorites coming soon...")
        elif choice == '9':
            print("[INFO] Tags coming soon...")
        elif choice == '10':
            print("[INFO] Import/Export coming soon...")
        else:
            print("[ERROR] Invalid choice.")
