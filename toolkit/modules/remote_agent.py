import os
import sys
import json
import time
import socket
import select
import threading
import uuid
import psutil
import subprocess
import ctypes
from cryptography.fernet import Fernet
import hashlib
import hmac

AGENT_CONFIG = os.path.expanduser(r"~\.toolkit_agent_config.json")

def load_or_create_config():
    if os.path.exists(AGENT_CONFIG):
        try:
            with open(AGENT_CONFIG, "r") as f:
                return json.load(f)
        except Exception:
            pass
            
    # Generate new config
    import random
    device_id = str(uuid.uuid4())
    pair_code = f"{random.randint(100000, 999999)}"
    config = {
        "device_id": device_id,
        "pair_code": pair_code,
        "trusted_clients": {} # client_id -> shared_key (str)
    }
    save_config(config)
    return config

def save_config(config):
    try:
        with open(AGENT_CONFIG, "w") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass

def get_system_info():
    """Aggregate detailed remote diagnostics metrics."""
    try:
        uptime = time.time() - psutil.boot_time()
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m"
        
        # CPU & Memory
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        # Disk usage
        disk = psutil.disk_usage("C:\\").percent
        
        # Hostname, IPs
        hostname = socket.gethostname()
        local_ip = "127.0.0.1"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            pass
            
        import requests
        public_ip = "Unknown"
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=2.0).text
        except Exception:
            pass
            
        # Battery (laptop)
        battery_str = "N/A"
        battery = psutil.sensors_battery()
        if battery:
            battery_str = f"{battery.percent}% ({'Charging' if battery.power_plugged else 'Discharging'})"
            
        # OS Version
        import platform
        os_version = f"{platform.system()} {platform.release()} (Build {platform.version()})"
        
        return {
            "status": "success",
            "metrics": {
                "CPU Usage": f"{cpu}%",
                "RAM Usage": f"{ram}%",
                "Disk Usage": f"{disk}%",
                "Uptime": uptime_str,
                "Battery Status": battery_str,
                "Windows Version": os_version,
                "Hostname": hostname,
                "Local IP": local_ip,
                "Public IP": public_ip,
                "Logged-in User": os.getlogin()
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_exec_cmd(cmd, run_in_powershell=False):
    try:
        shell_exe = "powershell.exe" if run_in_powershell else "cmd.exe"
        args = [shell_exe, "/c" if not run_in_powershell else "-Command", cmd]
        res = subprocess.run(args, capture_output=True, text=True, errors="ignore", timeout=15.0)
        return {
            "status": "success",
            "stdout": res.stdout,
            "stderr": res.stderr,
            "returncode": res.returncode
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Command execution timed out."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_file_manager(payload):
    op = payload.get("op")
    path = payload.get("path", "")
    try:
        if op == "list":
            if not path: path = "."
            items = []
            for entry in os.scandir(path):
                stat = entry.stat()
                items.append({
                    "name": entry.name,
                    "is_dir": entry.is_dir(),
                    "size": stat.st_size,
                    "mtime": stat.st_mtime
                })
            return {"status": "success", "items": items, "cwd": os.path.abspath(path)}
        elif op == "download":
            if os.path.exists(path) and os.path.isfile(path):
                import base64
                with open(path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                return {"status": "success", "file_data": data, "filename": os.path.basename(path)}
            return {"status": "error", "message": "File not found or is a directory."}
        elif op == "upload":
            import base64
            file_data = base64.b64decode(payload.get("file_data", ""))
            with open(path, "wb") as f:
                f.write(file_data)
            return {"status": "success", "message": f"File uploaded to {path}."}
        elif op == "delete":
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
            return {"status": "success", "message": f"Deleted {path}."}
        elif op == "rename":
            new_path = payload.get("new_path")
            os.rename(path, new_path)
            return {"status": "success", "message": f"Renamed to {new_path}."}
        elif op == "mkdir":
            os.makedirs(path, exist_ok=True)
            return {"status": "success", "message": f"Created directory {path}."}
        return {"status": "error", "message": "Unsupported file operation."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_power_control(op):
    try:
        if op == "restart":
            subprocess.Popen(["shutdown", "/r", "/t", "0"])
            return {"status": "success", "message": "System restart triggered."}
        elif op == "shutdown":
            subprocess.Popen(["shutdown", "/s", "/t", "0"])
            return {"status": "success", "message": "System shutdown triggered."}
        elif op == "lock":
            ctypes.windll.user32.LockWorkStation()
            return {"status": "success", "message": "Workstation locked."}
        elif op == "sleep":
            # Sleep using powrprof
            ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
            return {"status": "success", "message": "System put to sleep."}
        return {"status": "error", "message": "Unsupported power action."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_process_manager(payload):
    op = payload.get("op")
    try:
        if op == "list":
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    info = proc.info
                    processes.append({
                        "pid": info['pid'],
                        "name": info['name'],
                        "cpu": info['cpu_percent'] or 0.0,
                        "ram_mb": round(info['memory_info'].rss / (1024 * 1024), 1) if info['memory_info'] else 0.0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return {"status": "success", "processes": processes}
        elif op == "kill":
            pid = int(payload.get("pid"))
            proc = psutil.Process(pid)
            proc.kill()
            return {"status": "success", "message": f"Killed process {pid}."}
        return {"status": "error", "message": "Unsupported process operation."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_services_manager(payload):
    op = payload.get("op")
    name = payload.get("name")
    try:
        if op == "list":
            services = []
            for s in psutil.win_service_iter():
                try:
                    services.append({
                        "name": s.name(),
                        "display": s.display_name(),
                        "status": s.status()
                    })
                except Exception:
                    continue
            return {"status": "success", "services": services}
        elif op in ("start", "stop", "restart"):
            # Start/stop service via net cmd
            args = ["net", op, name] if op != "restart" else ["sc", "control", name, "param"] # Simplification
            if op == "restart":
                subprocess.run(["net", "stop", name], capture_output=True)
                res = subprocess.run(["net", "start", name], capture_output=True, text=True)
            else:
                res = subprocess.run(["net", op, name], capture_output=True, text=True)
            return {"status": "success", "message": f"Service operation {op} performed."}
        return {"status": "error", "message": "Unsupported service operation."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_client(conn, addr, config):
    print(f"[INFO] Active socket connection from {addr}")
    session_key = None
    
    try:
        # 1. Handshake Phase
        # Client sends initial JSON hello containing client_id & signature or pair request
        raw_hello = conn.recv(4096).decode("utf-8")
        if not raw_hello:
            return
            
        hello = json.loads(raw_hello)
        client_id = hello.get("client_id")
        action = hello.get("action") # "pair" or "connect"
        
        if action == "pair":
            # Authenticate using pair code via HMAC
            pair_code = config["pair_code"]
            client_sig = hello.get("signature")
            computed_sig = hmac.new(pair_code.encode("utf-8"), client_id.encode("utf-8"), hashlib.sha256).hexdigest()
            
            if hmac.compare_digest(client_sig, computed_sig):
                # Generates and stores new symmetric Fernet key for client
                shared_key = Fernet.generate_key().decode("utf-8")
                config["trusted_clients"][client_id] = shared_key
                save_config(config)
                
                # Send key back encrypted with derived pair code key
                derived_key = base64_pair_key(pair_code)
                f_temp = Fernet(derived_key)
                response = f_temp.encrypt(shared_key.encode("utf-8")).decode("utf-8")
                
                conn.send(json.dumps({"status": "paired", "session_key_enc": response}).encode("utf-8"))
                print(f"[SUCCESS] Successfully paired with client {client_id}")
                return
            else:
                conn.send(json.dumps({"status": "denied", "message": "Invalid pair code."}).encode("utf-8"))
                return
                
        elif action == "connect":
            shared_key = config["trusted_clients"].get(client_id)
            if not shared_key:
                conn.send(json.dumps({"status": "denied", "message": "Device not paired."}).encode("utf-8"))
                return
                
            # Verify signature using client key
            client_sig = hello.get("signature")
            timestamp = hello.get("timestamp", "")
            computed_sig = hmac.new(shared_key.encode("utf-8"), f"{client_id}:{timestamp}".encode("utf-8"), hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(client_sig, computed_sig):
                conn.send(json.dumps({"status": "denied", "message": "Authentication failed."}).encode("utf-8"))
                return
                
            # Valid session
            conn.send(json.dumps({"status": "authenticated"}).encode("utf-8"))
            session_key = shared_key
            
        else:
            conn.send(json.dumps({"status": "denied", "message": "Invalid handshake action."}).encode("utf-8"))
            return
            
        # 2. Encrypted Diagnostics Loop
        f_cipher = Fernet(session_key.encode("utf-8"))
        while True:
            # Read encrypted request
            raw_req = conn.recv(1024 * 1024) # 1MB buffer
            if not raw_req:
                break
                
            # Decrypt request
            decrypted = f_cipher.decrypt(raw_req).decode("utf-8")
            req = json.loads(decrypted)
            action = req.get("action")
            
            # Execute request
            if action == "system_info":
                res_payload = get_system_info()
            elif action == "exec_cmd":
                res_payload = handle_exec_cmd(req.get("command"), req.get("powershell", False))
            elif action == "file_manager":
                res_payload = handle_file_manager(req)
            elif action == "process":
                res_payload = handle_process_manager(req)
            elif action == "services":
                res_payload = handle_services_manager(req)
            elif action == "power":
                res_payload = handle_power_control(req.get("op"))
            else:
                res_payload = {"status": "error", "message": f"Unsupported action: {action}"}
                
            # Encrypt & return response
            enc_res = f_cipher.encrypt(json.dumps(res_payload).encode("utf-8"))
            conn.send(enc_res)
            
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"[INFO] Socket closed for {addr}")

def base64_pair_key(pair_code):
    """Generate a valid 32-byte urlsafe base64 Fernet key using pair code."""
    import base64
    hasher = hashlib.sha256()
    hasher.update(pair_code.encode("utf-8"))
    key_bytes = hasher.digest()
    return base64.urlsafe_b64encode(key_bytes)

def start_agent_server(port=5555):
    config = load_or_create_config()
    print(f"\n{Colors.BOLD}{Colors.YELLOW}============================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}              ⚡ TOOLKIT REMOTE MANAGEMENT AGENT{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}============================================================={Colors.RESET}")
    print(f"  Device ID: {Colors.CYAN}{config['device_id']}{Colors.RESET}")
    print(f"  Pair Code: {Colors.CYAN}{config['pair_code']}{Colors.RESET}")
    print(f"  Port     : {Colors.GREEN}{port}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}============================================================={Colors.RESET}")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", port))
        server.listen(10)
        print("[INFO] Remote Agent actively listening for pairing or connections...")
        
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, config), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[INFO] Agent server shutting down.")
    except Exception as e:
        print(f"[FATAL] Server socket failed: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_agent_server()
