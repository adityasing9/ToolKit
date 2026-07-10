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
        print("[INFO] No commands found in the database.")
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
        print(f"[INFO] No commands found matching '{query}'.")
        return

    print(f"\n{'ID':<4} | {'Name':<25} | {'Category':<15} | {'Risk':<6} | {'Command':<20} | Purpose")
    print("-" * 100)
    for row in rows:
        print(f"{row['id']:<4} | {row['name'][:25]:<25} | {row['category'][:15]:<15} | {row['risk_level']:<6} | {row['command'][:20]:<20} | {row['purpose']}")
    print("-" * 100)

def execute_command():
    cmd_id = input("Enter the ID of the command to execute: ").strip()
    if not cmd_id.isdigit():
        print("[ERROR] Please enter a valid numeric ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, command, risk_level FROM commands WHERE id = ?", (cmd_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"[ERROR] No command found with ID {cmd_id}.")
        return

    print(f"\n[INFO] You are about to execute: {row['name']} ({row['command']})")
    if row['risk_level'].lower() == 'high':
        print("[WARNING] This is a HIGH RISK command!")
    
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        print(f"[INFO] Executing '{row['command']}'...")
        try:
            # We use subprocess.Popen with shell=True for windows commands
            subprocess.Popen(row['command'], shell=True)
            print("[SUCCESS] Command launched successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to execute command: {e}")
    else:
        print("[INFO] Execution cancelled.")

def add_command():
    print("\n--- Add New Command ---")
    name = input("Name: ").strip()
    command = input("Command: ").strip()
    description = input("Description: ").strip()
    category = input("Category: ").strip()
    risk_level = input("Risk Level (Low/Medium/High): ").strip()
    purpose = input("Purpose: ").strip()

    if not name or not command:
        print("[ERROR] Name and Command are required fields.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO commands (name, command, description, category, risk_level, purpose) VALUES (?, ?, ?, ?, ?, ?)",
        (name, command, description, category, risk_level, purpose)
    )
    conn.commit()
    conn.close()
    print(f"[SUCCESS] Command '{name}' added successfully.")

def delete_command():
    cmd_id = input("Enter the ID of the command to delete: ").strip()
    if not cmd_id.isdigit():
        print("[ERROR] Please enter a valid numeric ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM commands WHERE id = ?", (cmd_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"[ERROR] No command found with ID {cmd_id}.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete '{row['name']}'? (y/n): ").strip().lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM commands WHERE id = ?", (cmd_id,))
        conn.commit()
        print(f"[SUCCESS] Command '{row['name']}' deleted.")
    else:
        print("[INFO] Deletion cancelled.")
    conn.close()

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [13] RUN COMMANDS")
        print("=============================================================")
        print("[1] List Commands")
        print("[2] Search Command")
        print("[3] Execute Command")
        print("[4] Add Command")
        print("[5] Delete Command")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[ERROR] Invalid choice.")
