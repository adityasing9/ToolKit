from toolkit.utils import Colors
def mock_ai_response(prompt_type):
    print(f"\n[INFO] AI Assistant ({prompt_type}) requires an active API key.")
    print("Please configure your API key in the Settings or Cloud Workspace modules.")
    print("Feature coming in v2.0.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [15] AI ASSISTANT{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Ask AI")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Explain Error")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Explain Command")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Generate Regex")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Generate SQL")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Generate Bash")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Generate PowerShell")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Generate Python")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Summarize Logs")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Fix Error")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Search Docs")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Translate")
        print(f"{Colors.GREEN}[13]{Colors.RESET} OCR (Image to Text)")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
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
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
