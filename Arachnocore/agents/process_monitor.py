import psutil
import time
import json
from core.threat_brain import log_threat
from config.config_loader import load_config

# Load WidowMind config
config = load_config()

# Load Safe Patterns
with open("config/safe_patterns.json", "r") as f:
    safe_patterns = json.load(f)

SAFE_PROCESSES = [p.lower() for p in safe_patterns.get('safe_processes', [])]
SAFE_PARENTS = [p.lower() for p in safe_patterns.get('safe_parents', [])]
SAFE_PATHS = [p.lower() for p in safe_patterns.get('safe_paths', [])]

BLACKLISTED_PROCESSES = [b.lower() for b in config['process_monitor']['blacklisted_processes']]
SCAN_INTERVAL = config['process_monitor']['scan_interval']

def check_processes():
    print(f"🕷️ Arachnocore: Watching for blacklisted processes and safe chain anomalies...")

    while True:
        time.sleep(SCAN_INTERVAL)
        for proc in psutil.process_iter(['pid', 'ppid', 'name', 'exe', 'cmdline']):
            try:
                proc_name = (proc.info['name'] or "").lower()
                proc_path = (proc.info['exe'] or "").lower()
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                combined = f"{proc_name} {cmdline}".lower()

                ppid = proc.info['ppid']
                parent_name = psutil.Process(ppid).name().lower() if ppid else "unknown"

                # Default status
                status = "pending"

                # Blacklist override
                for bad in BLACKLISTED_PROCESSES:
                    if bad in combined:
                        status = "confirmed"
                        break

                # Safe chain override
                if parent_name in SAFE_PARENTS or any(proc_path.startswith(path) for path in SAFE_PATHS):
                    status = "safe"

                # Log the process
                detail = f"Detected '{proc_name}' (Parent: {parent_name})"

                log_threat(
                    source="process_monitor",
                    threat_type="Suspicious Process",
                    detail=detail,
                    status_override=status
                )

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

if __name__ == "__main__":
    check_processes()
