from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'threat_log.db')

def fetch_threats():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, timestamp, source, threat_type, detail, score, status, device_ip, hostname FROM threats ORDER BY id DESC LIMIT 100")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return []

@app.route("/")
def index():
    threats = fetch_threats()
    return render_template("index.html", threats=threats)

@app.route("/data")
def data():
    return jsonify(fetch_threats())

@app.route("/update_status", methods=["POST"])
def update_status():
    try:
        threat_id = request.json['id']
        new_status = request.json['status']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE threats SET status = ? WHERE id = ?", (new_status, threat_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
