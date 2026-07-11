from toolkit.utils import Colors
import os
import shutil
import hashlib
import subprocess
import zipfile

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
    folder = input("Enter folder path: ").strip()
    if os.path.isdir(folder):
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Calculating...")
        size = get_folder_size(folder)
        print(f"\n[SUCCESS] Size of {folder}: {format_size(size)}")
    else:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid folder path.")

def find_large_files():
    folder = input("Enter folder path to search: ").strip()
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
    for fp, size in found[:50]:  # Top 50
        print(f"{format_size(size):<10} | {fp}")

def compress_folder():
    folder = input("Enter folder to compress: ").strip()
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid folder path.")
        return
    dest = input("Enter destination ZIP filename (e.g. backup.zip): ").strip()
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
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Compression complete.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Compression failed: {e}")

def extract_zip():
    zip_path = input("Enter ZIP file path: ").strip()
    if not os.path.isfile(zip_path) or not zip_path.endswith('.zip'):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid ZIP file.")
        return
    dest = input("Enter extraction folder (default current): ").strip() or "."
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(dest)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Extraction complete.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Extraction failed: {e}")

def calculate_file_hash():
    file_path = input("Enter file path: ").strip()
    if not os.path.isfile(file_path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file.")
        return
        
    print("\n[INFO] Calculating hashes...")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            print(f"MD5:    {hashlib.md5(data).hexdigest()}")
            print(f"SHA1:   {hashlib.sha1(data).hexdigest()}")
            print(f"SHA256: {hashlib.sha256(data).hexdigest()}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not read file: {e}")

def shred_file(path):
    if not os.path.isfile(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File does not exist: {path}")
        return
    try:
        size = os.path.getsize(path)
        print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Shredding {path} ({format_size(size)})...")
        # 3 passes of random data
        with open(path, "ba+", buffering=0) as f:
            for pass_num in range(3):
                print(f"   Pass {pass_num+1}/3 (Overwriting with random bytes)...")
                f.seek(0)
                remaining = size
                while remaining > 0:
                    chunk = min(remaining, 1024 * 1024)
                    f.write(os.urandom(chunk))
                    remaining -= chunk
        
        # Truncate file before deletion
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
            
        os.remove(path)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} File permanently shredded.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Shredding failed: {e}")

def find_duplicates():
    folder = input("Enter folder path to search: ").strip()
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

def change_file_timestamps():
    print(f"\n{Colors.CYAN}--- Change File Timestamps ---{Colors.RESET}")
    path = input("Enter file path: ").strip().replace('"', '')
    if not os.path.exists(path):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} File does not exist.")
        return
        
    print("\nFormat: YYYY-MM-DD HH:MM:SS (e.g. 2026-07-11 17:00:00)")
    created = input("Enter New Creation Date/Time (press Enter to skip): ").strip()
    modified = input("Enter New Modification Date/Time (press Enter to skip): ").strip()
    accessed = input("Enter New Last Access Date/Time (press Enter to skip): ").strip()
    
    commands = []
    if created:
        commands.append(f'$(Get-Item "{path}").CreationTime = "{created}"')
    if modified:
        commands.append(f'$(Get-Item "{path}").LastWriteTime = "{modified}"')
    if accessed:
        commands.append(f'$(Get-Item "{path}").LastAccessTime = "{accessed}"')
        
    if not commands:
        print("[INFO] No changes specified.")
        return
        
    ps_cmd = "; ".join(commands)
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, errors="ignore")
        if res.returncode == 0:
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} File timestamps updated successfully.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to update timestamps: {res.stderr}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Command execution failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [6] FILE & FOLDER{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Hide File")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Unhide File")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Hide Folder")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Unhide Folder")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Secure Folder")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Unlock Folder")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Encrypt Folder")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Decrypt Folder")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Find Large Files")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Duplicate Finder")
        print(f"{Colors.GREEN}[11]{Colors.RESET} Folder Size")
        print(f"{Colors.GREEN}[12]{Colors.RESET} Rename Multiple Files")
        print(f"{Colors.GREEN}[13]{Colors.RESET} Compress (ZIP)")
        print(f"{Colors.GREEN}[14]{Colors.RESET} Extract (ZIP)")
        print(f"{Colors.GREEN}[15]{Colors.RESET} File Hash")
        print(f"{Colors.GREEN}[16]{Colors.RESET} Secure Delete")
        print(f"{Colors.GREEN}[17]{Colors.RESET} Change File Timestamps")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            path = input("Enter file path to hide: ").strip()
            if path: set_hidden(path, True)
        elif choice == '2':
            path = input("Enter file path to unhide: ").strip()
            if path: set_hidden(path, False)
        elif choice == '3':
            path = input("Enter folder path to hide: ").strip()
            if path: set_hidden(path, True)
        elif choice == '4':
            path = input("Enter folder path to unhide: ").strip()
            if path: set_hidden(path, False)
        elif choice == '5':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Secure Folder (Password Protection) coming soon...")
        elif choice == '6':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Unlock Folder coming soon...")
        elif choice == '7':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Encrypt Folder coming soon...")
        elif choice == '8':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Decrypt Folder coming soon...")
        elif choice == '9':
            find_large_files()
        elif choice == '10':
            find_duplicates()
        elif choice == '11':
            calculate_folder_size()
        elif choice == '12':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Mass Renamer coming soon...")
        elif choice == '13':
            compress_folder()
        elif choice == '14':
            extract_zip()
        elif choice == '15':
            calculate_file_hash()
        elif choice == '16':
            path = input("Enter file path to secure delete (SHRED): ").strip()
            if path:
                confirm = input(f"[WARNING] Are you sure you want to permanently shred {path}? (y/n): ").strip().lower()
                if confirm == 'y':
                    shred_file(path)
        elif choice == '17':
            change_file_timestamps()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
