import threading
import time
import psutil
import sqlite3
import subprocess
from core.system_logger import log_system_event
from config.config_loader import load_config

# Load config
config = load_config()
DB_PATH = "database/threat_log.db"
RECLUSE_INTERVAL = 30  # Check every 30 seconds

def kill_process(proc_name):
    """Kill all processes matching proc_name."""
    killed = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == proc_name.lower():
                proc.kill()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed

def trigger_defender_scan():
    """Trigger a Windows Defender Quick Scan."""
    try:
        subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType QuickScan"], capture_output=True)
        log_system_event("[Recluse] Triggered Windows Defender Quick Scan.")
    except Exception as e:
        log_system_event(f"[Recluse] Failed to trigger Defender scan: {e}")

def auto_neutralize():
    """Recluse Spider: hunts confirmed threats and neutralizes them."""
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, detail FROM threats WHERE status = 'confirmed'")
            rows = c.fetchall()
            conn.close()

            for threat_id, detail in rows:
                proc_name = extract_process_name(detail)
                if proc_name:
                    killed = kill_process(proc_name)
                    if killed > 0:
                        log_system_event(f"[Recluse] Neutralized {killed} instance(s) of '{proc_name}'.")
                        trigger_defender_scan()
                        # Optionally: mark threat as "neutralized" in DB (Phase 6)
        except Exception as e:
            log_system_event(f"[Recluse] Error during neutralization: {e}")

        time.sleep(RECLUSE_INTERVAL)

def extract_process_name(detail):
    """Extracts the process name from a detail string."""
    if "'" in detail:
        parts = detail.split("'")
        if len(parts) >= 2:
            return parts[1].split(' ')[0]
    return None

def launch_recluse():
    threading.Thread(target=auto_neutralize, name="Recluse", daemon=True).start()
