from toolkit.utils import Colors
import os
import subprocess

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_ps_command(ps_cmd, require_admin=True):
    if require_admin and not is_admin():
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Administrator privileges required for this action.")
        return None
    try:
        result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to run command: {e}")
        return None

def list_users():
    print(f"\n{Colors.CYAN}--- List of Local Users ---{Colors.RESET}")
    output = run_ps_command("Get-LocalUser | Select-Object Name, Enabled, Description | Format-Table -AutoSize", require_admin=False)
    if output:
        print(output)

def add_user():
    print(f"\n{Colors.CYAN}--- Add New User ---{Colors.RESET}")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    desc = input("Description (optional): ").strip()
    
    if not username or not password:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Username and Password are required.")
        return
        
    ps = f'$Password = Read-Host -AsSecureString "{password}"; New-LocalUser "{username}" -Password $Password -FullName "{username}" -Description "{desc}"'
    # For automation we bypass Read-Host to pass plain text
    ps_auto = f'$Password = ConvertTo-SecureString "{password}" -AsPlainText -Force; New-LocalUser "{username}" -Password $Password -FullName "{username}" -Description "{desc}"'
    
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Creating user {username}...")
    res = run_ps_command(ps_auto)
    if res is not None:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} User '{username}' created successfully.")

def delete_user():
    print(f"\n{Colors.CYAN}--- Delete User ---{Colors.RESET}")
    username = input("Username to delete: ").strip()
    if not username: return
    
    confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").strip().lower()
    if confirm == 'y':
        res = run_ps_command(f'Remove-LocalUser -Name "{username}"')
        if res is not None:
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} User '{username}' deleted.")

def change_password():
    print(f"\n{Colors.CYAN}--- Change User Password ---{Colors.RESET}")
    username = input("Username: ").strip()
    new_password = input("New Password: ").strip()
    
    if not username or not new_password: return
    ps_auto = f'$Password = ConvertTo-SecureString "{new_password}" -AsPlainText -Force; Set-LocalUser -Name "{username}" -Password $Password'
    res = run_ps_command(ps_auto)
    if res is not None:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Password for '{username}' updated.")

def set_user_status(username, enable=True):
    action = "Enable" if enable else "Disable"
    ps_cmd = f'{action}-LocalUser -Name "{username}"'
    res = run_ps_command(ps_cmd)
    if res is not None:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} User '{username}' has been {action.lower()}d.")

def toggle_user(enable=True):
    action = "Enable" if enable else "Disable"
    print(f"\n--- {action} User ---")
    username = input("Username: ").strip()
    if username:
        set_user_status(username, enable)

def modify_admin(username, grant=True):
    action = "Add" if grant else "Remove"
    ps_cmd = f'{action}-LocalGroupMember -Group "Administrators" -Member "{username}"'
    res = run_ps_command(ps_cmd)
    if res is not None:
        status = "granted" if grant else "removed from"
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Administrator rights {status} '{username}'.")

def toggle_admin(grant=True):
    action_str = "Grant" if grant else "Remove"
    print(f"\n--- {action_str} Administrator Rights ---")
    username = input("Username: ").strip()
    if username:
        modify_admin(username, grant)

def user_info():
    print(f"\n{Colors.CYAN}--- Detailed Account Information ---{Colors.RESET}")
    username = input("Username: ").strip()
    if username:
        output = run_ps_command(f'Get-LocalUser -Name "{username}" | Format-List *', require_admin=False)
        if output:
            print(output)

def export_users():
    print(f"\n{Colors.CYAN}--- Export User List ---{Colors.RESET}")
    filename = input("Filename (default users.csv): ").strip()
    if not filename: filename = "users.csv"
    
    ps_cmd = f'Get-LocalUser | Select-Object Name, Enabled, Description | Export-Csv -Path "{filename}" -NoTypeInformation'
    res = run_ps_command(ps_cmd, require_admin=False)
    if res is not None:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} User list exported to {filename}.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [15] USER MANAGEMENT{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} List Users")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Add User")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Delete User")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Change Password")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Enable User")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Disable User")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Grant Administrator")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Remove Administrator")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Account Information")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Export User List")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            list_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            change_password()
        elif choice == '5':
            toggle_user(enable=True)
        elif choice == '6':
            toggle_user(enable=False)
        elif choice == '7':
            toggle_admin(grant=True)
        elif choice == '8':
            toggle_admin(grant=False)
        elif choice == '9':
            user_info()
        elif choice == '10':
            export_users()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
