from toolkit.utils import Colors
import os
import sys
import time
import json
import socket
import datetime
import subprocess
import urllib.request
import psutil

def _run_ps_json(script_body):
    """Executes a PowerShell script block and safely parses JSON output."""
    wrapper = f"$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8; {script_body}"
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", wrapper],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=8
        )
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout.strip())
    except Exception:
        pass
    return None

def _format_size(num_bytes):
    if not num_bytes or num_bytes <= 0:
        return "0 B"
    factor = 1024
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if num_bytes < factor:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= factor
    return f"{num_bytes:.2f} EB"

def _render_bar(percent, width=20, color=Colors.GREEN):
    clamped = max(0.0, min(100.0, float(percent)))
    filled = int((clamped / 100.0) * width)
    unfilled = width - filled
    if clamped > 85:
        bar_color = Colors.RED
    elif clamped > 60:
        bar_color = Colors.YELLOW
    else:
        bar_color = color
    return f"[{bar_color}{'█' * filled}{Colors.RESET}{'-' * unfilled}] {clamped:5.1f}%"

def gather_deep_system_info():
    """Gathers comprehensive deep diagnostic data across hardware, firmware, OS, and security."""
    data = {}

    # 1. OS & Machine Identity via psutil + platform
    data['hostname'] = socket.gethostname()
    data['user'] = os.environ.get('USERNAME', 'N/A')
    data['platform'] = sys.platform
    boot_time = psutil.boot_time()
    data['uptime_seconds'] = int(time.time() - boot_time)
    data['boot_time'] = datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
    uptime_delta = datetime.timedelta(seconds=data['uptime_seconds'])
    data['uptime_str'] = f"{uptime_delta.days}d {uptime_delta.seconds // 3600}h {(uptime_delta.seconds % 3600) // 60}m"

    # CPU Realtime via psutil
    data['cpu_count_phys'] = psutil.cpu_count(logical=False) or 0
    data['cpu_count_log'] = psutil.cpu_count(logical=True) or 0
    data['cpu_percent_overall'] = psutil.cpu_percent(interval=0.3)
    data['cpu_percent_percore'] = psutil.cpu_percent(interval=0.1, percpu=True)
    cpufreq = psutil.cpu_freq()
    data['cpu_freq_current'] = cpufreq.current if cpufreq else 0.0
    data['cpu_freq_max'] = cpufreq.max if cpufreq else 0.0

    # RAM Realtime via psutil
    vmem = psutil.virtual_memory()
    data['ram_total'] = vmem.total
    data['ram_available'] = vmem.available
    data['ram_used'] = vmem.used
    data['ram_percent'] = vmem.percent
    swap = psutil.swap_memory()
    data['swap_total'] = swap.total
    data['swap_used'] = swap.used
    data['swap_percent'] = swap.percent

    # Disks Realtime via psutil
    partitions_data = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions_data.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except Exception:
            pass
    data['partitions'] = partitions_data

    # Top Processes
    top_cpu_procs = []
    top_ram_procs = []
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                procs.append(p.info)
            except Exception:
                pass
        top_cpu_procs = sorted(procs, key=lambda x: x.get('cpu_percent') or 0.0, reverse=True)[:5]
        top_ram_procs = sorted(procs, key=lambda x: (x.get('memory_info').rss if x.get('memory_info') else 0), reverse=True)[:5]
    except Exception:
        pass
    data['top_cpu_procs'] = top_cpu_procs
    data['top_ram_procs'] = top_ram_procs

    # Public IP lookup (quick timeout 1.5s)
    try:
        req = urllib.request.Request("https://api.ipify.org?format=json", headers={"User-Agent": "Toolkit/1.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            ip_obj = json.loads(resp.read().decode())
            data['public_ip'] = ip_obj.get("ip", "Offline")
    except Exception:
        data['public_ip'] = "Offline / Unreachable"

    # Batch Hardware & Firmware Query via PowerShell CIM
    ps_query = """
    $out = @{}
    try { $out.os = Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture, LastBootUpTime, InstallDate } catch {}
    try { $out.cpu = Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed, L3CacheSize, SocketDesignation, Architecture } catch {}
    try { $out.ram = @(Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer, PartNumber, Capacity, Speed, FormFactor, DeviceLocator) } catch {}
    try { $out.board = Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, SerialNumber } catch {}
    try { $out.bios = Get-CimInstance Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate } catch {}
    try { $out.gpu = @(Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion, AdapterRAM, VideoModeDescription, CurrentRefreshRate) } catch {}
    try { $out.disks = @(Get-CimInstance Win32_DiskDrive | Select-Object Model, InterfaceType, MediaType, Size, Status, Partitions) } catch {}
    try { $out.net = @(Get-NetAdapter | Where-Object Status -eq 'Up' | Select-Object Name, InterfaceDescription, MacAddress, LinkSpeed) } catch {}
    try { 
        $tpm = Get-Tpm
        $out.tpm = @{ Present = $tpm.TpmPresent; Ready = $tpm.TpmReady; Enabled = $tpm.TpmEnabled }
    } catch { $out.tpm = @{ Present = $false } }
    try {
        $secBoot = Confirm-SecureBootUEFI
        $out.secure_boot = $secBoot
    } catch { $out.secure_boot = "Not Supported / Disabled" }
    try {
        $battery = Get-CimInstance Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus, DesignCapacity, FullChargeCapacity
        if ($battery) { $out.battery = $battery }
    } catch {}
    $out | ConvertTo-Json -Depth 4
    """
    cim_data = _run_ps_json(ps_query)
    data['cim'] = cim_data or {}

    return data

def render_terminal_report(data):
    """Renders the comprehensive, color-coded deep system report in the terminal."""
    W = 86
    sep = f"{Colors.CYAN}{'=' * W}{Colors.RESET}"
    sec_sep = f"{Colors.BLUE}{'─' * W}{Colors.RESET}"

    print(sep)
    print(f"{Colors.BOLD}{Colors.YELLOW}{'🔍 COMPREHENSIVE DEEP SYSTEM & HARDWARE INSPECTION'.center(W)}{Colors.RESET}")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host_str = data.get("hostname", "Localhost")
    user_str = data.get("user", "User")
    sub_title = f"Report Generated: {now_str} | Target: {host_str} ({user_str})"
    print(f"{Colors.CYAN}{sub_title.center(W)}{Colors.RESET}")
    print(sep)

    # 1. OS & Platform
    cim = data.get('cim', {})
    os_info = cim.get('os') or {}
    print(f"\n{Colors.BOLD}{Colors.CYAN}🖥️  OPERATING SYSTEM & SYSTEM IDENTITY{Colors.RESET}")
    print(sec_sep)
    os_name = os_info.get('Caption') or "Microsoft Windows"
    os_build = f"{os_info.get('Version', '')} (Build {os_info.get('BuildNumber', '')})"
    os_arch = os_info.get('OSArchitecture', '64-bit')
    print(f"  {Colors.BOLD}Operating System :{Colors.RESET} {Colors.GREEN}{os_name}{Colors.RESET} ({os_arch})")
    print(f"  {Colors.BOLD}Kernel & Build   :{Colors.RESET} {os_build}")
    print(f"  {Colors.BOLD}Host / User      :{Colors.RESET} {data.get('hostname')} / {data.get('user')}")
    print(f"  {Colors.BOLD}System Uptime    :{Colors.RESET} {Colors.YELLOW}{data.get('uptime_str')}{Colors.RESET} (Booted: {data.get('boot_time')})")
    print(f"  {Colors.BOLD}Secure Boot      :{Colors.RESET} {cim.get('secure_boot', 'Unknown')}")
    tpm = cim.get('tpm') or {}
    tpm_status = f"{Colors.GREEN}Active / Ready{Colors.RESET}" if tpm.get('Ready') else f"{Colors.YELLOW}Not Present or Disabled{Colors.RESET}"
    print(f"  {Colors.BOLD}TPM 2.0 Security :{Colors.RESET} {tpm_status}")

    # 2. Motherboard & BIOS
    board = cim.get('board') or {}
    bios = cim.get('bios') or {}
    print(f"\n{Colors.BOLD}{Colors.CYAN}🧩  MOTHERBOARD & FIRMWARE (BIOS){Colors.RESET}")
    print(sec_sep)
    print(f"  {Colors.BOLD}Board Vendor     :{Colors.RESET} {board.get('Manufacturer', 'N/A')}")
    print(f"  {Colors.BOLD}Board Model      :{Colors.RESET} {board.get('Product', 'N/A')}")
    print(f"  {Colors.BOLD}Serial Number    :{Colors.RESET} {board.get('SerialNumber', 'N/A')}")
    print(f"  {Colors.BOLD}BIOS Vendor/Ver  :{Colors.RESET} {bios.get('Manufacturer', 'N/A')} - {Colors.YELLOW}{bios.get('SMBIOSBIOSVersion', 'N/A')}{Colors.RESET}")

    # 3. CPU In-Depth
    cpu_info = cim.get('cpu') or {}
    cpu_name = cpu_info.get('Name', '').strip() or "Processor"
    print(f"\n{Colors.BOLD}{Colors.CYAN}⚡  PROCESSOR (CPU) DEEP SPECIFICATIONS{Colors.RESET}")
    print(sec_sep)
    print(f"  {Colors.BOLD}Processor Name   :{Colors.RESET} {Colors.GREEN}{cpu_name}{Colors.RESET}")
    p_cores = data.get('cpu_count_phys', 0)
    l_cores = data.get('cpu_count_log', 0)
    print(f"  {Colors.BOLD}Cores & Threads  :{Colors.RESET} {p_cores} Physical Cores | {l_cores} Logical Processors (Threads)")
    max_clk = cpu_info.get('MaxClockSpeed') or data.get('cpu_freq_max')
    cur_clk = data.get('cpu_freq_current')
    l3_cache = cpu_info.get('L3CacheSize')
    l3_str = f"{l3_cache // 1024} MB ({l3_cache} KB)" if l3_cache else "N/A"
    print(f"  {Colors.BOLD}Clock Frequencies:{Colors.RESET} Current: {cur_clk:.1f} MHz | Base/Max: {max_clk} MHz")
    print(f"  {Colors.BOLD}L3 Smart Cache   :{Colors.RESET} {l3_str}")
    overall_cpu = data.get('cpu_percent_overall', 0.0)
    print(f"  {Colors.BOLD}Overall CPU Load :{Colors.RESET} {_render_bar(overall_cpu, width=28, color=Colors.CYAN)}")

    percore = data.get('cpu_percent_percore', [])
    if percore:
        print(f"  {Colors.BOLD}Per-Core Load    :{Colors.RESET}")
        for idx in range(0, len(percore), 2):
            c1_text = f"Core {idx:02d}: {_render_bar(percore[idx], width=12)}"
            c2_text = ""
            if idx + 1 < len(percore):
                c2_text = f"  Core {idx+1:02d}: {_render_bar(percore[idx+1], width=12)}"
            print(f"    {c1_text}{c2_text}")

    # 4. RAM In-Depth
    ram_total = data.get('ram_total', 0)
    ram_used = data.get('ram_used', 0)
    ram_avail = data.get('ram_available', 0)
    ram_pct = data.get('ram_percent', 0.0)
    print(f"\n{Colors.BOLD}{Colors.CYAN}🧠  MEMORY (RAM) SLOTS & TOPOLOGY{Colors.RESET}")
    print(sec_sep)
    print(f"  {Colors.BOLD}Installed RAM    :{Colors.RESET} {_format_size(ram_total)} Total | {_format_size(ram_used)} Used | {_format_size(ram_avail)} Available")
    print(f"  {Colors.BOLD}RAM Utilization  :{Colors.RESET} {_render_bar(ram_pct, width=28)}")
    swap_total = data.get('swap_total', 0)
    swap_used = data.get('swap_used', 0)
    swap_pct = data.get('swap_percent', 0.0)
    print(f"  {Colors.BOLD}Virtual Pagefile :{Colors.RESET} {_format_size(swap_total)} Total ({_format_size(swap_used)} used) {_render_bar(swap_pct, width=16)}")

    ram_slots = cim.get('ram') or []
    if isinstance(ram_slots, dict):
        ram_slots = [ram_slots]
    if ram_slots:
        print(f"  {Colors.BOLD}Physical Modules :{Colors.RESET}")
        for i, slot in enumerate(ram_slots, 1):
            s_cap = _format_size(slot.get('Capacity', 0))
            s_mfg = (slot.get('Manufacturer') or 'OEM').strip()
            s_spd = slot.get('Speed') or 'N/A'
            s_part = (slot.get('PartNumber') or 'N/A').strip()
            loc = slot.get('DeviceLocator') or f"Slot {i}"
            print(f"    • {Colors.YELLOW}[{loc}]{Colors.RESET} {s_mfg} {s_cap} @ {s_spd} MHz (Part: {s_part})")

    # 5. Graphics & Displays
    gpus = cim.get('gpu') or []
    if isinstance(gpus, dict):
        gpus = [gpus]
    print(f"\n{Colors.BOLD}{Colors.CYAN}🎮  GRAPHICS (GPU) & DISPLAY OUTPUTS{Colors.RESET}")
    print(sec_sep)
    if not gpus:
        print("  No discrete or integrated GPU returned.")
    else:
        for i, g in enumerate(gpus, 1):
            g_name = g.get('Name', 'Unknown GPU')
            g_drv = g.get('DriverVersion', 'N/A')
            g_vram = _format_size(g.get('AdapterRAM', 0))
            g_mode = g.get('VideoModeDescription') or 'Display Mode N/A'
            g_ref = g.get('CurrentRefreshRate')
            ref_str = f" @ {g_ref} Hz" if g_ref else ""
            print(f"  {Colors.BOLD}GPU #{i}           :{Colors.RESET} {Colors.GREEN}{g_name}{Colors.RESET}")
            print(f"    Driver Version : {g_drv} | VRAM: {g_vram}")
            print(f"    Display Mode   : {g_mode}{ref_str}")

    # 6. Physical Disks & Volumes
    disks = cim.get('disks') or []
    if isinstance(disks, dict):
        disks = [disks]
    print(f"\n{Colors.BOLD}{Colors.CYAN}💾  STORAGE DRIVES & PARTITIONS{Colors.RESET}")
    print(sec_sep)
    if disks:
        print(f"  {Colors.BOLD}Physical Disks   :{Colors.RESET}")
        for i, d in enumerate(disks, 1):
            d_model = d.get('Model', 'Disk Drive')
            d_size = _format_size(d.get('Size', 0))
            d_media = d.get('MediaType', 'Fixed Drive')
            d_stat = d.get('Status', 'OK')
            stat_color = Colors.GREEN if d_stat.upper() == 'OK' else Colors.RED
            print(f"    • Disk #{i}: {Colors.YELLOW}{d_model}{Colors.RESET} ({d_size}) - S.M.A.R.T: {stat_color}{d_stat}{Colors.RESET} [{d_media}]")

    parts = data.get('partitions', [])
    if parts:
        print(f"  {Colors.BOLD}Logical Volumes  :{Colors.RESET}")
        for p in parts:
            p_tot = _format_size(p['total'])
            p_free = _format_size(p['free'])
            print(f"    • {Colors.BOLD}{p['device']}{Colors.RESET} ({p['fstype']}) {p_tot} Total | Free: {p_free} {_render_bar(p['percent'], width=18)}")

    # 7. Network & Connectivity
    net_adapters = cim.get('net') or []
    if isinstance(net_adapters, dict):
        net_adapters = [net_adapters]
    print(f"\n{Colors.BOLD}{Colors.CYAN}🌐  NETWORK INTERFACES & CONNECTIVITY{Colors.RESET}")
    print(sec_sep)
    print(f"  {Colors.BOLD}Public IPv4      :{Colors.RESET} {Colors.GREEN}{data.get('public_ip')}{Colors.RESET}")
    if net_adapters:
        print(f"  {Colors.BOLD}Active Adapters  :{Colors.RESET}")
        for n in net_adapters:
            n_name = n.get('Name', 'Interface')
            n_desc = n.get('InterfaceDescription', '')
            n_mac = n.get('MacAddress', 'N/A')
            n_speed = n.get('LinkSpeed', 'N/A')
            print(f"    • {Colors.YELLOW}{n_name}{Colors.RESET} ({n_desc})")
            print(f"      MAC: {n_mac} | Link Speed: {n_speed}")

    # 8. Battery Health (if present)
    bat = cim.get('battery')
    if bat:
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔋  BATTERY HEALTH & POWER{Colors.RESET}")
        print(sec_sep)
        pct = bat.get('EstimatedChargeRemaining', 'N/A')
        stat = bat.get('BatteryStatus', 'N/A')
        des_cap = bat.get('DesignCapacity')
        full_cap = bat.get('FullChargeCapacity')
        wear_str = ""
        if des_cap and full_cap and des_cap > 0:
            health_pct = (full_cap / des_cap) * 100
            wear_str = f" | Health: {health_pct:.1f}% (Full: {full_cap} mWh / Design: {des_cap} mWh)"
        print(f"  {Colors.BOLD}Charge Status    :{Colors.RESET} {pct}% [Status Code: {stat}]{wear_str}")

    # 9. Top Resource Consumers
    top_cpu = data.get('top_cpu_procs', [])
    top_ram = data.get('top_ram_procs', [])
    print(f"\n{Colors.BOLD}{Colors.CYAN}📊  LIVE TOP RESOURCE CONSUMERS{Colors.RESET}")
    print(sec_sep)
    print(f"  {Colors.BOLD}Top CPU Consumers :{Colors.RESET}")
    for p in top_cpu:
        p_name = p.get('name', 'N/A')[:20]
        p_cpu = p.get('cpu_percent', 0.0)
        p_pid = p.get('pid', 0)
        print(f"    PID {p_pid:<6} | {p_name:<20} | CPU: {p_cpu:5.1f}%")

    print(f"  {Colors.BOLD}Top RAM Consumers :{Colors.RESET}")
    for p in top_ram:
        p_name = p.get('name', 'N/A')[:20]
        mem_bytes = p.get('memory_info').rss if p.get('memory_info') else 0
        p_pid = p.get('pid', 0)
        print(f"    PID {p_pid:<6} | {p_name:<20} | RAM: {_format_size(mem_bytes)}")

    print(f"\n{sep}\n")

def export_report_txt(data, filepath="deep_system_report.txt"):
    """Exports plain-text inspection report to file."""
    import re
    # Strip ANSI colors
    ansi_regex = re.compile(r'\x1b\[[0-9;]*m')
    import io
    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        render_terminal_report(data)
    finally:
        sys.stdout = old_stdout
    
    clean_text = ansi_regex.sub('', buf.getvalue())
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_text)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Report exported to: {os.path.abspath(filepath)}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to export text report: {e}")

def export_report_html(data, filepath="deep_system_report.html"):
    """Exports clean dark-mode HTML hardware report to file."""
    cim = data.get('cim', {})
    os_info = cim.get('os') or {}
    cpu_info = cim.get('cpu') or {}
    board = cim.get('board') or {}
    bios = cim.get('bios') or {}
    gpus = cim.get('gpu') or []
    if isinstance(gpus, dict): gpus = [gpus]
    disks = cim.get('disks') or []
    if isinstance(disks, dict): disks = [disks]
    net_adapters = cim.get('net') or []
    if isinstance(net_adapters, dict): net_adapters = [net_adapters]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Deep System Inspection - {data.get('hostname')}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; margin: 0; }}
  .container {{ max-width: 1000px; margin: 0 auto; background: #1e293b; padding: 35px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
  h1 {{ color: #38bdf8; margin-top: 0; border-bottom: 2px solid #334155; padding-bottom: 12px; }}
  h2 {{ color: #a855f7; border-bottom: 1px solid #334155; padding-bottom: 6px; margin-top: 25px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 10px; }}
  .card {{ background: #0f172a; padding: 15px; border-radius: 8px; border-left: 4px solid #38bdf8; }}
  .label {{ color: #94a3b8; font-size: 0.85em; text-transform: uppercase; font-weight: bold; }}
  .val {{ font-size: 1.1em; color: #f1f5f9; margin-top: 4px; }}
  .bar-bg {{ background: #334155; height: 12px; border-radius: 6px; overflow: hidden; margin-top: 6px; }}
  .bar-fill {{ background: #22c55e; height: 100%; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  th, td {{ text-align: left; padding: 8px 12px; border-bottom: 1px solid #334155; }}
  th {{ background: #0f172a; color: #38bdf8; }}
  .footer {{ margin-top: 30px; text-align: center; color: #64748b; font-size: 0.85em; }}
</style>
</head>
<body>
<div class="container">
  <h1>⚡ Deep System & Hardware Inspection Report</h1>
  <p style="color: #94a3b8;">Host: <strong>{data.get('hostname')}</strong> | Generated: <strong>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
  
  <h2>🖥️ Operating System & Identity</h2>
  <div class="grid">
    <div class="card"><div class="label">OS Caption</div><div class="val">{os_info.get('Caption', 'Windows')} ({os_info.get('OSArchitecture', '64-bit')})</div></div>
    <div class="card"><div class="label">Version / Build</div><div class="val">{os_info.get('Version', '')} (Build {os_info.get('BuildNumber', '')})</div></div>
    <div class="card"><div class="label">System Uptime</div><div class="val">{data.get('uptime_str')} (Boot: {data.get('boot_time')})</div></div>
    <div class="card"><div class="label">Secure Boot / TPM</div><div class="val">Secure Boot: {cim.get('secure_boot', 'N/A')} | TPM Ready: {cim.get('tpm', {}).get('Ready', False)}</div></div>
  </div>

  <h2>🧩 Motherboard & Firmware</h2>
  <div class="grid">
    <div class="card"><div class="label">Motherboard</div><div class="val">{board.get('Manufacturer', '')} {board.get('Product', '')}</div></div>
    <div class="card"><div class="label">Serial Number</div><div class="val">{board.get('SerialNumber', 'N/A')}</div></div>
    <div class="card"><div class="label">BIOS Vendor / Version</div><div class="val">{bios.get('Manufacturer', '')} {bios.get('SMBIOSBIOSVersion', '')}</div></div>
  </div>

  <h2>⚡ Processor (CPU)</h2>
  <div class="card" style="border-left-color: #eab308;">
    <div class="label">Processor Model</div>
    <div class="val">{cpu_info.get('Name', 'Processor')}</div>
    <p style="margin: 8px 0 4px 0; color: #cbd5e1;">Cores: <strong>{data.get('cpu_count_phys')} Physical</strong> / <strong>{data.get('cpu_count_log')} Logical Threads</strong> | L3 Cache: <strong>{cpu_info.get('L3CacheSize', 0) // 1024} MB</strong></p>
    <div class="label" style="margin-top: 10px;">Overall Load: {data.get('cpu_percent_overall')}%</div>
    <div class="bar-bg"><div class="bar-fill" style="width: {data.get('cpu_percent_overall')}%;"></div></div>
  </div>

  <h2>🧠 Memory (RAM)</h2>
  <div class="card" style="border-left-color: #ec4899;">
    <div class="val">{_format_size(data.get('ram_total'))} Total ({_format_size(data.get('ram_used'))} Used / {_format_size(data.get('ram_available'))} Free)</div>
    <div class="bar-bg"><div class="bar-fill" style="width: {data.get('ram_percent')}%; background: #ec4899;"></div></div>
  </div>

  <h2>🎮 Graphics (GPU)</h2>
  <table>
    <tr><th>GPU Name</th><th>Driver Version</th><th>Video Memory (VRAM)</th><th>Resolution</th></tr>
    {''.join([f"<tr><td>{g.get('Name')}</td><td>{g.get('DriverVersion')}</td><td>{_format_size(g.get('AdapterRAM', 0))}</td><td>{g.get('VideoModeDescription', 'N/A')}</td></tr>" for g in gpus])}
  </table>

  <h2>💾 Storage & Drives</h2>
  <table>
    <tr><th>Disk Model</th><th>Size</th><th>S.M.A.R.T Status</th><th>Media Type</th></tr>
    {''.join([f"<tr><td>{d.get('Model')}</td><td>{_format_size(d.get('Size', 0))}</td><td>{d.get('Status')}</td><td>{d.get('MediaType')}</td></tr>" for d in disks])}
  </table>

  <h2>🌐 Network & IP</h2>
  <p>Public IP: <strong style="color: #22c55e;">{data.get('public_ip')}</strong></p>
  <table>
    <tr><th>Interface</th><th>MAC Address</th><th>Link Speed</th></tr>
    {''.join([f"<tr><td>{n.get('Name')} ({n.get('InterfaceDescription')})</td><td>{n.get('MacAddress')}</td><td>{n.get('LinkSpeed')}</td></tr>" for n in net_adapters])}
  </table>

  <div class="footer">Generated by Windows Terminal ToolKit v1.0</div>
</div>
</body>
</html>
"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} HTML report generated: {os.path.abspath(filepath)}")
        import webbrowser
        open_now = input("Open report in web browser now? (y/n): ").strip().lower()
        if open_now == 'y':
            webbrowser.open(os.path.abspath(filepath))
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to export HTML report: {e}")

def run_deep_inspection():
    """Entry point for deep system inspection."""
    print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Scanning computer hardware, firmware, OS, and security components in depth...")
    start_t = time.time()
    data = gather_deep_system_info()
    elapsed = time.time() - start_t
    print(f"{Colors.GREEN}[INFO]{Colors.RESET} Deep inspection completed in {elapsed:.2f} seconds.\n")

    render_terminal_report(data)

    while True:
        print(f"{Colors.CYAN}--- Report Actions ---{Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Export Full Report to Plain Text (.txt)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Export Full Report to Web Document (.html)")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Refresh & Rescan Diagnostics")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back")
        
        c = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if c == '0':
            break
        elif c == '1':
            fname = input("Filename (default: deep_system_report.txt): ").strip() or "deep_system_report.txt"
            export_report_txt(data, fname)
        elif c == '2':
            fname = input("Filename (default: deep_system_report.html): ").strip() or "deep_system_report.html"
            export_report_html(data, fname)
        elif c == '3':
            print(f"\n{Colors.BLUE}[INFO]{Colors.RESET} Rescanning...")
            data = gather_deep_system_info()
            render_terminal_report(data)

if __name__ == "__main__":
    Colors.init()
    run_deep_inspection()
