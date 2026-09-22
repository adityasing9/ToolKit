from toolkit.utils import Colors
import urllib.request
import urllib.error
import json
import base64
import os
import shutil
import socket
import datetime
from toolkit.db import get_setting, DB_PATH, get_connection

def call_supabase(method, endpoint, payload=None, headers_extra=None):
    sb_url = get_setting("supabase_url")
    sb_key = get_setting("supabase_key")
    if not sb_url or not sb_key:
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Supabase URL or Key is not configured.")
        print(f"Please configure them in {Colors.YELLOW}[20] Settings -> [1] Configure API / Cloud Keys{Colors.RESET}.")
        return None
        
    url = f"{sb_url.rstrip('/')}/rest/v1/{endpoint}"
    
    headers = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
    }
    if headers_extra:
        headers.update(headers_extra)
        
    data = json.dumps(payload).encode("utf-8") if payload else None
    
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method
    )
    
    try:
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Contacting Supabase Cloud...")
        with urllib.request.urlopen(req, timeout=20) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 404:
            print(f"\n{Colors.RED}[ERROR] Table not found in Supabase!{Colors.RESET}")
            print("Please run the following SQL command in your Supabase SQL Editor to create the backups table:")
            print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
            print("create table toolkit_backups (")
            print("  id bigint primary key generated always as identity,")
            print("  created_at timestamptz default now(),")
            print("  backup_data text not null,")
            print("  device_name text")
            print(");")
            print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Cloud operation failed (HTTP {e.code}): {body}")
        return None
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Connection failed: {e}")
        return None

def cloud_backup():
    if not os.path.exists(DB_PATH):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Local database not found at {DB_PATH}.")
        return

    try:
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Reading local database...")
        with open(DB_PATH, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to read database: {e}")
        return

    payload = {
        "backup_data": b64_data,
        "device_name": socket.gethostname()
    }
    
    response = call_supabase("POST", "toolkit_backups", payload, headers_extra={"Prefer": "return=minimal"})
    if response is not None:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Database backup uploaded successfully to Supabase cloud!")

def cloud_restore():
    url_suffix = "toolkit_backups?select=id,created_at,device_name,backup_data&order=id.desc&limit=1"
    response = call_supabase("GET", url_suffix)
    
    if not response:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} No backups found or failed to fetch.")
        return
        
    backup = response[0]
    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Found backup from {backup['created_at']} (Device: {backup['device_name']})")
    confirm = input("Are you sure you want to restore? This will OVERWRITE your local database. (y/n): ").strip().lower()
    if confirm != 'y':
        return

    try:
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Restoring database file...")
        db_bytes = base64.b64decode(backup['backup_data'])
        with open(DB_PATH, "wb") as f:
            f.write(db_bytes)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Database restored successfully! Please restart the Toolkit to load restored data.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to restore database: {e}")

def list_backups():
    url_suffix = "toolkit_backups?select=id,created_at,device_name&order=id.desc"
    response = call_supabase("GET", url_suffix)
    if not response:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No backups found on the cloud.")
        return
        
    print(f"\n{Colors.CYAN}--- Cloud Backups ---{Colors.RESET}")
    for b in response:
        print(f"[{Colors.GREEN}ID: {b['id']}{Colors.RESET}] Device: {b['device_name']} (Uploaded: {b['created_at']})")
    print(f"{Colors.CYAN}---------------------{Colors.RESET}")

def local_backup():
    if not os.path.exists(DB_PATH):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Local database not found at {DB_PATH}.")
        return
    backup_dir = os.path.join(os.path.dirname(DB_PATH), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_dir, f"toolkit_backup_{ts}.db")
    try:
        shutil.copy2(DB_PATH, dest)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Local backup created at:\n{dest}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Backup failed: {e}")

def export_all_json():
    print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Exporting all user data to JSON...")
    conn = get_connection()
    c = conn.cursor()
    
    export_data = {
        "exported_at": str(datetime.datetime.now()),
        "device": socket.gethostname(),
        "notes": [dict(r) for r in c.execute("SELECT * FROM notes").fetchall()],
        "links": [dict(r) for r in c.execute("SELECT * FROM links").fetchall()],
        "github_repos": [dict(r) for r in c.execute("SELECT * FROM github_repos").fetchall()],
        "snippets": [dict(r) for r in c.execute("SELECT * FROM snippets").fetchall()],
        "todos": [dict(r) for r in c.execute("SELECT * FROM todos").fetchall()],
        "expenses": [dict(r) for r in c.execute("SELECT * FROM expenses").fetchall()]
    }
    conn.close()

    export_path = os.path.join(os.getcwd(), "toolkit_export.json")
    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Full export saved to: {export_path}")
        print(f"Includes: {len(export_data['notes'])} notes, {len(export_data['links'])} links, {len(export_data['todos'])} todos, {len(export_data['expenses'])} expenses")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Export failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [4] CLOUD WORKSPACE{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Cloud Backup (Upload to Supabase)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Cloud Restore (Download from Supabase)")
        print(f"{Colors.GREEN}[3]{Colors.RESET} List Cloud Backups")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Local Offline Backup (Timestamped DB Copy)")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Export All Data to JSON (Portable File)")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            cloud_backup()
        elif choice == '2':
            cloud_restore()
        elif choice == '3':
            list_backups()
        elif choice == '4':
            local_backup()
        elif choice == '5':
            export_all_json()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
