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
        print("[ERROR] Administrator privileges required for this action.")
        return None
    try:
        result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] Failed to run command: {e}")
        return None

def list_users():
    print("\n--- List of Local Users ---")
    output = run_ps_command("Get-LocalUser | Select-Object Name, Enabled, Description | Format-Table -AutoSize", require_admin=False)
    if output:
        print(output)

def add_user():
    print("\n--- Add New User ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    desc = input("Description (optional): ").strip()
    
    if not username or not password:
        print("[ERROR] Username and Password are required.")
        return
        
    ps = f'$Password = Read-Host -AsSecureString "{password}"; New-LocalUser "{username}" -Password $Password -FullName "{username}" -Description "{desc}"'
    # For automation we bypass Read-Host to pass plain text
    ps_auto = f'$Password = ConvertTo-SecureString "{password}" -AsPlainText -Force; New-LocalUser "{username}" -Password $Password -FullName "{username}" -Description "{desc}"'
    
    print(f"[INFO] Creating user {username}...")
    res = run_ps_command(ps_auto)
    if res is not None:
        print(f"[SUCCESS] User '{username}' created successfully.")

def delete_user():
    print("\n--- Delete User ---")
    username = input("Username to delete: ").strip()
    if not username: return
    
    confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").strip().lower()
    if confirm == 'y':
        res = run_ps_command(f'Remove-LocalUser -Name "{username}"')
        if res is not None:
            print(f"[SUCCESS] User '{username}' deleted.")

def change_password():
    print("\n--- Change User Password ---")
    username = input("Username: ").strip()
    new_password = input("New Password: ").strip()
    
    if not username or not new_password: return
    ps_auto = f'$Password = ConvertTo-SecureString "{new_password}" -AsPlainText -Force; Set-LocalUser -Name "{username}" -Password $Password'
    res = run_ps_command(ps_auto)
    if res is not None:
        print(f"[SUCCESS] Password for '{username}' updated.")

def set_user_status(username, enable=True):
    action = "Enable" if enable else "Disable"
    ps_cmd = f'{action}-LocalUser -Name "{username}"'
    res = run_ps_command(ps_cmd)
    if res is not None:
        print(f"[SUCCESS] User '{username}' has been {action.lower()}d.")

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
        print(f"[SUCCESS] Administrator rights {status} '{username}'.")

def toggle_admin(grant=True):
    action_str = "Grant" if grant else "Remove"
    print(f"\n--- {action_str} Administrator Rights ---")
    username = input("Username: ").strip()
    if username:
        modify_admin(username, grant)

def user_info():
    print("\n--- Detailed Account Information ---")
    username = input("Username: ").strip()
    if username:
        output = run_ps_command(f'Get-LocalUser -Name "{username}" | Format-List *', require_admin=False)
        if output:
            print(output)

def export_users():
    print("\n--- Export User List ---")
    filename = input("Filename (default users.csv): ").strip()
    if not filename: filename = "users.csv"
    
    ps_cmd = f'Get-LocalUser | Select-Object Name, Enabled, Description | Export-Csv -Path "{filename}" -NoTypeInformation'
    res = run_ps_command(ps_cmd, require_admin=False)
    if res is not None:
        print(f"[SUCCESS] User list exported to {filename}.")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [3] USER MANAGEMENT")
        print("=============================================================")
        print("[1] List Users")
        print("[2] Add User")
        print("[3] Delete User")
        print("[4] Change Password")
        print("[5] Enable User")
        print("[6] Disable User")
        print("[7] Grant Administrator")
        print("[8] Remove Administrator")
        print("[9] Account Information")
        print("[10] Export User List")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[ERROR] Invalid choice.")
