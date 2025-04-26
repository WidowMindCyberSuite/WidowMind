import subprocess
import time
import os
from core.threat_brain import log_threat
from core.system_logger import log_system_event
from config.config_loader import load_config

config = load_config()
SCAN_INTERVAL = config['huntsman']['scan_interval']  # 5 min = 300 sec

def check_registry_startup():
    """Scan common startup registry keys for suspicious entries."""
    suspicious = []

    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'"],
            capture_output=True, text=True
        )
        output = result.stdout

        if output.strip():  # If anything exists
            for line in output.splitlines():
                if "=" in line and "Windows" not in line:
                    suspicious.append(line.strip())
    except Exception as e:
        log_system_event(f"Huntsman Registry Scan Error: {e}")

    return suspicious

def check_scheduled_tasks():
    """Check for newly scheduled tasks that might be suspicious."""
    suspicious = []

    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-ScheduledTask | Where-Object {$_.TaskName -notlike '*Microsoft*'}"],
            capture_output=True, text=True
        )
        output = result.stdout

        if output.strip():
            for line in output.splitlines():
                if line and not line.startswith("TaskName"):
                    suspicious.append(line.strip())
    except Exception as e:
        log_system_event(f"Huntsman Task Scan Error: {e}")

    return suspicious

def check_defender_threats():
    """Query Microsoft Defender for active threats."""
    threats = []

    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-MpThreatDetection"],
            capture_output=True, text=True
        )
        output = result.stdout

        if output.strip() and "ThreatID" in output:
            threats.append(output.strip())
    except Exception as e:
        log_system_event(f"Huntsman Defender Scan Error: {e}")

    return threats

def huntsman_loop():
    """Main Huntsman loop."""
    print("🕷️ Huntsman spider deployed... Hunting every 5 minutes.")

    while True:
        registry_hits = check_registry_startup()
        task_hits = check_scheduled_tasks()
        defender_hits = check_defender_threats()

        for reg in registry_hits:
            log_threat("huntsman", "Suspicious Registry Startup", reg)

        for task in task_hits:
            log_threat("huntsman", "Suspicious Scheduled Task", task)

        for threat in defender_hits:
            log_threat("huntsman", "Defender Detected Threat", threat)

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    huntsman_loop()
