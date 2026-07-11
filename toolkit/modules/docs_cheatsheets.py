from toolkit.utils import Colors
import sys

def draw_table(title, headers, rows):
    """Draw a clean, aligned table for console reading."""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== {title} ==={Colors.RESET}")
    
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(str(cell)))
            
    # Draw header
    border = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    print(border)
    header_str = "|" + "|".join([f" {headers[i]:<{widths[i]}} " for i in range(len(headers))]) + "|"
    print(header_str)
    print(border)
    
    # Draw rows
    for row in rows:
        row_str = "|" + "|".join([f" {str(row[i]):<{widths[i]}} " for i in range(len(row))]) + "|"
        print(row_str)
    print(border)

def show_windows_commands():
    headers = ["Command", "Description"]
    rows = [
        ["sfc /scannow", "Scans and repairs corrupt Windows system files"],
        ["dism /online /cleanup-image /restorehealth", "Restores system health via online Windows Update image"],
        ["ipconfig /flushdns", "Clears DNS resolver cache to fix connection issues"],
        ["gpupdate /force", "Forces update of local and Active Directory Group Policies"],
        ["chkdsk /f C:", "Scans and fixes errors on Drive C (requires reboot)"],
        ["systeminfo", "Retrieves detailed operating system and hardware specifications"],
        ["Get-Service | Where Status -eq Running", "PowerShell cmdlet listing all running system services"],
        ["wmic diskdrive get status", "Checks S.M.A.R.T drive health status"]
    ]
    draw_table("Windows Command Reference", headers, rows)
    input("\nPress Enter to continue...")

def show_linux_commands():
    headers = ["Command", "Category", "Description"]
    rows = [
        ["ls -la", "File List", "Lists all files, permissions, and sizes in detailed format"],
        ["chmod 755 file", "Permissions", "Sets Read/Write/Execute for owner, Read/Execute for others"],
        ["chown user:group file", "Ownership", "Changes the owner user and group of a file or folder"],
        ["df -h", "System Info", "Displays disk usage of all filesystems in human-readable format"],
        ["free -h", "System Info", "Displays active, cached, and total physical RAM and swap usage"],
        ["find / -name filename", "Search", "Recursively searches the filesystem from root for filename"],
        ["grep -rn 'query' .", "Search", "Recursively searches files in directory for matching query lines"],
        ["top / htop", "Processes", "Live interactive CPU, RAM, and process activity monitor"]
    ]
    draw_table("Linux/Bash Command Reference", headers, rows)
    input("\nPress Enter to continue...")

def show_git_cheat_sheet():
    headers = ["Command", "Action / Usage"]
    rows = [
        ["git init", "Initializes a new local Git repository in the current folder"],
        ["git clone <url>", "Clones a remote repository to your local machine"],
        ["git add .", "Stages all modified and new files for the next commit"],
        ["git commit -m \"msg\"", "Commits staged snapshots with a descriptive message"],
        ["git status", "Shows working tree status (untracked, modified, staged files)"],
        ["git checkout -b <name>", "Creates and switches to a new local branch"],
        ["git merge <branch>", "Merges changes from target branch into current branch"],
        ["git stash / stash pop", "Temporarily saves active changes / restores stashed changes"],
        ["git log --oneline", "Lists commit history in a clean, one-line-per-commit format"],
        ["git reset --hard HEAD~1", "Rolls back local repository and workspace to the previous commit"]
    ]
    draw_table("Git Version Control Cheat Sheet", headers, rows)
    input("\nPress Enter to continue...")

def show_sql_cheat_sheet():
    headers = ["SQL Syntax / Clause", "Example Usage"]
    rows = [
        ["SELECT ... FROM ...", "SELECT name, age FROM users WHERE age > 18;"],
        ["INSERT INTO ...", "INSERT INTO users (name, age) VALUES ('Aadi', 21);"],
        ["UPDATE ... SET ...", "UPDATE users SET age = 22 WHERE name = 'Aadi';"],
        ["DELETE FROM ...", "DELETE FROM users WHERE age < 18;"],
        ["INNER JOIN", "SELECT * FROM users U INNER JOIN orders O ON U.id = O.user_id;"],
        ["LEFT / RIGHT JOIN", "SELECT * FROM users U LEFT JOIN orders O ON U.id = O.user_id;"],
        ["CREATE TABLE", "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INT);"],
        ["GROUP BY / HAVING", "SELECT age, COUNT(*) FROM users GROUP BY age HAVING COUNT(*) > 1;"],
        ["CREATE INDEX", "CREATE INDEX idx_user_name ON users(name);"]
    ]
    draw_table("SQL Relational Database Cheat Sheet", headers, rows)
    input("\nPress Enter to continue...")

