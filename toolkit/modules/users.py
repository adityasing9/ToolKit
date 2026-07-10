def show_menu():
    while True:
        print("\n=============================================================")
        print("              [3] USER MANAGEMENT")
        print("=============================================================")
        print("[1] List Users")
        print("[2] Add User")
        print("[3] Delete User")
        print("[4] Change Password")
        print("[5] Lock User")
        print("[6] Unlock User")
        print("[7] Enable User")
        print("[8] Disable User")
        print("[9] Grant Administrator")
        print("[10] Remove Administrator")
        print("[11] Last Login")
        print("[12] Password Expiry")
        print("[13] Account Information")
        print("[14] Export User List")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] List Users coming soon...")
        elif choice == '2':
            print("[INFO] Add User coming soon...")
        elif choice == '3':
            print("[INFO] Delete User coming soon...")
        elif choice == '4':
            print("[INFO] Change Password coming soon...")
        elif choice == '5':
            print("[INFO] Lock User coming soon...")
        elif choice == '6':
            print("[INFO] Unlock User coming soon...")
        elif choice == '7':
            print("[INFO] Enable User coming soon...")
        elif choice == '8':
            print("[INFO] Disable User coming soon...")
        elif choice == '9':
            print("[INFO] Grant Administrator coming soon...")
        elif choice == '10':
            print("[INFO] Remove Administrator coming soon...")
        elif choice == '11':
            print("[INFO] Last Login coming soon...")
        elif choice == '12':
            print("[INFO] Password Expiry coming soon...")
        elif choice == '13':
            print("[INFO] Account Information coming soon...")
        elif choice == '14':
            print("[INFO] Export User List coming soon...")
        else:
            print("[ERROR] Invalid choice.")
