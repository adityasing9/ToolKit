from toolkit.utils import Colors
from toolkit.db import get_connection
import os
import shutil
import subprocess
import webbrowser

def run_git_cmd(args):
    """Helper to run a git command in the current directory."""
    if not shutil.which("git"):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Git is not installed or not in PATH.")
        return
    try:
        subprocess.run(["git"] + args)
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to run Git command: {e}")

def git_clone():
    url = input("Enter repository URL: ").strip()
    if url:
        run_git_cmd(["clone", url])

def git_commit():
    msg = input("Enter commit message: ").strip()
    if msg:
        run_git_cmd(["add", "."])
        run_git_cmd(["commit", "-m", msg])

def check_installation(tool_name, cmd_args):
    """Checks if a tool is installed and prints its version."""
    print(f"\n--- Checking {tool_name} ---")
    if shutil.which(cmd_args[0]) is None:
        print(f"{Colors.RED}[x]{Colors.RESET} {tool_name} is NOT installed or not in PATH.")
        return
    
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {tool_name} is installed!")
    try:
        output = subprocess.check_output(cmd_args, text=True, stderr=subprocess.STDOUT)
        first_line = output.strip().split('\n')[0]
        print(f"Version: {Colors.CYAN}{first_line}{Colors.RESET}")
    except Exception as e:
        print(f"Could not fetch version: {e}")

def manage_github_repos():
    while True:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, url, description, created_at FROM github_repos ORDER BY id DESC")
        repos = c.fetchall()
        conn.close()

        print(f"\n{Colors.CYAN}--- GitHub Repositories Manager ---{Colors.RESET}")
        if not repos:
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} No saved GitHub repositories.")
        else:
            print(f"{'ID':<4} | {'Name':<20} | {'URL':<35} | Description")
            print("-" * 80)
            for r in repos:
                desc = (r['description'] or "")[:20]
                print(f"{r['id']:<4} | {r['name']:<20} | {r['url']:<35} | {desc}")

        print(f"\n{Colors.GREEN}[1]{Colors.RESET} Add Repo  {Colors.GREEN}[2]{Colors.RESET} Open in Browser  {Colors.GREEN}[3]{Colors.RESET} Clone Repo  {Colors.GREEN}[4]{Colors.RESET} Delete Repo  {Colors.GREEN}[0]{Colors.RESET} Back")
        sub = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if sub == '0':
            break
        elif sub == '1':
            name = input("Repository Name: ").strip()
            url = input("Repository URL: ").strip()
            desc = input("Description (optional): ").strip()
            if name and url:
                conn = get_connection()
                conn.cursor().execute("INSERT INTO github_repos (name, url, description) VALUES (?, ?, ?)", (name, url, desc))
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Repository added.")
        elif sub == '2':
            rid = input("Enter Repo ID to open in browser: ").strip()
            if rid.isdigit():
                conn = get_connection()
                row = conn.cursor().execute("SELECT url FROM github_repos WHERE id = ?", (int(rid),)).fetchone()
                conn.close()
                if row:
                    webbrowser.open(row['url'])
                    print(f"{Colors.GREEN}[INFO]{Colors.RESET} Opening {row['url']} in default browser...")
                else:
                    print(f"{Colors.RED}[ERROR]{Colors.RESET} Repo ID not found.")
        elif sub == '3':
            rid = input("Enter Repo ID to clone: ").strip()
            if rid.isdigit():
                conn = get_connection()
                row = conn.cursor().execute("SELECT url FROM github_repos WHERE id = ?", (int(rid),)).fetchone()
                conn.close()
                if row:
                    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cloning {row['url']}...")
                    run_git_cmd(["clone", row['url']])
                else:
                    print(f"{Colors.RED}[ERROR]{Colors.RESET} Repo ID not found.")
        elif sub == '4':
            rid = input("Enter Repo ID to delete: ").strip()
            if rid.isdigit():
                conn = get_connection()
                conn.cursor().execute("DELETE FROM github_repos WHERE id = ?", (int(rid),))
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Repo entry deleted.")

def manage_ssh_keys():
    print(f"\n{Colors.CYAN}--- SSH Key Manager ---{Colors.RESET}")
    ssh_dir = os.path.expanduser("~/.ssh")
    if not os.path.exists(ssh_dir):
        try:
            os.makedirs(ssh_dir, exist_ok=True)
        except Exception:
            pass

    pub_keys = []
    if os.path.exists(ssh_dir):
        pub_keys = [f for f in os.listdir(ssh_dir) if f.endswith(".pub")]

    if pub_keys:
        print("Existing Public SSH Keys:")
        for pk in pub_keys:
            key_path = os.path.join(ssh_dir, pk)
            print(f"  {Colors.GREEN}• {pk}{Colors.RESET} ({key_path})")
            try:
                with open(key_path, 'r') as kf:
                    print(f"    {Colors.YELLOW}{kf.read().strip()[:65]}...{Colors.RESET}")
            except Exception:
                pass
    else:
        print(f"{Colors.YELLOW}[INFO]{Colors.RESET} No existing SSH keys found in {ssh_dir}")

    print(f"\n{Colors.GREEN}[1]{Colors.RESET} Generate New Ed25519 Key (Recommended)")
    print(f"{Colors.GREEN}[2]{Colors.RESET} Generate New RSA 4096-bit Key")
    print(f"{Colors.GREEN}[3]{Colors.RESET} View Full Key Content")
    print(f"{Colors.GREEN}[0]{Colors.RESET} Back")
    
    sub = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    if sub == '1':
        email = input("Enter your email for the key comment: ").strip()
        if not email:
            email = "toolkit@user"
        key_file = os.path.join(ssh_dir, "id_ed25519")
        print(f"[INFO] Generating Ed25519 key pair at {key_file}...")
        subprocess.run(["ssh-keygen", "-t", "ed25519", "-C", email, "-f", key_file])
    elif sub == '2':
        email = input("Enter your email for the key comment: ").strip()
        if not email:
            email = "toolkit@user"
        key_file = os.path.join(ssh_dir, "id_rsa")
        print(f"[INFO] Generating RSA 4096-bit key pair at {key_file}...")
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", email, "-f", key_file])
    elif sub == '3':
        if pub_keys:
            name = input(f"Enter key filename ({pub_keys[0]}): ").strip() or pub_keys[0]
            target = os.path.join(ssh_dir, name)
            if os.path.exists(target):
                with open(target, 'r') as kf:
                    print(f"\n{Colors.CYAN}--- {name} ---{Colors.RESET}")
                    print(kf.read().strip())
                    print(f"{Colors.CYAN}------------------{Colors.RESET}")
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} File not found.")

