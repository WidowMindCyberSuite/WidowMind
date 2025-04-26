import sqlite3
import os

DB_PATH = os.path.join('database', 'threat_log.db')

def patch_database():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Try adding missing columns safely
    try:
        c.execute("ALTER TABLE threats ADD COLUMN status TEXT DEFAULT 'pending';")
        print("[+] Added 'status' column.")
    except Exception as e:
        print("[!] 'status' column may already exist.")

    try:
        c.execute("ALTER TABLE threats ADD COLUMN device_ip TEXT;")
        print("[+] Added 'device_ip' column.")
    except Exception as e:
        print("[!] 'device_ip' column may already exist.")

    try:
        c.execute("ALTER TABLE threats ADD COLUMN hostname TEXT;")
        print("[+] Added 'hostname' column.")
    except Exception as e:
        print("[!] 'hostname' column may already exist.")

    conn.commit()
    conn.close()
    print("[+] Database patch complete.")

if __name__ == "__main__":
    patch_database()