def show_regex_examples():
    headers = ["Pattern", "Meaning", "Example Match"]
    rows = [
        ["^ / $", "Start / End of string", "^hello matches start, world$ matches end"],
        ["\\d / \\D", "Digit / Non-Digit", "\\d matches '5', \\D matches 'a'"],
        ["\\w / \\W", "Alphanumeric / Non-Alphanumeric", "\\w matches 'x', \\W matches '!'"],
        ["* / + / ?", "0 or more / 1 or more / 0 or 1", "a* matches '', a+ matches 'aaa', a? matches 'a'"],
        ["{m,n}", "m to n occurrences", "a{2,4} matches 'aa', 'aaa', 'aaaa'"],
        ["(a|b)", "Alternation (OR)", "(cat|dog) matches 'cat' or 'dog'"],
        ["Email Regex", "Validates emails", "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"],
        ["IPv4 Regex", "Validates IP address", "^(\\d{1,3}\\.){3}\\d{1,3}$"]
    ]
    draw_table("Regular Expression (Regex) Reference", headers, rows)
    input("\nPress Enter to continue...")

def show_markdown_guide():
    headers = ["Element", "Syntax", "Output Example"]
    rows = [
        ["Headers", "# H1  ## H2  ### H3", "Large titles to section headers"],
        ["Emphasis", "*italic* or **bold**", "Italic text or Bold text for callouts"],
        ["Lists", "- Item 1  1. Item A", "Unordered bullet lists or Ordered lists"],
        ["Links", "[Google](https://google.com)", "Clickable text directing to URLs"],
        ["Code Inline", "`print('hello')`", "Monospaced code snippet in a sentence"],
        ["Code Block", "```python \\n ... \\n ```", "Syntax highlighted drop-down block"],
        ["Tables", "| Header | \\n | --- |", "Symmetric grids organizing information"],
        ["Blockquotes", "> Important Quote", "Indented, shaded text blocks for emphasis"]
    ]
    draw_table("Markdown Syntax Formatting Guide", headers, rows)
    input("\nPress Enter to continue...")

def show_keyboard_shortcuts():
    headers = ["Application", "Shortcut", "Action / Description"]
    rows = [
        ["Windows", "Win + D", "Instantly minimizes all windows and shows Desktop"],
        ["Windows", "Win + L", "Locks your Windows user profile session immediately"],
        ["Windows", "Ctrl + Shift + Esc", "Launches the Windows Task Manager directly"],
        ["Windows", "Win + Shift + S", "Opens the Windows snipping overlay tool"],
        ["Browsers", "Ctrl + T / Ctrl + W", "Opens a new browser tab / Closes current tab"],
        ["Browsers", "Ctrl + Shift + T", "Reopens the last closed browser tab"],
        ["VS Code", "Ctrl + P", "Launches quick open menu to search and load files"],
        ["VS Code", "Ctrl + Shift + P", "Launches the command palette matching features"],
        ["VS Code", "Ctrl + Shift + L", "Selects all instances of the current cursor word"]
    ]
    draw_table("Common Keyboard Shortcuts Reference", headers, rows)
    input("\nPress Enter to continue...")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [19] CHEAT SHEETS & DOCUMENTATION{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Windows Commands Cheat Sheet")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Linux Commands Cheat Sheet")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Git Cheat Sheet")
        print(f"{Colors.GREEN}[4]{Colors.RESET} SQL Cheat Sheet")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Regex Examples Guide")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Markdown Formatting Guide")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Essential Keyboard Shortcuts")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            show_windows_commands()
        elif choice == '2':
            show_linux_commands()
        elif choice == '3':
            show_git_cheat_sheet()
        elif choice == '4':
            show_sql_cheat_sheet()
        elif choice == '5':
            show_regex_examples()
        elif choice == '6':
            show_markdown_guide()
        elif choice == '7':
            show_keyboard_shortcuts()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