def audit_all_dev_tools():
    print(f"\n{Colors.CYAN}--- Comprehensive Dev Environment Audit ---{Colors.RESET}")
    print("Auditing development compilers, runtimes, and containers...\n")
    tools = [
        ("Git", ["git", "--version"]),
        ("Node.js", ["node", "--version"]),
        ("NPM", ["npm", "--version"]),
        ("Python", ["python", "--version"]),
        ("Pip", ["pip", "--version"]),
        ("Java (JDK)", ["java", "-version"]),
        ("Rust (rustc)", ["rustc", "--version"]),
        ("Cargo", ["cargo", "--version"]),
        ("Go", ["go", "version"]),
        ("Docker", ["docker", "--version"]),
        ("Flutter", ["flutter", "--version"]),
        ("VS Code", ["code", "--version"]),
        ("WSL", ["wsl", "--status"])
    ]

    print(f"{'Tool':<15} | {'Status':<12} | Version / Details")
    print("-" * 65)
    for name, cmd in tools:
        if shutil.which(cmd[0]) is None:
            print(f"{name:<15} | {Colors.RED}Not Found{Colors.RESET}    | -")
        else:
            try:
                out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT, timeout=4).strip()
                v_line = out.split('\n')[0][:35]
                print(f"{name:<15} | {Colors.GREEN}Installed{Colors.RESET}    | {Colors.YELLOW}{v_line}{Colors.RESET}")
            except Exception:
                print(f"{name:<15} | {Colors.GREEN}Installed{Colors.RESET}    | Available in PATH")
    print("-" * 65)

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [5] DEVELOPER TOOLS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Git Status & Info")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Git Clone")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Git Commit & Add")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Git Push")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Git Pull")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Git Status")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Git Branches")
        print(f"{Colors.GREEN}[8]{Colors.RESET} GitHub Repos Manager")
        print(f"{Colors.GREEN}[9]{Colors.RESET} SSH Key Manager & Generator")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Docker Check")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Node.js Check")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Python Check")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Java Check")
        print(f"{Colors.GREEN}[14]{Colors.RESET} Rust Check")
        print(f"{Colors.GREEN}[15]{Colors.RESET} Go Check")
        print(f"{Colors.GREEN}[16]{Colors.RESET} Flutter Check")
        print(f"{Colors.GREEN}[17]{Colors.RESET} Android SDK Check")
        print(f"{Colors.GREEN}[18]{Colors.RESET} VS Code Check")
        print(f"{Colors.GREEN}[19]{Colors.RESET} WSL Check")
        print(f"{Colors.GREEN}[20]{Colors.RESET} VirtualBox Check")
        print(f"{Colors.GREEN}[21]{Colors.RESET} VMware Check")
        print(f"{Colors.GREEN}[22]{Colors.RESET} Audit All Dev Environments (1-Click)")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            check_installation("Git", ["git", "--version"])
        elif choice == '2':
            git_clone()
        elif choice == '3':
            git_commit()
        elif choice == '4':
            run_git_cmd(["push"])
        elif choice == '5':
            run_git_cmd(["pull"])
        elif choice == '6':
            run_git_cmd(["status"])
        elif choice == '7':
            run_git_cmd(["branch", "-a"])
        elif choice == '8':
            manage_github_repos()
        elif choice == '9':
            manage_ssh_keys()
        elif choice == '10':
            check_installation("Docker", ["docker", "--version"])
        elif choice == '11':
            check_installation("Node.js", ["node", "--version"])
        elif choice == '12':
            check_installation("Python", ["python", "--version"])
        elif choice == '13':
            check_installation("Java", ["java", "-version"])
        elif choice == '14':
            check_installation("Rust", ["rustc", "--version"])
        elif choice == '15':
            check_installation("Go", ["go", "version"])
        elif choice == '16':
            check_installation("Flutter", ["flutter", "--version"])
        elif choice == '17':
            check_installation("Android SDK", ["adb", "version"])
        elif choice == '18':
            check_installation("VS Code", ["code", "--version"])
        elif choice == '19':
            check_installation("WSL", ["wsl", "--status"])
        elif choice == '20':
            check_installation("VirtualBox", ["VBoxManage", "--version"])
        elif choice == '21':
            check_installation("VMware", ["vmrun"])
        elif choice == '22':
            audit_all_dev_tools()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
