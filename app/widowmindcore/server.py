# app/widowmindcore/server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from widowmindcore.core.threat_brain import log_threat
from widowmindcore.database import initialize_database, get_all_threats, update_threat_status

# Initialize Flask app
app = Flask(__name__)

# Initialize the database on startup
initialize_database()

# Allow CORS for agents posting from different origins
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WidowMindCore')

# =========================
# API ROUTES
# =========================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🕷️ WidowMind Core API is running!"}), 200

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/threat", methods=["POST"])
def receive_threat():
    data = request.get_json(force=True, silent=True)
    if not data:
        logger.warning("Received invalid threat JSON.")
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    try:
        source = data.get("source")
        threat_type = data.get("threat_type")
        detail = data.get("detail")
        score = data.get("score", 1)
        status = data.get("status", "pending")
        hostname = data.get("hostname")
        device_ip = data.get("device_ip")  # 🔥 Corrected field

        logger.info(f"🛡️ Threat received: {threat_type} from {hostname} ({device_ip})")

        log_threat(source, threat_type, detail, score, status, hostname, device_ip)

        return jsonify({"success": True}), 201

    except Exception as e:
        logger.error(f"❌ Error processing threat: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/heartbeat", methods=["POST"])
def receive_heartbeat():
    data = request.get_json(force=True, silent=True)
    if not data:
        logger.warning("Received invalid heartbeat JSON.")
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    hostname = data.get("hostname")
    device_ip = data.get("device_ip")  # 🔥 Corrected field

    logger.info(f"💓 Heartbeat received from {hostname} ({device_ip})")

    return jsonify({"success": True}), 200

@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        threats = get_all_threats()
        return jsonify(threats), 200
    except Exception as e:
        logger.error(f"❌ Error fetching data: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/update_status", methods=["POST"])
def update_status():
    try:
        data = request.get_json(force=True, silent=True)
        threat_id = data.get('id')
        new_status = data.get('status')

        update_threat_status(threat_id, new_status)

        logger.info(f"✅ Threat {threat_id} updated to status '{new_status}'")
        return jsonify({"success": True}), 200

    except Exception as e:
        logger.error(f"❌ Error updating threat status: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# =========================
# END OF API
# =========================
