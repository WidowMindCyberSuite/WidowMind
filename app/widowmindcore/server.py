# app/arachnocore_server.py
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from core.threat_brain import log_threat
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🕷️ WidowMind Core API is running!", 200

@app.route("/api/threat", methods=["POST"])
def receive_threat():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    try:
        source = data.get("source")
        threat_type = data.get("threat_type")
        detail = data.get("detail")
        score = data.get("score", 1)  # Default score if not provided
        status = data.get("status", "pending")  # Default status
        hostname = data.get("hostname")
        ip_address = data.get("ip_address")

        # Use Threat Brain to log the threat
        log_threat(source, threat_type, detail, score, status, hostname, ip_address)

        return jsonify({"success": True}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/heartbeat", methods=["POST"])
def receive_heartbeat():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    hostname = data.get("hostname")
    ip_address = data.get("ip_address")

    print(f"💓 Heartbeat received from {hostname} ({ip_address})")
    return jsonify({"success": True}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
