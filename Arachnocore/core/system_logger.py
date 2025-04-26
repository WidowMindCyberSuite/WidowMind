import os
from datetime import datetime

# === Setup Log Directory ===
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

SYSLOG_FILE = os.path.join(LOG_DIR, 'widowmind_syslog.log')

def log_system_event(event):
    """Logs a system event with timestamp to WidowMind system log."""
    timestamp = datetime.now().isoformat()
    with open(SYSLOG_FILE, 'a') as f:
        f.write(f"{timestamp} [SYSTEM] {event}\n")
    print(f"[SYSLOG] {event}")
