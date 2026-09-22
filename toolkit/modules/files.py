from toolkit.utils import Colors
import os
import shutil
import hashlib
import subprocess
import zipfile
import base64
from getpass import getpass

def set_hidden(path, hide=True):
    if not os.path.exists(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Path does not exist: {path}")
        return
    try:
        if hide:
            subprocess.run(["attrib", "+h", path])
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {path} is now hidden.")
        else:
            subprocess.run(["attrib", "-h", path])
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {path} is now unhidden.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to change attributes: {e}")

def get_folder_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(bytes):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"
        bytes /= factor
    return "0B"

def calculate_folder_size():
    folder = input("Enter folder path: ").strip().replace('"', '')
    if os.path.isdir(folder):
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Calculating...")
        size = get_folder_size(folder)
        print(f"\n[SUCCESS] Size of {folder}: {format_size(size)}")
    else:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid folder path.")

def find_large_files():
    folder = input("Enter folder path to search: ").strip().replace('"', '')
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid folder path.")
        return
    min_mb = input("Enter minimum file size in MB (default 100): ").strip()
    min_mb = int(min_mb) if min_mb.isdigit() else 100
    min_bytes = min_mb * 1024 * 1024
    
    print(f"\n[INFO] Searching for files > {min_mb}MB in {folder}...")
    found = []
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
                if size > min_bytes:
                    found.append((fp, size))
            except:
                pass
                
    found.sort(key=lambda x: x[1], reverse=True)
    if not found:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No files > {min_mb}MB found.")
        return
        
    print(f"\n{'Size':<10} | Path")
    print("-" * 60)
    for fp, size in found[:50]:
        print(f"{format_size(size):<10} | {fp}")

def compress_folder():
    folder = input("Enter folder to compress: ").strip().replace('"', '')
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid folder path.")
        return
    dest = input("Enter destination ZIP filename (e.g. backup.zip): ").strip().replace('"', '')
    if not dest:
        return
    if not dest.endswith('.zip'):
        dest += '.zip'
        
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Compressing {folder} into {dest}...")
    try:
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(folder))
                    zipf.write(file_path, arcname)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Compression complete: {dest}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Compression failed: {e}")

def extract_zip():
    zip_path = input("Enter ZIP file path: ").strip().replace('"', '')
    if not os.path.isfile(zip_path) or not zip_path.endswith('.zip'):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid ZIP file.")
        return
    dest = input("Enter extraction folder (default current): ").strip().replace('"', '') or "."
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(dest)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Extraction complete to {dest}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Extraction failed: {e}")

