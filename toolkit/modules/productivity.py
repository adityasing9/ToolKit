from toolkit.utils import Colors
import os
import sys
import time
import uuid
import json
import base64
import random
import string
import calendar
import subprocess
from datetime import datetime

def generate_password():
    length = input("Enter password length (default 16): ").strip()
    length = int(length) if length.isdigit() else 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    pwd = "".join(random.choice(chars) for _ in range(length))
    print(f"\n[SUCCESS] Generated Password: {pwd}")
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} You can copy this to your clipboard.")

def generate_uuid():
    print(f"\n[SUCCESS] Generated UUID (v4): {uuid.uuid4()}")

def show_calendar():
    year = input("Enter year (default current): ").strip()
    month = input("Enter month (1-12, default current): ").strip()
    now = datetime.now()
    year = int(year) if year.isdigit() else now.year
    month = int(month) if month.isdigit() and 1 <= int(month) <= 12 else now.month
    print(f"\n{calendar.month(year, month)}")

def run_stopwatch():
    print(f"\n{Colors.CYAN}--- Stopwatch ---{Colors.RESET}")
    print("Press Enter to start, and Ctrl+C to stop.")
    input()
    print("Stopwatch started...")
    start_time = time.time()
    try:
        while True:
            elapsed = time.time() - start_time
            print(f"\rElapsed Time: {elapsed:.2f} seconds", end="")
            time.sleep(0.1)
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\n[INFO] Stopwatch stopped. Total time: {elapsed:.2f} seconds")

def run_timer():
    seconds = input("Enter seconds to count down: ").strip()
    if not seconds.isdigit():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid number of seconds.")
        return
    seconds = int(seconds)
    print(f"Starting timer for {seconds} seconds...")
    try:
        while seconds > 0:
            print(f"\rTime Remaining: {seconds} seconds", end="")
            time.sleep(1)
            seconds -= 1
        print("\n[SUCCESS] Timer complete! BEEP BEEP BEEP!")
    except KeyboardInterrupt:
        print("\n[INFO] Timer cancelled.")

def base64_tool():
    print(f"\n{Colors.CYAN}--- Base64 Encoder / Decoder ---{Colors.RESET}")
    mode = input("Select mode - (1) Encode or (2) Decode: ").strip()
    data = input("Enter text: ").strip()
    if not data:
        return
    try:
        if mode == '1':
            encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Encoded: {encoded}")
        elif mode == '2':
            decoded = base64.b64decode(data.encode('utf-8')).decode('utf-8')
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Decoded: {decoded}")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid mode.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Base64 operation failed: {e}")

def json_formatter():
    print(f"\n{Colors.CYAN}--- JSON Formatter ---{Colors.RESET}")
    print("Paste your minified JSON below. Press Enter on a blank line to finish:")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    raw_json = "".join(lines)
    if not raw_json:
        return
    try:
        parsed = json.loads(raw_json)
        formatted = json.dumps(parsed, indent=4)
        print("\n[SUCCESS] Formatted JSON:")
        print(formatted)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid JSON: {e}")

def generate_lorem():
    paragraphs = input("Enter number of paragraphs (default 1): ").strip()
    paragraphs = int(paragraphs) if paragraphs.isdigit() else 1
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    print("\n[SUCCESS] Generated Text:")
    for _ in range(paragraphs):
        print(lorem + "\n")

def read_clipboard():
    print(f"\n{Colors.CYAN}--- Clipboard History Viewer ---{Colors.RESET}")
    try:
        output = subprocess.check_output(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], text=True)
        print(f"Current Clipboard Contents:\n{output}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not read clipboard: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [8] PRODUCTIVITY{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} To-do")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Reminder")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Calendar")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Pomodoro")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Timer")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Stopwatch")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Expense Notes")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Clipboard")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Password Generator")
        print(f"{Colors.GREEN}[10]{Colors.RESET} UUID Generator")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Lorem Ipsum")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Random Data")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Base64")
        print(f"{Colors.GREEN}[14]{Colors.RESET} JSON Formatter")
        print(f"{Colors.GREEN}[15]{Colors.RESET} Markdown Preview")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} To-do module coming soon...")
        elif choice == '2':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Reminder module coming soon...")
        elif choice == '3':
            show_calendar()
        elif choice == '4':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Pomodoro timer coming soon...")
        elif choice == '5':
            run_timer()
        elif choice == '6':
            run_stopwatch()
        elif choice == '7':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Expense Notes coming soon...")
        elif choice == '8':
            read_clipboard()
        elif choice == '9':
            generate_password()
        elif choice == '10':
            generate_uuid()
        elif choice == '11':
            generate_lorem()
        elif choice == '12':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Random Data generator coming soon...")
        elif choice == '13':
            base64_tool()
        elif choice == '14':
            json_formatter()
        elif choice == '15':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Markdown Preview coming soon...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
