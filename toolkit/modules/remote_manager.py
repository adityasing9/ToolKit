from toolkit.utils import Colors
import os
import sys
import json
import socket
import hashlib
import hmac
import base64
import time
from cryptography.fernet import Fernet

REMOTE_CONFIG = os.path.expanduser(r"~\.toolkit_remote_devices.json")
CLIENT_ID_FILE = os.path.expanduser(r"~\.toolkit_client_id.json")

def get_client_id():
    """Retrieve or generate a static client UUID for secure handshakes."""
    if os.path.exists(CLIENT_ID_FILE):
        try:
            with open(CLIENT_ID_FILE, "r") as f:
                return json.load(f)["client_id"]
        except Exception:
            pass
    import uuid
    client_id = str(uuid.uuid4())
    try:
        with open(CLIENT_ID_FILE, "w") as f:
            json.dump({"client_id": client_id}, f)
    except Exception:
        pass
    return client_id

def load_remote_devices():
    if os.path.exists(REMOTE_CONFIG):
        try:
            with open(REMOTE_CONFIG, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_remote_devices(devices):
    try:
        with open(REMOTE_CONFIG, "w") as f:
            json.dump(devices, f, indent=4)
    except Exception:
        pass

def base64_pair_key(pair_code):
    hasher = hashlib.sha256()
    hasher.update(pair_code.encode("utf-8"))
    return base64.urlsafe_b64encode(hasher.digest())

def pair_device(ip, pair_code, alias=None):
    print(f"\n{Colors.CYAN}--- Pairing Remote Device ({ip}) ---{Colors.RESET}")
    client_id = get_client_id()
    
    # Calculate HMAC signature using pairing code
    signature = hmac.new(pair_code.encode("utf-8"), client_id.encode("utf-8"), hashlib.sha256).hexdigest()
    
    payload = {
        "client_id": client_id,
        "action": "pair",
        "signature": signature
    }
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(6.0)
    try:
        client.connect((ip, 5555))
        client.send(json.dumps(payload).encode("utf-8"))
        
        # Read handshake response
        raw_res = client.recv(4096).decode("utf-8")
        res = json.loads(raw_res)
        
        if res.get("status") == "paired":
            # Decrypt symmetric Fernet session key
            derived_key = base64_pair_key(pair_code)
            f_temp = Fernet(derived_key)
            shared_key = f_temp.decrypt(res["session_key_enc"].encode("utf-8")).decode("utf-8")
            
            # Save trusted device
            devices = load_remote_devices()
            dev_alias = alias if alias else f"Device_{ip.replace('.', '_')}"
            devices[dev_alias] = {
                "ip": ip,
                "shared_key": shared_key
            }
            save_remote_devices(devices)
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Device successfully paired under alias '{dev_alias}'!")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Pairing denied: {res.get('message')}")
    except socket.timeout:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Connection timed out. Is the Remote Agent running on {ip}?")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Pairing failed: {e}")
    finally:
        client.close()

def list_devices():
    devices = load_remote_devices()
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Trusted Remote Devices ({len(devices)}) ==={Colors.RESET}")
    if not devices:
        print("  No paired devices found. Run 'remote pair <IP> <code-code>' to pair.")
        return
        
    print(f"{'Alias':<20} | {'IP Address':<20}")
    print("-" * 45)
    for alias, info in devices.items():
        print(f"{alias:<20} | {info['ip']:<20}")
    print("-" * 45)

def remove_device(alias):
    devices = load_remote_devices()
    if alias in devices:
        del devices[alias]
        save_remote_devices(devices)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Device '{alias}' removed.")
    else:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Alias '{alias}' not found in trusted devices.")

def execute_remote_payload(client, f_cipher, payload):
    """Utility to encrypt payload, send, receive, and decrypt response."""
    try:
        enc_payload = f_cipher.encrypt(json.dumps(payload).encode("utf-8"))
        client.send(enc_payload)
        
        # Read response
        raw_res = client.recv(1024 * 1024)
        if not raw_res:
            return {"status": "error", "message": "Connection closed by remote host."}
            
        decrypted = f_cipher.decrypt(raw_res).decode("utf-8")
        return json.loads(decrypted)
    except Exception as e:
        return {"status": "error", "message": f"Data exchange failed: {e}"}

def run_remote_shell(client, f_cipher, use_powershell=False):
    shell_name = "PowerShell" if use_powershell else "CMD"
    print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Spawning Remote {shell_name} Shell. Type 'exit' to return.")
    
    while True:
        try:
            cmd = input(f"{Colors.GREEN}Remote:{shell_name} > {Colors.RESET}").strip()
            if not cmd:
                continue
            if cmd.lower() in ("exit", "quit"):
                break
                
            payload = {
                "action": "exec_cmd",
                "command": cmd,
                "powershell": use_powershell
            }
            res = execute_remote_payload(client, f_cipher, payload)
            if res.get("status") == "success":
                if res.get("stdout"):
                    print(res["stdout"])
                if res.get("stderr"):
                    print(f"{Colors.RED}{res['stderr']}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Command failed: {res.get('message')}")
        except (KeyboardInterrupt, EOFError):
            break

