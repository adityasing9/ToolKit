from toolkit.utils import Colors
import sqlite3
import subprocess
from toolkit.db import get_connection

def list_commands():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, command, category, risk_level, purpose FROM commands ORDER BY category, name")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No commands found in the database.")
        return

    print(f"\n{'ID':<4} | {'Name':<25} | {'Category':<15} | {'Risk':<6} | {'Command':<20} | Purpose")
    print("-" * 100)
    for row in rows:
        print(f"{row['id']:<4} | {row['name'][:25]:<25} | {row['category'][:15]:<15} | {row['risk_level']:<6} | {row['command'][:20]:<20} | {row['purpose']}")
    print("-" * 100)

def search_command():
    query = input("Enter search term (name, command, or category): ").strip().lower()
    if not query:
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, command, category, risk_level, purpose 
        FROM commands 
        WHERE LOWER(name) LIKE ? OR LOWER(command) LIKE ? OR LOWER(category) LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No commands found matching '{query}'.")
        return

    print(f"\n{'ID':<4} | {'Name':<25} | {'Category':<15} | {'Risk':<6} | {'Command':<20} | Purpose")
    print("-" * 100)
    for row in rows:
        print(f"{row['id']:<4} | {row['name'][:25]:<25} | {row['category'][:15]:<15} | {row['risk_level']:<6} | {row['command'][:20]:<20} | {row['purpose']}")
    print("-" * 100)

def execute_command():
    cmd_id = input("Enter the ID of the command to execute: ").strip()
    if not cmd_id.isdigit():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Please enter a valid numeric ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, command, risk_level FROM commands WHERE id = ?", (cmd_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} No command found with ID {cmd_id}.")
        return

    print(f"\n[INFO] You are about to execute: {row['name']} ({row['command']})")
    if row['risk_level'].lower() == 'high':
        print("[WARNING] This is a HIGH RISK command!")
    
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Executing '{row['command']}'...")
        try:
            # We use subprocess.Popen with shell=True for windows commands
            subprocess.Popen(row['command'], shell=True)
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Command launched successfully.")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to execute command: {e}")
    else:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Execution cancelled.")

def add_command():
    print(f"\n{Colors.CYAN}--- Add New Command ---{Colors.RESET}")
    name = input("Name: ").strip()
    command = input("Command: ").strip()
    description = input("Description: ").strip()
    category = input("Category: ").strip()
    risk_level = input("Risk Level (Low/Medium/High): ").strip()
    purpose = input("Purpose: ").strip()

    if not name or not command:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Name and Command are required fields.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO commands (name, command, description, category, risk_level, purpose) VALUES (?, ?, ?, ?, ?, ?)",
        (name, command, description, category, risk_level, purpose)
    )
    conn.commit()
    conn.close()
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Command '{name}' added successfully.")

def delete_command():
    cmd_id = input("Enter the ID of the command to delete: ").strip()
    if not cmd_id.isdigit():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Please enter a valid numeric ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM commands WHERE id = ?", (cmd_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} No command found with ID {cmd_id}.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete '{row['name']}'? (y/n): ").strip().lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM commands WHERE id = ?", (cmd_id,))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Command '{row['name']}' deleted.")
    else:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Deletion cancelled.")
    conn.close()

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [10] RUN COMMANDS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} List Commands")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Search Command")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Execute Command")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Add Command")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Delete Command")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            list_commands()
        elif choice == '2':
            search_command()
        elif choice == '3':
            execute_command()
        elif choice == '4':
            add_command()
        elif choice == '5':
            delete_command()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
