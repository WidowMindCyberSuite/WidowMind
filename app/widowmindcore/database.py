# WidowMind Core Database Layer
import os
import sqlite3

DB_DIR = '/app/database'
DB_PATH = f'{DB_DIR}/threat_log.db'

# Insert a new threat record
def insert_threat(source, threat_type, detail, score, status, hostname, device_ip):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO threats (source, threat_type, detail, score, status, hostname, device_ip)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (source, threat_type, detail, score, status, hostname, device_ip))
    conn.commit()
    conn.close()

# Get all threat records
def get_all_threats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM threats")
    threats = cursor.fetchall()
    conn.close()
    return threats

# Update status of a threat record
def update_threat_status(threat_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE threats SET status = ? WHERE id = ?", (new_status, threat_id))
    conn.commit()
    conn.close()

# WidowMindCore: Initialize database if missing
def initialize_database():
    # 🛠 Create /app/database if missing
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            threat_type TEXT,
            detail TEXT,
            score INTEGER,
            status TEXT,
            hostname TEXT,
            device_ip TEXT
        )
    ''')
    conn.commit()
    conn.close()