def run_remote_processes(client, f_cipher):
    print("\n[INFO] Loading remote processes...")
    res = execute_remote_payload(client, f_cipher, {"action": "process", "op": "list"})
    if res.get("status") != "success":
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed: {res.get('message')}")
        return
        
    processes = res.get("processes", [])
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Active Remote Processes (Top 35) ==={Colors.RESET}")
    print(f"{'PID':<8} | {'Process Name':<30} | {'CPU %':<8} | {'RAM (MB)':<10}")
    print("-" * 65)
    processes.sort(key=lambda x: x["ram_mb"], reverse=True)
    for p in processes[:35]:
        print(f"{p['pid']:<8} | {p['name'][:30]:<30} | {p['cpu']:<8.1f} | {p['ram_mb']:<10.1f}")
    print("-" * 65)
    
    pid_kill = input("\nEnter PID to terminate (leave blank to return): ").strip()
    if pid_kill.isdigit():
        kill_res = execute_remote_payload(client, f_cipher, {"action": "process", "op": "kill", "pid": int(pid_kill)})
        if kill_res.get("status") == "success":
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Terminated remote process {pid_kill}.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Kill failed: {kill_res.get('message')}")

def run_remote_files(client, f_cipher):
    cwd = "."
    while True:
        print(f"\n{Colors.CYAN}--- Remote File Browser (CWD: {cwd}) ---{Colors.RESET}")
        res = execute_remote_payload(client, f_cipher, {"action": "file_manager", "op": "list", "path": cwd})
        if res.get("status") != "success":
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not list: {res.get('message')}")
            break
            
        items = res.get("items", [])
        cwd = res.get("cwd", ".")
        
        # Sort folders first
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        
        print(f"{'Type':<8} | {'Name':<35} | {'Size (Bytes)':<12}")
        print("-" * 60)
        for i in items[:30]:
            ftype = "Folder" if i["is_dir"] else "File"
            print(f"{ftype:<8} | {i['name'][:35]:<35} | {i['size']:<12}")
        print("-" * 60)
        if len(items) > 30:
            print(f"  ... and {len(items) - 30} more items.")
            
        print("\nCommands: cd <dir> | download <file> | mkdir <name> | back | exit")
        action = input(f"{Colors.MAGENTA}Browse Select > {Colors.RESET}").strip()
        if not action:
            continue
        if action.lower() == "exit":
            break
        elif action.lower() == "back":
            cwd = os.path.dirname(cwd)
        elif action.startswith("cd "):
            target = action[3:].strip()
            cwd = os.path.join(cwd, target)
        elif action.startswith("mkdir "):
            target = action[6:].strip()
            mkdir_res = execute_remote_payload(client, f_cipher, {"action": "file_manager", "op": "mkdir", "path": os.path.join(cwd, target)})
            print(mkdir_res.get("message"))
        elif action.startswith("download "):
            target = action[9:].strip()
            target_path = os.path.join(cwd, target)
            print(f"[INFO] Downloading {target_path}...")
            dl_res = execute_remote_payload(client, f_cipher, {"action": "file_manager", "op": "download", "path": target_path})
            if dl_res.get("status") == "success":
                import base64
                file_bytes = base64.b64decode(dl_res["file_data"])
                local_dest = input(f"Enter local save filename (default: {target}): ").strip()
                if not local_dest: local_dest = target
                try:
                    with open(local_dest, "wb") as f:
                        f.write(file_bytes)
                    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} File downloaded to {os.path.abspath(local_dest)}")
                except Exception as e:
                    print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to write file locally: {e}")
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Download failed: {dl_res.get('message')}")

def run_remote_services(client, f_cipher):
    print("\n[INFO] Loading remote Windows services...")
    res = execute_remote_payload(client, f_cipher, {"action": "services", "op": "list"})
    if res.get("status") != "success":
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed: {res.get('message')}")
        return
        
    services = res.get("services", [])
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Windows Services ({len(services)}) ==={Colors.RESET}")
    print(f"{'Service Name':<25} | {'Display Name':<35} | {'Status':<10}")
    print("-" * 75)
    for s in services[:35]:
        print(f"{s['name'][:25]:<25} | {s['display'][:35]:<35} | {s['status']:<10}")
    print("-" * 75)
    
    choice = input("\nEnter service name to control (leave blank to return): ").strip()
    if choice:
        op = input("Enter action (start/stop/restart): ").strip().lower()
        if op in ("start", "stop", "restart"):
            ctrl_res = execute_remote_payload(client, f_cipher, {"action": "services", "op": op, "name": choice})
            print(ctrl_res.get("message"))

