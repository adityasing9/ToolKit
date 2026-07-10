import os
import subprocess
from toolkit.db import get_connection

def manage_links():
    print("\n--- Links Management ---")
    print("1. Add Link")
    print("2. List Links")
    print("3. Delete Link")
    choice = input("Select > ").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == '1':
        title = input("Title: ").strip()
        url = input("URL: ").strip()
        tags = input("Tags (comma separated): ").strip()
        cursor.execute("INSERT INTO links (title, url, tags) VALUES (?, ?, ?)", (title, url, tags))
        conn.commit()
        print("[SUCCESS] Link added.")
    elif choice == '2':
        cursor.execute("SELECT id, title, url, tags FROM links")
        rows = cursor.fetchall()
        if not rows:
            print("[INFO] No links found.")
        else:
            print(f"\n{'ID':<4} | {'Title':<20} | {'URL':<40} | Tags")
            print("-" * 80)
            for r in rows:
                print(f"{r['id']:<4} | {r['title'][:20]:<20} | {r['url'][:40]:<40} | {r['tags']}")
    elif choice == '3':
        link_id = input("Enter ID to delete: ").strip()
        cursor.execute("DELETE FROM links WHERE id = ?", (link_id,))
        conn.commit()
        print("[SUCCESS] Link deleted.")
    conn.close()

def manage_github():
    print("\n--- Github Repositories ---")
    print("1. Save Repo")
    print("2. List Repos")
    print("3. Clone Repo")
    choice = input("Select > ").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == '1':
        name = input("Repo Name: ").strip()
        url = input("URL: ").strip()
        desc = input("Description: ").strip()
        cursor.execute("INSERT INTO github_repos (name, url, description) VALUES (?, ?, ?)", (name, url, desc))
        conn.commit()
        print("[SUCCESS] Repo saved.")
    elif choice == '2':
        cursor.execute("SELECT id, name, url, description FROM github_repos")
        rows = cursor.fetchall()
        if not rows:
            print("[INFO] No repos found.")
        else:
            print(f"\n{'ID':<4} | {'Name':<20} | {'URL':<40}")
            print("-" * 70)
            for r in rows:
                print(f"{r['id']:<4} | {r['name'][:20]:<20} | {r['url'][:40]:<40}")
    elif choice == '3':
        repo_id = input("Enter ID to clone: ").strip()
        cursor.execute("SELECT url FROM github_repos WHERE id = ?", (repo_id,))
        row = cursor.fetchone()
        if row:
            print(f"[INFO] Cloning {row['url']}...")
            subprocess.run(["git", "clone", row['url']])
        else:
            print("[ERROR] Repo not found.")
    conn.close()

def manage_snippets():
    print("\n--- Code Snippets ---")
    print("1. Add Snippet")
    print("2. View Snippet")
    print("3. Delete Snippet")
    choice = input("Select > ").strip()
    
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
        print("[SUCCESS] Snippet saved.")
    elif choice == '2':
        cursor.execute("SELECT id, title, language FROM snippets")
        rows = cursor.fetchall()
        if not rows:
            print("[INFO] No snippets found.")
        else:
            print(f"\n{'ID':<4} | {'Title':<30} | Language")
            print("-" * 55)
            for r in rows:
                print(f"{r['id']:<4} | {r['title'][:30]:<30} | {r['language']}")
            snip_id = input("\nEnter ID to view code (or press enter to cancel): ").strip()
            if snip_id:
                cursor.execute("SELECT code FROM snippets WHERE id = ?", (snip_id,))
                row = cursor.fetchone()
                if row:
                    print("\n--- CODE ---")
                    print(row['code'])
                    print("------------")
    elif choice == '3':
        snip_id = input("Enter ID to delete: ").strip()
        cursor.execute("DELETE FROM snippets WHERE id = ?", (snip_id,))
        conn.commit()
        print("[SUCCESS] Snippet deleted.")
    conn.close()

def manage_notes():
    print("\n--- Quick Notes ---")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Delete Note")
    choice = input("Select > ").strip()
    
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
        print("[SUCCESS] Note saved.")
    elif choice == '2':
        cursor.execute("SELECT id, title, created_at FROM notes")
        rows = cursor.fetchall()
        if not rows:
            print("[INFO] No notes found.")
        else:
            print(f"\n{'ID':<4} | {'Title':<40} | Date")
            print("-" * 70)
            for r in rows:
                print(f"{r['id']:<4} | {r['title'][:40]:<40} | {r['created_at']}")
            note_id = input("\nEnter ID to view content (or press enter to cancel): ").strip()
            if note_id:
                cursor.execute("SELECT content FROM notes WHERE id = ?", (note_id,))
                row = cursor.fetchone()
                if row:
                    print("\n--- CONTENT ---")
                    print(row['content'])
                    print("---------------")
    elif choice == '3':
        note_id = input("Enter ID to delete: ").strip()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        print("[SUCCESS] Note deleted.")
    conn.close()

def export_db():
    print("\n[INFO] Creating database backup...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "toolkit.db")
    backup_path = db_path + ".backup"
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"[SUCCESS] Database exported to: {backup_path}")
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [1] STORAGE & NOTES")
        print("=============================================================")
        print("[1] Links")
        print("[2] Github")
        print("[3] Commands")
        print("[4] Snippets")
        print("[5] Clipboard History")
        print("[6] Quick Notes")
        print("[7] Bookmarks")
        print("[8] Favorites")
        print("[9] Tags")
        print("[10] Import / Export")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            manage_links()
        elif choice == '2':
            manage_github()
        elif choice == '3':
            print("[INFO] Please use the main [13] Run Commands module for this.")
        elif choice == '4':
            manage_snippets()
        elif choice == '5':
            print("[INFO] Please use the [9] Productivity module for Clipboard operations.")
        elif choice == '6':
            manage_notes()
        elif choice == '7' or choice == '8' or choice == '9':
            print("[INFO] Use Links and Notes to manage Bookmarks/Favorites/Tags.")
        elif choice == '10':
            export_db()
        else:
            print("[ERROR] Invalid choice.")
