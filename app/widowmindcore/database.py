# WidowMind Core Database Layer

import sqlite3

DB_PATH = '/app/database/threat_log.db'

# Insert a new threat record
def insert_threat(source, threat_type, detail, score, status, hostname, ip_address):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO threats (source, threat_type, detail, score, status, hostname, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (source, threat_type, detail, score, status, hostname, ip_address))
    conn.commit()
    conn.close()

# New: Get all threat records
def get_all_threats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM threats")
    threats = cursor.fetchall()
    conn.close()
    return threats

# New: Update status of a threat record
def update_threat_status(threat_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE threats SET status = ? WHERE id = ?", (new_status, threat_id))
    conn.commit()
    conn.close()
