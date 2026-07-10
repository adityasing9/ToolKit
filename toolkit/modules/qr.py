def show_menu():
    while True:
        print("\n=============================================================")
        print("              [10] QR / BARCODE")
        print("=============================================================")
        print("[1] Generate QR")
        print("[2] Generate Barcode")
        print("[3] QR from Text")
        print("[4] QR from URL")
        print("[5] WiFi QR")
        print("[6] Email QR")
        print("[7] Phone QR")
        print("[8] Scan QR")
        print("[9] Save PNG")
        print("[10] SVG Export")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Generate QR coming soon...")
        elif choice == '2':
            print("[INFO] Generate Barcode coming soon...")
        elif choice == '3':
            print("[INFO] QR from Text coming soon...")
        elif choice == '4':
            print("[INFO] QR from URL coming soon...")
        elif choice == '5':
            print("[INFO] WiFi QR coming soon...")
        elif choice == '6':
            print("[INFO] Email QR coming soon...")
        elif choice == '7':
            print("[INFO] Phone QR coming soon...")
        elif choice == '8':
            print("[INFO] Scan QR coming soon...")
        elif choice == '9':
            print("[INFO] Save PNG coming soon...")
        elif choice == '10':
            print("[INFO] SVG Export coming soon...")
        else:
            print("[ERROR] Invalid choice.")
