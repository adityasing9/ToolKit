def show_menu():
    while True:
        print("\n=============================================================")
        print("              [9] PRODUCTIVITY")
        print("=============================================================")
        print("[1] To-do")
        print("[2] Reminder")
        print("[3] Calendar")
        print("[4] Pomodoro")
        print("[5] Timer")
        print("[6] Stopwatch")
        print("[7] Expense Notes")
        print("[8] Clipboard")
        print("[9] Password Generator")
        print("[10] UUID Generator")
        print("[11] Lorem Ipsum")
        print("[12] Random Data")
        print("[13] Base64")
        print("[14] JSON Formatter")
        print("[15] Markdown Preview")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] To-do coming soon...")
        elif choice == '2':
            print("[INFO] Reminder coming soon...")
        elif choice == '3':
            print("[INFO] Calendar coming soon...")
        elif choice == '4':
            print("[INFO] Pomodoro coming soon...")
        elif choice == '5':
            print("[INFO] Timer coming soon...")
        elif choice == '6':
            print("[INFO] Stopwatch coming soon...")
        elif choice == '7':
            print("[INFO] Expense Notes coming soon...")
        elif choice == '8':
            print("[INFO] Clipboard coming soon...")
        elif choice == '9':
            print("[INFO] Password Generator coming soon...")
        elif choice == '10':
            print("[INFO] UUID Generator coming soon...")
        elif choice == '11':
            print("[INFO] Lorem Ipsum coming soon...")
        elif choice == '12':
            print("[INFO] Random Data coming soon...")
        elif choice == '13':
            print("[INFO] Base64 coming soon...")
        elif choice == '14':
            print("[INFO] JSON Formatter coming soon...")
        elif choice == '15':
            print("[INFO] Markdown Preview coming soon...")
        else:
            print("[ERROR] Invalid choice.")
