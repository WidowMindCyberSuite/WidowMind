import os
import time
import hashlib
from core.threat_brain import log_threat
from config.config_loader import load_config

config = load_config()
WATCH_PATHS = config['file_monitor']['watch_paths']
SCAN_INTERVAL = config['file_monitor']['scan_interval']

def hash_file(filepath):
    try:
        if not os.path.exists(filepath):
            print(f"[WARNING] File not found: {filepath}")
            return None
        with open(filepath, "rb") as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()
    except Exception as e:
        print(f"[ERROR] Couldn't hash {filepath}: {e}")
        return None

def watch_files():
    file_hashes = {path: hash_file(path) for path in WATCH_PATHS}

    print(f"🕷️ Arachnocore: Watching {len(WATCH_PATHS)} files...")

    while True:
        time.sleep(SCAN_INTERVAL)
        for path in WATCH_PATHS:
            current_hash = hash_file(path)
            old_hash = file_hashes.get(path)

            # Only alert if file exists and was changed
            if current_hash and old_hash and current_hash != old_hash:
                log_threat("file_monitor", "Unauthorized File Access", f"Change detected in {path}")
                file_hashes[path] = current_hash

if __name__ == "__main__":
    watch_files()

