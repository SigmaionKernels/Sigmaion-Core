from flask import Flask, jsonify, request, render_template
from core.agent import SISS_AGENT
from core.ts import TEMPORAL_SCHEDULER

app = Flask(__name__)

agent = SISS_AGENT()
scheduler = None


@app.route("/")
def home():
    return render_template("index.html")


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

    return jsonify({"status": "scheduler_stopped"})


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "system": "SISS ACTIVE",
        "scheduler": scheduler is not None
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)