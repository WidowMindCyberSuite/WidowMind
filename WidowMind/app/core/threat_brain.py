import sqlite3
import socket
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'threat_log.db')

# Ensure database directory exists
os.makedirs(DB_DIR, exist_ok=True)

THREAT_SCORES = {
    "Unusual Open Port": 3,
    "High CPU Usage": 2,
    "Suspicious Process": 4,
    "Unauthorized File Access": 5,
    "Defender Detected Threat": 5,
    "Suspicious Registry Startup": 4,
    "Suspicious Scheduled Task": 4
}

def get_score(threat_type):
    return THREAT_SCORES.get(threat_type, 1)

def get_device_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "0.0.0.0"
    return hostname, ip_address

def log_threat(source, threat_type, detail, status_override=None):
    score = get_score(threat_type)
    timestamp = datetime.now().isoformat()
    hostname, ip_address = get_device_info()
    status = status_override if status_override else "pending"

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source TEXT,
                threat_type TEXT,
                detail TEXT,
                score INTEGER,
                status TEXT DEFAULT 'pending',
                device_ip TEXT,
                hostname TEXT
            )
        ''')
        c.execute('''
            INSERT INTO threats (timestamp, source, threat_type, detail, score, status, device_ip, hostname)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, source, threat_type, detail, score, status, ip_address, hostname))
        conn.commit()
        conn.close()
        print(f"[LOGGED] {timestamp} | {source} | {threat_type} | Status: {status} | Score: {score}")
    except Exception as e:
        print(f"[ERROR] Failed to log threat: {e}")