def calculate_file_hash():
    file_path = input("Enter file path: ").strip().replace('"', '')
    if not os.path.isfile(file_path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file.")
        return
        
    print("\n[INFO] Calculating hashes...")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            print(f"MD5:    {Colors.YELLOW}{hashlib.md5(data).hexdigest()}{Colors.RESET}")
            print(f"SHA1:   {Colors.YELLOW}{hashlib.sha1(data).hexdigest()}{Colors.RESET}")
            print(f"SHA256: {Colors.YELLOW}{hashlib.sha256(data).hexdigest()}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not read file: {e}")

def shred_file(path):
    if not os.path.isfile(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File does not exist: {path}")
        return
    try:
        size = os.path.getsize(path)
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Shredding {path} ({format_size(size)})...")
        with open(path, "ba+", buffering=0) as f:
            for pass_num in range(3):
                print(f"   Pass {pass_num+1}/3 (Overwriting with random bytes)...")
                f.seek(0)
                remaining = size
                while remaining > 0:
                    chunk = min(remaining, 1024 * 1024)
                    f.write(os.urandom(chunk))
                    remaining -= chunk
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        os.remove(path)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} File permanently shredded.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Shredding failed: {e}")

def find_duplicates():
    folder = input("Enter folder path to search: ").strip().replace('"', '')
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid folder path.")
        return
        
    print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Scanning files for duplicates...")
    by_size = {}
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
                by_size.setdefault(size, []).append(fp)
            except:
                pass
                
    potential_dupes = {sz: paths for sz, paths in by_size.items() if len(paths) > 1}
    if not potential_dupes:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No duplicates found.")
        return
        
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Calculating file hashes for potential duplicates...")
    by_hash = {}
    for size, paths in potential_dupes.items():
        for fp in paths:
            try:
                hasher = hashlib.md5()
                with open(fp, "rb") as f:
                    for chunk in iter(lambda: f.read(65536), b""):
                        hasher.update(chunk)
                file_hash = hasher.hexdigest()
                by_hash.setdefault((size, file_hash), []).append(fp)
            except:
                pass
                
    duplicates = {k: paths for k, paths in by_hash.items() if len(paths) > 1}
    if not duplicates:
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} No duplicates found.")
        return
        
    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Found duplicate sets:")
    all_dupe_files = []
    idx = 1
    for (size, file_hash), paths in duplicates.items():
        print(f"\nSet #{idx} (Size: {format_size(size)}, MD5: {file_hash})")
        print(f"  [Original] {paths[0]}")
        for p in paths[1:]:
            print(f"  [Duplicate] {p}")
            all_dupe_files.append(p)
        idx += 1
            
    confirm = input(f"\nWould you like to delete all {len(all_dupe_files)} duplicates? (y/n): ").strip().lower()
    if confirm == 'y':
        deleted_count = 0
        for p in all_dupe_files:
            try:
                os.remove(p)
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {p}: {e}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Deleted {deleted_count} duplicate files.")

