import socket
import sqlite3
from datetime import datetime

# Define your "safe" ports
KNOWN_PORTS = [22, 80, 443, 53, 8080]

# Log to the local SQLite DB
def log_threat(port):
    conn = sqlite3.connect('../database/threat_log.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            threat_type TEXT,
            detail TEXT
        )
    ''')
    c.execute('INSERT INTO threats (timestamp, source, threat_type, detail) VALUES (?, ?, ?, ?)', (
        datetime.now().isoformat(),
        'network_monitor',
        'Unusual Open Port',
        f'Port {port} is open but not whitelisted'
    ))
    conn.commit()
    conn.close()

# Scan local ports
def scan_ports():
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"[!] Open port detected: {port}")
            if port not in KNOWN_PORTS:
                log_threat(port)
        sock.close()

if __name__ == "__main__":
    print("Arachnocore: Running network monitor spider...")
    scan_ports()
