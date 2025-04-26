import socket
import time
from core.threat_brain import log_threat
from config.config_loader import load_config

config = load_config()
KNOWN_PORTS = config['network_monitor']['known_ports']
SCAN_INTERVAL = config['network_monitor']['scan_interval']

def scan_ports():
    while True:
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                print(f"[!] Open port detected: {port}")
                if port not in KNOWN_PORTS:
                    log_threat("network_monitor", "Unusual Open Port", f"Port {port} is open but not whitelisted")
            sock.close()
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    print("Arachnocore: Running network monitor spider...")
    scan_ports()
