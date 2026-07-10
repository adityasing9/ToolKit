def show_menu():
    while True:
        print("\n=============================================================")
        print("              [15] AI ASSISTANT")
        print("=============================================================")
        print("[1] Ask AI")
        print("[2] Explain Error")
        print("[3] Explain Command")
        print("[4] Generate Regex")
        print("[5] Generate SQL")
        print("[6] Generate Bash")
        print("[7] Generate PowerShell")
        print("[8] Generate Python")
        print("[9] Summarize Logs")
        print("[10] Fix Error")
        print("[11] Search Docs")
        print("[12] Translate")
        print("[13] OCR")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] Ask AI coming soon...")
        elif choice == '2':
            print("[INFO] Explain Error coming soon...")
        elif choice == '3':
            print("[INFO] Explain Command coming soon...")
        elif choice == '4':
            print("[INFO] Generate Regex coming soon...")
        elif choice == '5':
            print("[INFO] Generate SQL coming soon...")
        elif choice == '6':
            print("[INFO] Generate Bash coming soon...")
        elif choice == '7':
            print("[INFO] Generate PowerShell coming soon...")
        elif choice == '8':
            print("[INFO] Generate Python coming soon...")
        elif choice == '9':
            print("[INFO] Summarize Logs coming soon...")
        elif choice == '10':
            print("[INFO] Fix Error coming soon...")
        elif choice == '11':
            print("[INFO] Search Docs coming soon...")
        elif choice == '12':
            print("[INFO] Translate coming soon...")
        elif choice == '13':
            print("[INFO] OCR coming soon...")
        else:
            print("[ERROR] Invalid choice.")
