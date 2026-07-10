import os
import shutil
import subprocess

def run_git_cmd(args):
    """Helper to run a git command in the current directory."""
    if not shutil.which("git"):
        print("[ERROR] Git is not installed or not in PATH.")
        return
    try:
        subprocess.run(["git"] + args)
    except Exception as e:
        print(f"[ERROR] Failed to run Git command: {e}")

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
        print(f"[x] {tool_name} is NOT installed or not in PATH.")
        return
    
    print(f"[✓] {tool_name} is installed!")
    try:
        output = subprocess.check_output(cmd_args, text=True, stderr=subprocess.STDOUT)
        print(f"Version: {output.strip()}")
    except Exception as e:
        print(f"Could not fetch version: {e}")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [8] DEVELOPER TOOLS")
        print("=============================================================")
        print("[1] Git")
        print("[2] Clone Repo")
        print("[3] Commit")
        print("[4] Push")
        print("[5] Pull")
        print("[6] Status")
        print("[7] Branch")
        print("[8] Github URLs")
        print("[9] SSH Keys")
        print("[10] Docker")
        print("[11] Node")
        print("[12] Python")
        print("[13] Java")
        print("[14] Rust")
        print("[15] Go")
        print("[16] Flutter")
        print("[17] Android")
        print("[18] VS Code")
        print("[19] WSL")
        print("[20] VirtualBox")
        print("[21] VMware")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[INFO] Github URLs coming soon...")
        elif choice == '9':
            print("\n--- SSH Keys ---")
            ssh_dir = os.path.expanduser("~/.ssh")
            if os.path.exists(ssh_dir):
                files = os.listdir(ssh_dir)
                for f in files:
                    if f.endswith(".pub"):
                        print(f"Public Key Found: {f}")
                        with open(os.path.join(ssh_dir, f), 'r') as key_file:
                            print(key_file.read().strip())
            else:
                print("No ~/.ssh directory found.")
        elif choice == '10':
            check_installation("Docker", ["docker", "--version"])
        elif choice == '11':
            check_installation("Node.js", ["node", "-v"])
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
            check_installation("Android Studio (ADB)", ["adb", "--version"])
        elif choice == '18':
            check_installation("VS Code", ["code", "--version"])
        elif choice == '19':
            check_installation("WSL", ["wsl", "--version"])
        elif choice == '20':
            check_installation("VirtualBox", ["VBoxManage", "--version"])
        elif choice == '21':
            check_installation("VMware", ["vmrun"])
        else:
            print("[ERROR] Invalid choice.")
