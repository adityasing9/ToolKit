def show_menu():
    while True:
        print("\n=============================================================")
        print("              [12] CLEANUP & MAINTENANCE")
        print("=============================================================")
        print("[1] Temp")
        print("[2] Prefetch")
        print("[3] Windows Temp")
        print("[4] Recycle Bin")
        print("[5] DNS Cache")
        print("[6] Thumbnail Cache")
        print("[7] Recent Files")
        print("[8] PowerShell History")
        print("[9] Browser Cache")
        print("[10] Windows Logs")
        print("[11] Disk Cleanup")
        print("[12] Optimize Drives")
        print("[13] Winget Upgrade")
        print("[14] Winget Repair")
        print("[15] App Repair")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Temp coming soon...")
        elif choice == '2':
            print("[INFO] Prefetch coming soon...")
        elif choice == '3':
            print("[INFO] Windows Temp coming soon...")
        elif choice == '4':
            print("[INFO] Recycle Bin coming soon...")
        elif choice == '5':
            print("[INFO] DNS Cache coming soon...")
        elif choice == '6':
            print("[INFO] Thumbnail Cache coming soon...")
        elif choice == '7':
            print("[INFO] Recent Files coming soon...")
        elif choice == '8':
            print("[INFO] PowerShell History coming soon...")
        elif choice == '9':
            print("[INFO] Browser Cache coming soon...")
        elif choice == '10':
            print("[INFO] Windows Logs coming soon...")
        elif choice == '11':
            print("[INFO] Disk Cleanup coming soon...")
        elif choice == '12':
            print("[INFO] Optimize Drives coming soon...")
        elif choice == '13':
            print("[INFO] Winget Upgrade coming soon...")
        elif choice == '14':
            print("[INFO] Winget Repair coming soon...")
        elif choice == '15':
            print("[INFO] App Repair coming soon...")
        else:
            print("[ERROR] Invalid choice.")
