from flask import Flask, jsonify, request, render_template
import json
import os

from core.agent import SISS_AGENT
from core.ts import TEMPORAL_SCHEDULER

app = Flask(__name__)

# =========================
# CORE SYSTEM
# =========================
agent = SISS_AGENT()
scheduler = None

# =========================
# COUNTER SYSTEM
# =========================
COUNTER_FILE = "counter.json"

def read_count():
    if not os.path.exists(COUNTER_FILE):
        return 0
    with open(COUNTER_FILE, "r") as f:
        return json.load(f).get("count", 0)

def write_count(v):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": v}, f)

# =========================
# PAGES (ROUTER)
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/engineering")
def engineering():
    return render_template("engineering.html")

@app.route("/library")
def library():
    return render_template("library.html")

# =========================
# COUNTER API
# =========================
@app.route("/hit")
def hit():
    c = read_count() + 1
    write_count(c)
    return jsonify({"count": c})

@app.route("/counter")
def counter():
    return jsonify({"count": read_count()})

# =========================
# SISS CORE API
# =========================
@app.route("/api/run", methods=["POST"])
def run_step():
    data = request.json
    input_text = data.get("input", "")

    result = agent.step(input_text)
    return jsonify(result)

@app.route("/api/start", methods=["POST"])
def start_scheduler():
    global scheduler

    data = request.json
    seed = data.get("seed", "auto")

    scheduler = TEMPORAL_SCHEDULER(agent, interval=5)
    scheduler.start(seed)

    return jsonify({"status": "scheduler_started"})

@app.route("/api/stop", methods=["POST"])
def stop_scheduler():
    global scheduler

    if scheduler:
        scheduler.stop()
        scheduler = None

    return jsonify({"status": "scheduler_stopped"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "system": "SISS ACTIVE",
        "scheduler": scheduler is not None
    })

# =========================
# BOOT
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)