def connect_device(alias):
    devices = load_remote_devices()
    if alias not in devices:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Alias '{alias}' not registered. Run 'remote pair <IP>' first.")
        return
        
    device = devices[alias]
    ip = device["ip"]
    shared_key = device["shared_key"]
    client_id = get_client_id()
    
    print(f"\n[INFO] Connecting to remote host {ip} ({alias})...")
    
    # Connection Handshake authentication
    timestamp = str(int(time.time()))
    signature = hmac.new(shared_key.encode("utf-8"), f"{client_id}:{timestamp}".encode("utf-8"), hashlib.sha256).hexdigest()
    
    payload = {
        "client_id": client_id,
        "action": "connect",
        "signature": signature,
        "timestamp": timestamp
    }
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(6.0)
    try:
        client.connect((ip, 5555))
        client.send(json.dumps(payload).encode("utf-8"))
        
        # Read handshake response
        raw_res = client.recv(4096).decode("utf-8")
        res = json.loads(raw_res)
        
        if res.get("status") == "authenticated":
            print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Secure connection established via E2E Fernet encryption.")
            
            f_cipher = Fernet(shared_key.encode("utf-8"))
            
            # Connection Control Menu
            while True:
                print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.YELLOW}              💻 REMOTE MANAGEMENT: {alias.upper()}{Colors.RESET}")
                print(f"{Colors.CYAN}============================================================={Colors.RESET}")
                print(f"{Colors.GREEN}[1]{Colors.RESET} View System Diagnostics Metrics")
                print(f"{Colors.GREEN}[2]{Colors.RESET} Launch Remote Command Line (CMD)")
                print(f"{Colors.GREEN}[3]{Colors.RESET} Launch Remote PowerShell Shell")
                print(f"{Colors.GREEN}[4]{Colors.RESET} Remote Process Manager")
                print(f"{Colors.GREEN}[5]{Colors.RESET} Remote Services Controller")
                print(f"{Colors.GREEN}[6]{Colors.RESET} Remote File Browser / Downloader")
                print(f"{Colors.GREEN}[7]{Colors.RESET} Remote Power Controls (Restart/Shutdown/Lock)")
                print(f"{Colors.GREEN}[0]{Colors.RESET} Disconnect Session")
                print(f"{Colors.CYAN}============================================================={Colors.RESET}")
                
                choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
                if choice == '0':
                    break
                elif choice == '1':
                    sys_res = execute_remote_payload(client, f_cipher, {"action": "system_info"})
                    if sys_res.get("status") == "success":
                        print(f"\n{Colors.BOLD}{Colors.YELLOW}=== Remote Metrics ==={Colors.RESET}")
                        for k, v in sys_res["metrics"].items():
                            print(f"  {k:<20} : {v}")
                    else:
                        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed: {sys_res.get('message')}")
                    input("\nPress Enter to continue...")
                elif choice == '2':
                    run_remote_shell(client, f_cipher, use_powershell=False)
                elif choice == '3':
                    run_remote_shell(client, f_cipher, use_powershell=True)
                elif choice == '4':
                    run_remote_processes(client, f_cipher)
                    input("\nPress Enter to continue...")
                elif choice == '5':
                    run_remote_services(client, f_cipher)
                    input("\nPress Enter to continue...")
                elif choice == '6':
                    run_remote_files(client, f_cipher)
                elif choice == '7':
                    print("\nPower Commands: lock | sleep | restart | shutdown")
                    pow_op = input("Enter Power Operation: ").strip().lower()
                    if pow_op in ("lock", "sleep", "restart", "shutdown"):
                        confirm = input(f"Confirm remote power operation '{pow_op}'? (y/n): ").strip().lower()
                        if confirm == 'y':
                            pow_res = execute_remote_payload(client, f_cipher, {"action": "power", "op": pow_op})
                            print(pow_res.get("message"))
                            if pow_op in ("restart", "shutdown"):
                                break
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid choice.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Connection denied: {res.get('message')}")
    except socket.timeout:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Socket timed out.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Connection failed: {e}")
    finally:
        client.close()
        print("\nSession disconnected.")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [26] REMOTE DEVICE MANAGER{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Launch Standby Remote Agent Server (Listen)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Pair Remote Computer (Using IP + Pair Code)")
        print(f"{Colors.GREEN}[3]{Colors.RESET} List Trusted Paired Remote Computers")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Connect to Paired Remote Computer")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Remove Paired Remote Computer Credentials")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("\n[INFO] Initializing Remote Agent server on port 5555...")
            from toolkit.modules import remote_agent
            try:
                remote_agent.start_agent_server()
            except Exception as e:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Server error: {e}")
        elif choice == '2':
            ip = input("Enter remote computer IP address: ").strip()
            code = input("Enter 6-digit pairing code shown on remote computer: ").strip()
            alias = input("Enter custom alias name (optional): ").strip()
            pair_device(ip, code, alias if alias else None)
            input("\nPress Enter to continue...")
        elif choice == '3':
            list_devices()
            input("\nPress Enter to continue...")
        elif choice == '4':
            list_devices()
            alias = input("\nEnter remote device alias to connect: ").strip()
            if alias:
                connect_device(alias)
            input("\nPress Enter to continue...")
        elif choice == '5':
            list_devices()
            alias = input("\nEnter remote device alias to remove: ").strip()
            if alias:
                remove_device(alias)
            input("\nPress Enter to continue...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
