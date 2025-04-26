import threading
import time
import json
import requests
from core.system_logger import log_system_event
from config.config_loader import load_config
import csv
import io

# Load WidowMind config
config = load_config()

SYNC_INTERVAL = config['intelli_spider']['sync_interval']
ENABLE_THREATFOX = config['intelli_spider']['enable_threatfox']
ENABLE_MALWAREBAZAAR = config['intelli_spider']['enable_malwarebazaar']
ENABLE_OTX = config['intelli_spider']['enable_otx']

# Local memory (where pulled threats live)
LIVE_THREATS = {
    "blacklisted_processes": set()
}

def fetch_threatfox():
    try:
        url = "https://threatfox.abuse.ch/export/csv/recent/"
        res = requests.get(url, timeout=15)
        
        if res.status_code == 200:
            threats = []
            content = res.content.decode('utf-8')
            csv_reader = csv.reader(io.StringIO(content))
            for row in csv_reader:
                if len(row) > 5:
                    malware_name = row[5].strip()
                    if malware_name and malware_name != 'malware_alias':
                        threats.append(malware_name)
            return threats
        else:
            log_system_event(f"[Error] ThreatFox CSV fetch bad status {res.status_code}")
    except Exception as e:
        log_system_event(f"[Error] ThreatFox CSV fetch failed: {e}")

    return []

def fetch_malwarebazaar():
    try:
        url = "https://mb-api.abuse.ch/api/v1/"
        payload = {"query": "get_recent"}
        headers = {'Content-Type': 'application/json'}
        res = requests.post(url, data=payload, timeout=15)
        if res.status_code == 200:
            data = res.json()
            threats = [entry['file_name'] for entry in data.get('data', []) if entry.get('file_name')]
            return threats
    except Exception as e:
        log_system_event(f"[Error] MalwareBazaar fetch failed: {e}")
    return []

def fetch_otx():
    try:
        url = "https://otx.alienvault.com/api/v1/indicators/malware/analysis"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            # Placeholder: real OTX integration needs API key or specific endpoint
            return []
    except Exception as e:
        log_system_event(f"[Error] AlienVault OTX fetch failed: {e}")
    return []

def merge_threats(new_threats):
    initial_count = len(LIVE_THREATS['blacklisted_processes'])
    for threat in new_threats:
        if threat:
            LIVE_THREATS['blacklisted_processes'].add(threat.lower())
    updated_count = len(LIVE_THREATS['blacklisted_processes'])
    added = updated_count - initial_count
    return added

def sync_threats():
    while True:
        total_new = 0

        if ENABLE_THREATFOX:
            threats = fetch_threatfox()
            total_new += merge_threats(threats)

        if ENABLE_MALWAREBAZAAR:
            threats = fetch_malwarebazaar()
            total_new += merge_threats(threats)

        if ENABLE_OTX:
            threats = fetch_otx()
            total_new += merge_threats(threats)

        log_system_event(f"[IntelliSpider] Synced {total_new} new threats.")

        time.sleep(SYNC_INTERVAL)

def launch_intelli_spider():
    threading.Thread(target=sync_threats, name="IntelliSpider", daemon=True).start()
