from toolkit.utils import Colors
import urllib.request
import json
import base64
import os
import mimetypes
from toolkit.db import get_setting

def call_gemini(prompt, system_instruction=None, image_data=None, mime_type=None):
    api_key = get_setting("gemini_api_key")
    if not api_key:
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Gemini API Key is not set.")
        print("Please configure your API Key in [16] Settings -> [16] Configure API / Cloud Keys.")
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    parts = []
    if image_data and mime_type:
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": image_data
            }
        })
    parts.append({"text": prompt})
    
    contents = {
        "contents": [{
            "parts": parts
        }]
    }
    
    if system_instruction:
        contents["systemInstruction"] = {
            "parts": [{
                "text": system_instruction
            }]
        }
        
    data = json.dumps(contents).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Contacting Gemini AI...")
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            # Safely navigate the JSON response
            candidates = res_data.get('candidates', [])
            if candidates:
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if parts:
                    return parts[0].get('text', '')
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid response structure from API.")
            return None
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Gemini API call failed: {e}")
        return None

def handle_prompt(title, system_instruction, user_prompt_label="Enter prompt: "):
    print(f"\n{Colors.CYAN}--- {title} ---{Colors.RESET}")
    user_input = input(user_prompt_label).strip()
    if not user_input:
        return
    response = call_gemini(user_input, system_instruction)
    if response:
        print(f"\n{Colors.GREEN}--- AI Response ---{Colors.RESET}")
        print(response)
        print(f"{Colors.CYAN}-------------------{Colors.RESET}")

def handle_ocr():
    print(f"\n{Colors.CYAN}--- OCR (Image to Text) ---{Colors.RESET}")
    img_path = input("Enter absolute path to image: ").strip().replace('"', '')
    if not img_path or not os.path.exists(img_path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Image path does not exist.")
        return
        
    mime_type, _ = mimetypes.guess_type(img_path)
    if not mime_type or not mime_type.startswith("image/"):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File is not a valid image.")
        return
        
    try:
        with open(img_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to read image: {e}")
        return

    response = call_gemini(
        prompt="Perform OCR on this image. Extract all text, maintaining layout if possible.",
        image_data=encoded_img,
        mime_type=mime_type
    )
    if response:
        print(f"\n{Colors.GREEN}--- Extracted Text ---{Colors.RESET}")
        print(response)
        print(f"{Colors.CYAN}----------------------{Colors.RESET}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [15] AI ASSISTANT{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Ask AI (General)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Explain Error")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Explain Command")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Generate Regex")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Generate SQL")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Generate Bash")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Generate PowerShell")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Generate Python")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Summarize Logs")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Fix Error")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Search Docs Helper")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Translate Text")
        print(f"{Colors.GREEN}[13]{Colors.RESET} OCR (Image to Text)")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            handle_prompt("Ask AI", "You are a helpful terminal programming assistant. Keep answers brief and optimized for command line users.")
        elif choice == '2':
            handle_prompt("Explain Error", "Explain this stacktrace/error output clearly and suggest a quick solution.", "Paste error: ")
        elif choice == '3':
            handle_prompt("Explain Command", "Explain this terminal/shell command in detail.", "Enter command: ")
        elif choice == '4':
            handle_prompt("Generate Regex", "Generate a regular expression matching the user's description. Include brief explanations.", "Describe target text pattern: ")
        elif choice == '5':
            handle_prompt("Generate SQL", "Generate optimized SQL based on the database schema description.", "Describe query goal: ")
        elif choice == '6':
            handle_prompt("Generate Bash", "Generate a clean Bash shell script for the task. Output code directly.", "Describe task: ")
        elif choice == '7':
            handle_prompt("Generate PowerShell", "Generate a clean PowerShell script for the task. Output code directly.", "Describe task: ")
        elif choice == '8':
            handle_prompt("Generate Python", "Generate a clean Python script/snippet for the task. Output code directly.", "Describe task: ")
        elif choice == '9':
            handle_prompt("Summarize Logs", "Summarize these log messages, highlighting errors, warnings, or key statistics.", "Paste logs here: ")
        elif choice == '10':
            handle_prompt("Fix Error", "Suggest code adjustments to fix this specific bug or compilation error.", "Paste code and error details: ")
        elif choice == '11':
            handle_prompt("Search Docs Helper", "Help the user search documentation or structure queries for technical documentation.", "Enter search objective: ")
        elif choice == '12':
            handle_prompt("Translate Text", "Translate the user's text to the requested target language. Output translation directly.", "Enter text and target language (e.g., 'Hello to Spanish'): ")
        elif choice == '13':
            handle_ocr()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
