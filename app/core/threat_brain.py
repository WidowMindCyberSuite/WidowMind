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

def log_threat(source, threat_type, detail, score=1, status="pending", hostname=None, ip_address=None):
    """
    Logs a detected threat into the threats database.

    Parameters:
        - source: Source agent or subsystem
        - threat_type: Type/category of threat detected
        - detail: Full text or short description of the threat
        - score: Severity score (default 1)
        - status: Threat status (default 'pending')
        - hostname: Hostname of the reporting system (optional)
        - ip_address: IP address of the reporting system (optional)
    """
    # Correct database path, even inside Docker
    db_path = os.path.join(os.path.dirname(__file__), "../database/threat_log.db")
    db_path = os.path.abspath(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert threat data into the threats table
    cursor.execute('''
        INSERT INTO threats (source, threat_type, detail, score, status, hostname, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (source, threat_type, detail, score, status, hostname, ip_address))

    conn.commit()
    conn.close()