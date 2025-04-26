import os
import time
import hashlib
from core.threat_brain import log_threat

# === Settings ===
WATCH_PATHS = [
    "/etc/passwd",
    "/etc/shadow",
    "/home/joseph/Documents/secret.txt"
]

SCAN_INTERVAL = 5  # seconds


# === Helper: Get file hash ===
def hash_file(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()
    except Exception as e:
        print(f"[ERROR] Couldn't hash {filepath}: {e}")
        return None


# === Spider loop ===
def watch_files():
    file_hashes = {path: hash_file(path) for path in WATCH_PATHS}

    print(f"🕷️ Arachnocore: Watching {len(WATCH_PATHS)} files...")

    while True:
        time.sleep(SCAN_INTERVAL)
        for path in WATCH_PATHS:
            current_hash = hash_file(path)
            if current_hash and current_hash != file_hashes.get(path):
                log_threat("file_monitor", "Unauthorized File Access", f"Change detected in {path}")
                file_hashes[path] = current_hash  # Update hash after logging


if __name__ == "__main__":
    watch_files()
