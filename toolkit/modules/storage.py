from toolkit.utils import Colors
import os
import subprocess
from toolkit.db import get_connection

def manage_links():
    print(f"\n{Colors.CYAN}--- Links Management ---{Colors.RESET}")
    print("1. Add Link")
    print("2. List Links")
    print("3. Delete Link")
    choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == '1':
        title = input("Title: ").strip()
        url = input("URL: ").strip()
        tags = input("Tags (comma separated): ").strip()
        cursor.execute("INSERT INTO links (title, url, tags) VALUES (?, ?, ?)", (title, url, tags))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Link added.")
    elif choice == '2':
        cursor.execute("SELECT id, title, url, tags FROM links")
        rows = cursor.fetchall()
        if not rows:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No links found.")
        else:
            print(f"\n{Colors.CYAN}--- Saved Links ---{Colors.RESET}")
            for r in rows:
                print(f"[{Colors.GREEN}ID: {r['id']}{Colors.RESET}] {Colors.BOLD}{r['title']}{Colors.RESET}")
                print(f"      {Colors.BLUE}URL:{Colors.RESET}  {r['url']}")
                print(f"      {Colors.BLUE}Tags:{Colors.RESET} {r['tags']}")
                print(f"{Colors.CYAN}-{Colors.RESET}" * 40)
    elif choice == '3':
        link_id = input("Enter ID to delete: ").strip()
        cursor.execute("DELETE FROM links WHERE id = ?", (link_id,))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Link deleted.")
    conn.close()

def manage_github():
    print(f"\n{Colors.CYAN}--- Github Repositories ---{Colors.RESET}")
    print("1. Save Repo")
    print("2. List Repos")
    print("3. Clone Repo")
    choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == '1':
        name = input("Repo Name: ").strip()
        url = input("URL: ").strip()
        desc = input("Description: ").strip()
        cursor.execute("INSERT INTO github_repos (name, url, description) VALUES (?, ?, ?)", (name, url, desc))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Repo saved.")
    elif choice == '2':
        cursor.execute("SELECT id, name, url, description FROM github_repos")
        rows = cursor.fetchall()
        if not rows:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No repos found.")
        else:
            print(f"\n{Colors.CYAN}--- Saved Repositories ---{Colors.RESET}")
            for r in rows:
                print(f"[{Colors.GREEN}ID: {r['id']}{Colors.RESET}] {Colors.BOLD}{r['name']}{Colors.RESET}")
                print(f"      {Colors.BLUE}URL:{Colors.RESET}  {r['url']}")
                print(f"      {Colors.BLUE}Desc:{Colors.RESET} {r['description']}")
                print(f"{Colors.CYAN}-{Colors.RESET}" * 40)
    elif choice == '3':
        repo_id = input("Enter ID to clone: ").strip()
        cursor.execute("SELECT url FROM github_repos WHERE id = ?", (repo_id,))
        row = cursor.fetchone()
        if row:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cloning {row['url']}...")
            subprocess.run(["git", "clone", row['url']])
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Repo not found.")
    conn.close()

def manage_snippets():
    print(f"\n{Colors.CYAN}--- Code Snippets ---{Colors.RESET}")
    print("1. Add Snippet")
    print("2. View Snippet")
    print("3. Delete Snippet")
    choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == '1':
        title = input("Title: ").strip()
        lang = input("Language (e.g. python, bash): ").strip()
        print("Enter code (end with an empty line):")
        code_lines = []
        while True:
            line = input()
            if not line: break
            code_lines.append(line)
        cursor.execute("INSERT INTO snippets (title, language, code) VALUES (?, ?, ?)", (title, lang, "\n".join(code_lines)))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Snippet saved.")
    elif choice == '2':
        cursor.execute("SELECT id, title, language FROM snippets")
        rows = cursor.fetchall()
        if not rows:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No snippets found.")
        else:
            print(f"\n{Colors.CYAN}--- Saved Snippets ---{Colors.RESET}")
            for r in rows:
                print(f"[{Colors.GREEN}ID: {r['id']}{Colors.RESET}] {Colors.BOLD}{r['title']}{Colors.RESET} ({r['language']})")
            snip_id = input("\nEnter ID to view code (or press enter to cancel): ").strip()
            if snip_id:
                cursor.execute("SELECT code FROM snippets WHERE id = ?", (snip_id,))
                row = cursor.fetchone()
                if row:
                    print(f"\n{Colors.CYAN}--- CODE ---{Colors.RESET}")
                    print(row['code'])
                    print("------------")
    elif choice == '3':
        snip_id = input("Enter ID to delete: ").strip()
        cursor.execute("DELETE FROM snippets WHERE id = ?", (snip_id,))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Snippet deleted.")
    conn.close()

def manage_notes():
    print(f"\n{Colors.CYAN}--- Quick Notes ---{Colors.RESET}")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Delete Note")
    choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == '1':
        title = input("Title: ").strip()
        print("Enter content (end with an empty line):")
        lines = []
        while True:
            line = input()
            if not line: break
            lines.append(line)
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, "\n".join(lines)))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Note saved.")
    elif choice == '2':
        cursor.execute("SELECT id, title, created_at FROM notes")
        rows = cursor.fetchall()
        if not rows:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No notes found.")
        else:
            print(f"\n{Colors.CYAN}--- Saved Notes ---{Colors.RESET}")
            for r in rows:
                print(f"[{Colors.GREEN}ID: {r['id']}{Colors.RESET}] {Colors.BOLD}{r['title']}{Colors.RESET} (Created: {r['created_at']})")
            note_id = input("\nEnter ID to view content (or press enter to cancel): ").strip()
            if note_id:
                cursor.execute("SELECT content FROM notes WHERE id = ?", (note_id,))
                row = cursor.fetchone()
                if row:
                    print(f"\n{Colors.CYAN}--- CONTENT ---{Colors.RESET}")
                    print(row['content'])
                    print("---------------")
    elif choice == '3':
        note_id = input("Enter ID to delete: ").strip()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Note deleted.")
    conn.close()

def export_db():
    print("\n[INFO] Creating database backup...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "toolkit.db")
    backup_path = db_path + ".backup"
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Database exported to: {backup_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Export failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [13] STORAGE & NOTES{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Links")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Github")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Commands")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Snippets")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Clipboard History")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Quick Notes")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Bookmarks")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Favorites")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Tags")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Import / Export")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            manage_links()
        elif choice == '2':
            manage_github()
        elif choice == '3':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use the main [13] Run Commands module for this.")
        elif choice == '4':
            manage_snippets()
        elif choice == '5':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please use the [9] Productivity module for Clipboard operations.")
        elif choice == '6':
            manage_notes()
        elif choice == '7' or choice == '8' or choice == '9':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Use Links and Notes to manage Bookmarks/Favorites/Tags.")
        elif choice == '10':
            export_db()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
