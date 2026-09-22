from toolkit.utils import Colors
from toolkit.db import get_connection
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
    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Generated Password: {Colors.YELLOW}{pwd}{Colors.RESET}")
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} You can copy this to your clipboard.")

def generate_uuid():
    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Generated UUID (v4): {Colors.YELLOW}{uuid.uuid4()}{Colors.RESET}")

def show_calendar():
    year = input("Enter year (default current): ").strip()
    month = input("Enter month (1-12, default current): ").strip()
    now = datetime.now()
    year = int(year) if year.isdigit() else now.year
    month = int(month) if month.isdigit() and 1 <= int(month) <= 12 else now.month
    print(f"\n{Colors.CYAN}{calendar.month(year, month)}{Colors.RESET}")

def run_stopwatch():
    print(f"\n{Colors.CYAN}--- Stopwatch ---{Colors.RESET}")
    print("Press Enter to start, and Ctrl+C to stop.")
    input()
    print("Stopwatch started... (Ctrl+C to stop)")
    start_time = time.time()
    try:
        while True:
            elapsed = time.time() - start_time
            mins, secs = divmod(int(elapsed), 60)
            ms = int((elapsed - int(elapsed)) * 100)
            print(f"\rElapsed Time: {Colors.GREEN}{mins:02d}:{secs:02d}.{ms:02d}{Colors.RESET}", end="", flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Stopwatch stopped. Total time: {mins:02d}m {secs:02d}s")

def run_timer():
    seconds = input("Enter seconds to count down: ").strip()
    if not seconds.isdigit():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid number of seconds.")
        return
    total = int(seconds)
    print(f"Starting countdown for {total} seconds... (Ctrl+C to cancel)")
    try:
        for remaining in range(total, -1, -1):
            mins, secs = divmod(remaining, 60)
            percent = int(((total - remaining) / max(total, 1)) * 30)
            bar = "█" * percent + "░" * (30 - percent)
            print(f"\rTime Remaining: [{Colors.CYAN}{bar}{Colors.RESET}] {Colors.YELLOW}{mins:02d}:{secs:02d}{Colors.RESET}", end="", flush=True)
            if remaining > 0:
                time.sleep(1)
        print(f"\n\a{Colors.GREEN}[SUCCESS]{Colors.RESET} Timer finished! ⏰")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Timer cancelled.")

def run_pomodoro():
    print(f"\n{Colors.CYAN}--- Pomodoro Focus Timer ---{Colors.RESET}")
    print(f"{Colors.GREEN}[1]{Colors.RESET} Standard 25 min Focus + 5 min Break")
    print(f"{Colors.GREEN}[2]{Colors.RESET} Custom Focus Duration")
    p_choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    
    if p_choice == '2':
        work_mins = input("Focus minutes (default 25): ").strip()
        work_mins = int(work_mins) if work_mins.isdigit() else 25
        break_mins = input("Break minutes (default 5): ").strip()
        break_mins = int(break_mins) if break_mins.isdigit() else 5
    else:
        work_mins, break_mins = 25, 5

    def countdown_block(minutes, label, color):
        total_sec = minutes * 60
        print(f"\n{color}=== {label} ({minutes} mins) ==={Colors.RESET}")
        try:
            for s in range(total_sec, -1, -1):
                m, sec = divmod(s, 60)
                pct = int(((total_sec - s) / max(total_sec, 1)) * 30)
                bar = "█" * pct + "-" * (30 - pct)
                print(f"\r[{color}{bar}{Colors.RESET}] {m:02d}:{sec:02d} remaining", end="", flush=True)
                if s > 0:
                    time.sleep(1)
            print(f"\n\a{Colors.GREEN}[DONE]{Colors.RESET} {label} finished!")
            return True
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[ABORTED]{Colors.RESET} Session interrupted.")
            return False

    if countdown_block(work_mins, "FOCUS SESSION", Colors.RED):
        input(f"\n{Colors.YELLOW}Press Enter to start your {break_mins}-minute break...{Colors.RESET}")
        countdown_block(break_mins, "SHORT BREAK", Colors.GREEN)

def manage_reminders():
    print(f"\n{Colors.CYAN}--- Quick Reminder Alarm ---{Colors.RESET}")
    mins = input("Remind me in how many minutes? (e.g. 15): ").strip()
    if not mins.isdigit() or int(mins) <= 0:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Please enter a valid number of minutes.")
        return
    message = input("Reminder message / note: ").strip()
    if not message:
        message = "Time's up! Check your tasks."
    
    total_seconds = int(mins) * 60
    print(f"{Colors.GREEN}[INFO]{Colors.RESET} Reminder set for {mins} minutes from now. (Background countdown running...)")
    try:
        time.sleep(total_seconds)
        print(f"\n\a{Colors.BOLD}{Colors.YELLOW}🔔 REMINDER ALERT:{Colors.RESET} {message}")
        try:
            # Show a Windows notification box
            ps_cmd = f'Add-Type -AssemblyName PresentationCore,PresentationFramework; [System.Windows.MessageBox]::Show("{message}", "Toolkit Reminder")'
            subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd])
        except Exception:
            pass
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Reminder cancelled.")