def mass_rename_files():
    print(f"\n{Colors.CYAN}--- Mass File Renamer ---{Colors.RESET}")
    folder = input("Enter folder path containing files: ").strip().replace('"', '')
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Directory not found.")
        return

    files = [f for f in sorted(os.listdir(folder)) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print(f"{Colors.YELLOW}[INFO]{Colors.RESET} No files found in this folder.")
        return

    print(f"\nFound {len(files)} files.")
    print(f"{Colors.GREEN}[1]{Colors.RESET} Add Prefix (e.g. 'Project_')")
    print(f"{Colors.GREEN}[2]{Colors.RESET} Add Suffix before extension (e.g. '_v1')")
    print(f"{Colors.GREEN}[3]{Colors.RESET} Find and Replace Text")
    print(f"{Colors.GREEN}[4]{Colors.RESET} Sequential Numbering (e.g. 'Item_001.ext')")
    print(f"{Colors.GREEN}[5]{Colors.RESET} Change Extension (e.g. .jpeg -> .jpg)")
    print(f"{Colors.GREEN}[6]{Colors.RESET} Convert to Lowercase")
    print(f"{Colors.GREEN}[0]{Colors.RESET} Cancel")
    
    sub = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
    if sub == '0':
        return

    new_names = []
    if sub == '1':
        prefix = input("Enter prefix to add: ").strip()
        new_names = [(f, f"{prefix}{f}") for f in files]
    elif sub == '2':
        suffix = input("Enter suffix to add: ").strip()
        for f in files:
            name, ext = os.path.splitext(f)
            new_names.append((f, f"{name}{suffix}{ext}"))
    elif sub == '3':
        find_str = input("Find text: ")
        replace_str = input("Replace with: ")
        new_names = [(f, f.replace(find_str, replace_str)) for f in files]
    elif sub == '4':
        base_name = input("Base filename (e.g. Doc): ").strip() or "File"
        pad = len(str(len(files)))
        for i, f in enumerate(files, 1):
            _, ext = os.path.splitext(f)
            new_names.append((f, f"{base_name}_{str(i).zfill(pad)}{ext}"))
    elif sub == '5':
        old_ext = input("Old extension to match (e.g. .jpeg): ").strip()
        if not old_ext.startswith('.'): old_ext = '.' + old_ext
        new_ext = input("New extension (e.g. .jpg): ").strip()
        if not new_ext.startswith('.'): new_ext = '.' + new_ext
        for f in files:
            name, ext = os.path.splitext(f)
            if ext.lower() == old_ext.lower():
                new_names.append((f, f"{name}{new_ext}"))
            else:
                new_names.append((f, f))
    elif sub == '6':
        new_names = [(f, f.lower()) for f in files]

    # Show preview
    changes = [(orig, nxt) for orig, nxt in new_names if orig != nxt]
    if not changes:
        print(f"{Colors.YELLOW}[INFO]{Colors.RESET} No files will be changed with these settings.")
        return

    print(f"\n{Colors.CYAN}--- Rename Preview (First 10) ---{Colors.RESET}")
    for orig, nxt in changes[:10]:
        print(f"  {orig} -> {Colors.GREEN}{nxt}{Colors.RESET}")
    if len(changes) > 10:
        print(f"  ...and {len(changes) - 10} more files.")

    confirm = input(f"\nApply changes to {len(changes)} files? (y/n): ").strip().lower()
    if confirm == 'y':
        success = 0
        for orig, nxt in changes:
            try:
                os.rename(os.path.join(folder, orig), os.path.join(folder, nxt))
                success += 1
            except Exception as e:
                print(f"Error renaming {orig}: {e}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Renamed {success}/{len(changes)} files.")

def _derive_fernet_key(password: str, salt: bytes) -> bytes:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file():
    print(f"\n{Colors.CYAN}--- File Encryption (AES-256 / Fernet) ---{Colors.RESET}")
    path = input("Enter path of file to encrypt: ").strip().replace('"', '')
    if not os.path.isfile(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File not found.")
        return
    pwd = getpass("Enter encryption password: ").strip()
    if not pwd:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Password cannot be empty.")
        return
    pwd_confirm = getpass("Confirm password: ").strip()
    if pwd != pwd_confirm:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Passwords do not match.")
        return

    from cryptography.fernet import Fernet
    salt = os.urandom(16)
    key = _derive_fernet_key(pwd, salt)
    f = Fernet(key)

    try:
        with open(path, 'rb') as infile:
            data = infile.read()
        encrypted = f.encrypt(data)
        out_path = path + ".enc"
        with open(out_path, 'wb') as outfile:
            outfile.write(salt + encrypted)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} File encrypted successfully: {out_path}")
        del_orig = input("Securely shred original unencrypted file? (y/n): ").strip().lower()
        if del_orig == 'y':
            shred_file(path)
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Encryption failed: {e}")

def decrypt_file():
    print(f"\n{Colors.CYAN}--- File Decryption (AES-256 / Fernet) ---{Colors.RESET}")
    path = input("Enter path of encrypted .enc file: ").strip().replace('"', '')
    if not os.path.isfile(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File not found.")
        return
    pwd = getpass("Enter decryption password: ").strip()
    if not pwd:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Password cannot be empty.")
        return

    from cryptography.fernet import Fernet
    try:
        with open(path, 'rb') as infile:
            salt = infile.read(16)
            encrypted = infile.read()
        key = _derive_fernet_key(pwd, salt)
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
        
        out_path = path[:-4] if path.endswith(".enc") else path + ".dec"
        with open(out_path, 'wb') as outfile:
            outfile.write(decrypted)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} File decrypted successfully: {out_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Decryption failed (Wrong password or corrupted file): {e}")

def secure_folder_lock():
    print(f"\n{Colors.CYAN}--- Secure Folder Lock (NTFS ACL + System Attribute) ---{Colors.RESET}")
    folder = input("Enter folder path to lock: ").strip().replace('"', '')
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Directory not found.")
        return
    try:
        username = os.environ.get("USERNAME", "Everyone")
        subprocess.run(["icacls", folder, "/deny", f"{username}:(OI)(CI)(F)"], check=True)
        subprocess.run(["attrib", "+s", "+h", folder])
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Folder locked and hidden: {folder}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to lock folder: {e}")

def unlock_folder():
    print(f"\n{Colors.CYAN}--- Unlock Secure Folder ---{Colors.RESET}")
    folder = input("Enter folder path to unlock: ").strip().replace('"', '')
    if not os.path.exists(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Path not found.")
        return
    try:
        username = os.environ.get("USERNAME", "Everyone")
        subprocess.run(["attrib", "-s", "-h", folder])
        subprocess.run(["icacls", folder, "/remove:d", username], check=True)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Folder unlocked: {folder}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to unlock folder: {e}")

def change_file_timestamps():
    print(f"\n{Colors.CYAN}--- Change File/Folder Timestamps ---{Colors.RESET}")
    path = input("Enter path: ").strip().replace('"', '')
    if not os.path.exists(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Path does not exist.")
        return
        
    print("\nFormat: YYYY-MM-DD HH:MM:SS (e.g. 2026-07-11 17:00:00)")
    created = input("Enter New Creation Date/Time (press Enter to skip): ").strip()
    modified = input("Enter New Modification Date/Time (press Enter to skip): ").strip()
    accessed = input("Enter New Last Access Date/Time (press Enter to skip): ").strip()
    
    is_dir = os.path.isdir(path)
    io_class = "Directory" if is_dir else "File"
    
    commands = []
    if created:
        commands.append(f'[System.IO.{io_class}]::SetCreationTime("{path}", "{created}")')
    if modified:
        commands.append(f'[System.IO.{io_class}]::SetLastWriteTime("{path}", "{modified}")')
    if accessed:
        commands.append(f'[System.IO.{io_class}]::SetLastAccessTime("{path}", "{accessed}")')
        
    if not commands:
        print("[INFO] No changes specified.")
        return
        
    ps_cmd = "; ".join(commands)
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0:
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Timestamps updated successfully.")
        else:
            err_msg = res.stderr.strip()
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to update timestamps: {err_msg}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Command execution failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [8] FILE & FOLDER{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Hide File")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Unhide File")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Hide Folder")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Unhide Folder")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Secure Folder (Lock Access)")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Unlock Folder")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Encrypt File (AES-256)")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Decrypt File (AES-256)")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Find Large Files")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Duplicate Finder")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Folder Size Calculator")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Mass File Renamer")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Compress to ZIP")
        print(f"{Colors.GREEN}[14]{Colors.RESET} Extract from ZIP")
        print(f"{Colors.GREEN}[15]{Colors.RESET} File Hash (MD5, SHA1, SHA256)")
        print(f"{Colors.GREEN}[16]{Colors.RESET} Secure Delete (Shred File)")
        print(f"{Colors.GREEN}[17]{Colors.RESET} Change File Timestamps")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            path = input("Enter file path to hide: ").strip().replace('"', '')
            if path: set_hidden(path, True)
        elif choice == '2':
            path = input("Enter file path to unhide: ").strip().replace('"', '')
            if path: set_hidden(path, False)
        elif choice == '3':
            path = input("Enter folder path to hide: ").strip().replace('"', '')
            if path: set_hidden(path, True)
        elif choice == '4':
            path = input("Enter folder path to unhide: ").strip().replace('"', '')
            if path: set_hidden(path, False)
        elif choice == '5':
            secure_folder_lock()
        elif choice == '6':
            unlock_folder()
        elif choice == '7':
            encrypt_file()
        elif choice == '8':
            decrypt_file()
        elif choice == '9':
            find_large_files()
        elif choice == '10':
            find_duplicates()
        elif choice == '11':
            calculate_folder_size()
        elif choice == '12':
            mass_rename_files()
        elif choice == '13':
            compress_folder()
        elif choice == '14':
            extract_zip()
        elif choice == '15':
            calculate_file_hash()
        elif choice == '16':
            path = input("Enter file path to secure delete (SHRED): ").strip().replace('"', '')
            if path:
                confirm = input(f"[WARNING] Are you sure you want to permanently shred {path}? (y/n): ").strip().lower()
                if confirm == 'y':
                    shred_file(path)
        elif choice == '17':
            change_file_timestamps()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
