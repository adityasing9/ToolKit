def show_menu():
    while True:
        print("\n=============================================================")
        print("              [6] FILE & FOLDER")
        print("=============================================================")
        print("[1] Hide File")
        print("[2] Unhide File")
        print("[3] Hide Folder")
        print("[4] Unhide Folder")
        print("[5] Secure Folder")
        print("[6] Unlock Folder")
        print("[7] Encrypt Folder")
        print("[8] Decrypt Folder")
        print("[9] Find Large Files")
        print("[10] Duplicate Finder")
        print("[11] Folder Size")
        print("[12] Rename Multiple Files")
        print("[13] Compress")
        print("[14] Extract ZIP")
        print("[15] File Hash")
        print("[16] Secure Delete")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Hide File coming soon...")
        elif choice == '2':
            print("[INFO] Unhide File coming soon...")
        elif choice == '3':
            print("[INFO] Hide Folder coming soon...")
        elif choice == '4':
            print("[INFO] Unhide Folder coming soon...")
        elif choice == '5':
            print("[INFO] Secure Folder coming soon...")
        elif choice == '6':
            print("[INFO] Unlock Folder coming soon...")
        elif choice == '7':
            print("[INFO] Encrypt Folder coming soon...")
        elif choice == '8':
            print("[INFO] Decrypt Folder coming soon...")
        elif choice == '9':
            print("[INFO] Find Large Files coming soon...")
        elif choice == '10':
            print("[INFO] Duplicate Finder coming soon...")
        elif choice == '11':
            print("[INFO] Folder Size coming soon...")
        elif choice == '12':
            print("[INFO] Rename Multiple Files coming soon...")
        elif choice == '13':
            print("[INFO] Compress coming soon...")
        elif choice == '14':
            print("[INFO] Extract ZIP coming soon...")
        elif choice == '15':
            print("[INFO] File Hash coming soon...")
        elif choice == '16':
            print("[INFO] Secure Delete coming soon...")
        else:
            print("[ERROR] Invalid choice.")