def manage_todos():
    while True:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, priority, status, created_at FROM todos ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        print(f"\n{Colors.CYAN}--- To-Do Task Manager ---{Colors.RESET}")
        if not rows:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No tasks found. Your to-do list is empty!")
        else:
            print(f"{'ID':<4} | {'Status':<12} | {'Priority':<8} | {'Task':<35} | Created")
            print("-" * 75)
            for r in rows:
                status_str = f"{Colors.GREEN}[✓] Done{Colors.RESET}" if r['status'] == 'Completed' else f"{Colors.YELLOW}[ ] Pending{Colors.RESET}"
                p_color = Colors.RED if r['priority'] == 'High' else (Colors.YELLOW if r['priority'] == 'Medium' else Colors.CYAN)
                p_str = f"{p_color}{r['priority']:<8}{Colors.RESET}"
                task_text = r['task'][:35]
                print(f"{r['id']:<4} | {status_str:<21} | {p_str} | {task_text:<35} | {r['created_at'][:10]}")

        print(f"\n{Colors.GREEN}[1]{Colors.RESET} Add Task  {Colors.GREEN}[2]{Colors.RESET} Toggle Done  {Colors.GREEN}[3]{Colors.RESET} Delete Task  {Colors.GREEN}[4]{Colors.RESET} Clear Completed  {Colors.GREEN}[0]{Colors.RESET} Back")
        sub_choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        
        if sub_choice == '0':
            break
        elif sub_choice == '1':
            task = input("Enter task description: ").strip()
            if not task:
                continue
            priority = input("Priority (High / Medium / Low, default Medium): ").strip().capitalize()
            if priority not in ['High', 'Medium', 'Low']:
                priority = 'Medium'
            conn = get_connection()
            conn.cursor().execute("INSERT INTO todos (task, priority) VALUES (?, ?)", (task, priority))
            conn.commit()
            conn.close()
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Task added.")
        elif sub_choice == '2':
            tid = input("Enter Task ID to toggle status: ").strip()
            if tid.isdigit():
                conn = get_connection()
                c = conn.cursor()
                c.execute("SELECT status FROM todos WHERE id = ?", (int(tid),))
                row = c.fetchone()
                if row:
                    new_status = 'Pending' if row['status'] == 'Completed' else 'Completed'
                    c.execute("UPDATE todos SET status = ? WHERE id = ?", (new_status, int(tid)))
                    conn.commit()
                    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Task marked as {new_status}.")
                else:
                    print(f"{Colors.RED}[ERROR]{Colors.RESET} Task not found.")
                conn.close()
        elif sub_choice == '3':
            tid = input("Enter Task ID to delete: ").strip()
            if tid.isdigit():
                conn = get_connection()
                conn.cursor().execute("DELETE FROM todos WHERE id = ?", (int(tid),))
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Task deleted.")
        elif sub_choice == '4':
            conn = get_connection()
            conn.cursor().execute("DELETE FROM todos WHERE status = 'Completed'")
            conn.commit()
            conn.close()
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Completed tasks cleared.")

def manage_expenses():
    while True:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, amount, category, created_at FROM expenses ORDER BY id DESC")
        rows = cursor.fetchall()
        cursor.execute("SELECT category, SUM(amount) as total FROM expenses GROUP BY category")
        cat_totals = cursor.fetchall()
        cursor.execute("SELECT SUM(amount) FROM expenses")
        grand_total = cursor.fetchone()[0] or 0.0
        conn.close()

        print(f"\n{Colors.CYAN}--- Expense Tracker & Notes ---{Colors.RESET}")
        print(f"Total Logged Spending: {Colors.GREEN}${grand_total:.2f}{Colors.RESET}")
        if cat_totals:
            breakdown = " | ".join([f"{c['category']}: ${c['total']:.2f}" for c in cat_totals])
            print(f"Breakdown: {Colors.CYAN}{breakdown}{Colors.RESET}")

        if not rows:
            print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} No expenses logged yet.")
        else:
            print(f"\n{'ID':<4} | {'Amount':<10} | {'Category':<15} | {'Title':<25} | Date")
            print("-" * 65)
            for r in rows[:15]:
                print(f"{r['id']:<4} | ${r['amount']:<9.2f} | {r['category']:<15} | {r['title'][:25]:<25} | {r['created_at'][:10]}")

        print(f"\n{Colors.GREEN}[1]{Colors.RESET} Add Expense  {Colors.GREEN}[2]{Colors.RESET} Delete Expense  {Colors.GREEN}[3]{Colors.RESET} Clear All  {Colors.GREEN}[0]{Colors.RESET} Back")
        sub = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if sub == '0':
            break
        elif sub == '1':
            title = input("Expense title / description: ").strip()
            amount_str = input("Amount (e.g. 24.50): ").strip()
            category = input("Category (Food, Transport, Bills, Tech, General): ").strip().capitalize()
            if not category:
                category = "General"
            try:
                amt = float(amount_str)
                conn = get_connection()
                conn.cursor().execute("INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)", (title, amt, category))
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Expense logged.")
            except ValueError:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid amount number.")
        elif sub == '2':
            eid = input("Enter Expense ID to delete: ").strip()
            if eid.isdigit():
                conn = get_connection()
                conn.cursor().execute("DELETE FROM expenses WHERE id = ?", (int(eid),))
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Expense deleted.")
        elif sub == '3':
            confirm = input("Clear all expense records? (y/n): ").strip().lower()
            if confirm == 'y':
                conn = get_connection()
                conn.cursor().execute("DELETE FROM expenses")
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} All expenses cleared.")

