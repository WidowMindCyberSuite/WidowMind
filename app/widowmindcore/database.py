# WidowMind Core Database Layer
import os
import sqlite3

# === Setup Database Paths Dynamically ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'threat_log.db')

# === Database Operations ===

def insert_threat(source, threat_type, detail, score, status, hostname, device_ip):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO threats (source, threat_type, detail, score, status, hostname, device_ip)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (source, threat_type, detail, score, status, hostname, device_ip))
    conn.commit()
    conn.close()

def get_all_threats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, source, threat_type, detail, score, status, hostname, device_ip FROM threats ORDER BY id DESC")
    threats = cursor.fetchall()
    conn.close()
    return threats

def update_threat_status(threat_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE threats SET status = ? WHERE id = ?", (new_status, threat_id))
    conn.commit()
    conn.close()

def initialize_database():
    """
    Create the database and threats table if missing.
    """
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            threat_type TEXT,
            detail TEXT,
            score INTEGER,
            status TEXT DEFAULT 'pending',
            hostname TEXT,
            device_ip TEXT
        )
    ''')
    conn.commit()
    conn.close()
