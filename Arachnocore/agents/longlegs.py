# === agents/longlegs.py ===

import os
import time
import socket
import psutil
import subprocess
from core.threat_brain import log_threat
from config.config_loader import load_config

# Load WidowMind config
config = load_config()
WATCH_PATHS = config['longlegs']['watch_paths']
KNOWN_PORTS = config['longlegs']['known_ports']
SCAN_INTERVAL = config['longlegs']['scan_interval']


def hash_file(filepath):
    try:
        if not os.path.exists(filepath):
            return None
        with open(filepath, "rb") as f:
            data = f.read()
            return hash(data)
    except Exception as e:
        print(f"[ERROR] Couldn't hash {filepath}: {e}")
        return None


def check_critical_files(file_hashes):
    for path in WATCH_PATHS:
        current_hash = hash_file(path)
        old_hash = file_hashes.get(path)

        if current_hash and old_hash and current_hash != old_hash:
            log_threat("longlegs", "Critical File Modified", f"Change detected in {path}")
            file_hashes[path] = current_hash


def scan_open_ports():
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0 and port not in KNOWN_PORTS:
            log_threat("longlegs", "Unusual Open Port", f"Port {port} is open but not whitelisted")
        sock.close()


def detect_suspicious_processes():
    suspicious_names = ["netcat", "nc", "nmap", "hydra", "minerd", "xmrig"]
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            proc_name = (proc.info['name'] or "").lower()
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            combined = f"{proc_name} {cmdline}".lower()

            for bad in suspicious_names:
                if bad in combined:
                    log_threat("longlegs", "Suspicious Process Detected", f"Detected {proc_name}")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def check_cron_jobs():
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        output = result.stdout

        if output.strip():
            for line in output.splitlines():
                if line and not line.startswith('#'):
                    log_threat("longlegs", "Suspicious Cron Entry", line)
    except Exception as e:
        print(f"[ERROR] Cron job scan failed: {e}")


def longlegs_loop():
    print("🕷️ LongLegs spider deployed... Hunting threats on Linux.")

    # Hash critical files initially
    file_hashes = {path: hash_file(path) for path in WATCH_PATHS}

    while True:
        check_critical_files(file_hashes)
        scan_open_ports()
        detect_suspicious_processes()
        check_cron_jobs()
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    longlegs_loop()
