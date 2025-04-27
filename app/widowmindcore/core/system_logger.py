import os
from datetime import datetime

# === Setup Log Directory ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
SYSLOG_FILE = os.path.join(LOG_DIR, 'widowmind_syslog.log')

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_system_event(message, level="INFO"):
    """
    Logs a system event with timestamp to WidowMind system log.

    Parameters:
        message (str): Event message to log
        level (str): Logging level (e.g., INFO, WARNING, ERROR)
    """
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    log_entry = f"{timestamp} [{level}] {message}"

    with open(SYSLOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

    print(f"[SYSLOG] {log_entry}")

