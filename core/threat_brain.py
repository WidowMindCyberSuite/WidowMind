import sqlite3
from datetime import datetime

# Simple scoring rules based on type
THREAT_SCORES = {
    "Unusual Open Port": 3,
    "High CPU Usage": 2,
    "Suspicious Process": 4,
    "Unauthorized File Access": 5
}

DB_PATH = '../database/threat_log.db'


def get_score(threat_type):
    return THREAT_SCORES.get(threat_type, 1)  # Default score = 1


def log_threat(source, threat_type, detail):
    score = get_score(threat_type)
    timestamp = datetime.now().isoformat()

    # Log it
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            threat_type TEXT,
            detail TEXT,
            score INTEGER
        )
    ''')
    c.execute('''
        INSERT INTO threats (timestamp, source, threat_type, detail, score)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, source, threat_type, detail, score))
    conn.commit()
    conn.close()

    print(f"[LOGGED] {timestamp} | {source} | {threat_type} | Score: {score}")
