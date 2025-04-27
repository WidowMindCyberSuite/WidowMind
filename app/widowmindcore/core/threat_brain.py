# app/widowmindcore/core/threat_brain.py

from widowmindcore.database import insert_threat
from datetime import datetime

# === Threat score mappings ===
THREAT_SCORES = {
    "Unusual Open Port": 3,
    "High CPU Usage": 2,
    "Suspicious Process": 4,
    "Unauthorized File Access": 5,
    "Defender Detected Threat": 5,
    "Suspicious Registry Startup": 4,
    "Suspicious Scheduled Task": 4,
    "Persistence Mechanism Detected": 4,
    "Public IP Exposure": 3,
    "External Threat": 5,
    "DNS Resolution Event": 1,
    "Agent Error": 1,
}

def get_score(threat_type):
    """
    Returns a severity score for a given threat type.
    Defaults to 1 if type is unknown.
    """
    return THREAT_SCORES.get(threat_type, 1)

def log_threat(source, threat_type, detail, score=None, status="pending", hostname=None, device_ip=None):
    """
    Logs a threat event into the database.

    Parameters:
        source (str): Source agent or system
        threat_type (str): Type/category of threat
        detail (str): Specific threat details
        score (int): Threat severity score (optional, auto-scored if None)
        status (str): Status of threat ("pending", "confirmed", "safe")
        hostname (str): Name of the reporting device
        device_ip (str): IP address of the device
    """
    if score is None:
        score = get_score(threat_type)

    # Ensure default safe values
    if not status:
        status = "pending"

    insert_threat(source, threat_type, detail, score, status, hostname, device_ip)