def generate_random_data():
    print(f"\n{Colors.CYAN}--- Mock Data Generator ---{Colors.RESET}")
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Casey", "Riley", "Avery", "Jamie"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Anderson", "Taylor"]
    domains = ["gmail.com", "outlook.com", "yahoo.com", "proton.me", "example.com"]
    cities = ["New York", "San Francisco", "Austin", "Seattle", "London", "Tokyo", "Berlin", "Toronto", "Sydney"]

    count = input("How many mock records to generate (1-20, default 5): ").strip()
    count = int(count) if count.isdigit() and 1 <= int(count) <= 20 else 5

    records = []
    for _ in range(count):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        record = {
            "id": str(uuid.uuid4())[:8],
            "name": f"{fn} {ln}",
            "email": f"{fn.lower()}.{ln.lower()}{random.randint(10,99)}@{random.choice(domains)}",
            "phone": f"+1 ({random.randint(200,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}",
            "city": random.choice(cities),
            "ip_address": f"{random.randint(11,210)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        }
        records.append(record)

    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Generated {count} Mock Records (JSON Format):")
    print(f"{Colors.CYAN}{json.dumps(records, indent=2)}{Colors.RESET}")

def preview_markdown():
    print(f"\n{Colors.CYAN}--- Terminal Markdown Previewer ---{Colors.RESET}")
    filepath = input("Enter path to markdown file (or press Enter to view README.md): ").strip()
    if not filepath:
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "README.md")
    
    if not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File not found: {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not read file: {e}")
        return

    print(f"\n{Colors.CYAN}=== Previewing: {os.path.basename(filepath)} ==={Colors.RESET}\n")
    in_code_block = False
    for line in lines[:80]:  # Show first 80 lines
        line_clean = line.rstrip()
        if line_clean.startswith("```"):
            in_code_block = not in_code_block
            print(f"{Colors.YELLOW}{line_clean}{Colors.RESET}")
            continue
        if in_code_block:
            print(f"{Colors.GREEN}    {line_clean}{Colors.RESET}")
            continue
        if line_clean.startswith("# "):
            print(f"\n{Colors.BOLD}{Colors.CYAN}{line_clean.upper()}{Colors.RESET}")
            print(f"{Colors.CYAN}{'=' * len(line_clean)}{Colors.RESET}")
        elif line_clean.startswith("## "):
            print(f"\n{Colors.BOLD}{Colors.YELLOW}{line_clean}{Colors.RESET}")
            print(f"{Colors.YELLOW}{'-' * len(line_clean)}{Colors.RESET}")
        elif line_clean.startswith("### "):
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}{line_clean}{Colors.RESET}")
        elif line_clean.startswith("- ") or line_clean.startswith("* "):
            print(f"  {Colors.CYAN}•{Colors.RESET} {line_clean[2:]}")
        elif line_clean.startswith("> "):
            print(f"  {Colors.BLUE}│ {line_clean[2:]}{Colors.RESET}")
        else:
            print(line_clean)
    if len(lines) > 80:
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Display truncated. ({len(lines) - 80} more lines in file)")

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
    print("Paste your JSON below. Press Enter on a blank line to finish:")
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
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Formatted JSON:")
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
        print(f"{Colors.BOLD}{Colors.YELLOW}              [15] PRODUCTIVITY{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} To-do List (Task Manager)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Reminders & Alarms")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Calendar")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Pomodoro Focus Timer")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Timer (Countdown)")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Stopwatch")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Expense Tracker")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Clipboard Viewer")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Password Generator")
        print(f"{Colors.GREEN}[10]{Colors.RESET} UUID Generator")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Lorem Ipsum Generator")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Mock Data Generator (JSON)")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Base64 Encoder/Decoder")
        print(f"{Colors.GREEN}[14]{Colors.RESET} JSON Formatter")
        print(f"{Colors.GREEN}[15]{Colors.RESET} Markdown Terminal Previewer")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            manage_todos()
        elif choice == '2':
            manage_reminders()
        elif choice == '3':
            show_calendar()
        elif choice == '4':
            run_pomodoro()
        elif choice == '5':
            run_timer()
        elif choice == '6':
            run_stopwatch()
        elif choice == '7':
            manage_expenses()
        elif choice == '8':
            read_clipboard()
        elif choice == '9':
            generate_password()
        elif choice == '10':
            generate_uuid()
        elif choice == '11':
            generate_lorem()
        elif choice == '12':
            generate_random_data()
        elif choice == '13':
            base64_tool()
        elif choice == '14':
            json_formatter()
        elif choice == '15':
            preview_markdown()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
