def mock_ai_response(prompt_type):
    print(f"\n[INFO] AI Assistant ({prompt_type}) requires an active API key.")
    print("Please configure your API key in the Settings or Cloud Workspace modules.")
    print("Feature coming in v2.0.")

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
        print("[13] OCR (Image to Text)")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            mock_ai_response("General Query")
        elif choice == '2':
            mock_ai_response("Explain Error")
        elif choice == '3':
            mock_ai_response("Explain Command")
        elif choice == '4':
            mock_ai_response("Generate Regex")
        elif choice == '5':
            mock_ai_response("Generate SQL")
        elif choice == '6':
            mock_ai_response("Generate Bash")
        elif choice == '7':
            mock_ai_response("Generate PowerShell")
        elif choice == '8':
            mock_ai_response("Generate Python")
        elif choice == '9':
            mock_ai_response("Summarize Logs")
        elif choice == '10':
            mock_ai_response("Fix Error")
        elif choice == '11':
            mock_ai_response("Search Docs")
        elif choice == '12':
            mock_ai_response("Translate")
        elif choice == '13':
            mock_ai_response("OCR")
        else:
            print("[ERROR] Invalid choice.")
