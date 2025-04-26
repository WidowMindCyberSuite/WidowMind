import psutil
import time
from core.threat_brain import log_threat
from config.config_loader import load_config

config = load_config()
BLACKLISTED_PROCESSES = config['process_monitor']['blacklisted_processes']
SCAN_INTERVAL = config['process_monitor']['scan_interval']

def check_processes():
    print(f"🕷️ Arachnocore: Watching for blacklisted processes...")
    
    while True:
        time.sleep(SCAN_INTERVAL)
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = proc.info['name'] or ''
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                combined = f"{name} {cmdline}".lower()

                for bad in BLACKLISTED_PROCESSES:
                    if bad.lower() in combined:
                        log_threat(
                            "process_monitor",
                            "Suspicious Process",
                            f"Detected process '{combined}' (PID {proc.pid})"
                        )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

if __name__ == "__main__":
    check_processes()
