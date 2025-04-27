import sqlite3
import os

# Set correct DB directory and path
DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'database')
DB_PATH = os.path.join(DB_DIR, 'threat_log.db')

def patch_database():
    if not os.path.exists(DB_PATH):
        print(f"[❌] Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("[🛠️] Starting database patch process...")

    # Try adding missing columns safely
    patch_steps = [
        ("ALTER TABLE threats ADD COLUMN status TEXT DEFAULT 'pending';", "status"),
        ("ALTER TABLE threats ADD COLUMN device_ip TEXT;", "device_ip"),
        ("ALTER TABLE threats ADD COLUMN hostname TEXT;", "hostname"),
    ]

    for sql, column in patch_steps:
        try:
            c.execute(sql)
            print(f"[+] Added '{column}' column successfully.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"[!] Column '{column}' already exists. Skipping.")
            else:
                print(f"[⚠️] Error patching '{column}' column: {e}")

    conn.commit()
    conn.close()
    print("[✅] Database patch complete.")

if __name__ == "__main__":
    patch_database()
