from flask import Flask, jsonify, request, render_template_string
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "content", "articles.json")


# -----------------------
# SAFE STORAGE LAYER
# -----------------------
DEFAULT_STATE = {
    "meta": {
        "version": "1.0",
        "system": "SIGMAION",
        "source_of_truth": "articles.json"
    },
    "articles": []
}


def load_articles():
    if not os.path.exists(DATA_FILE):
        return DEFAULT_STATE

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return DEFAULT_STATE

            data = json.loads(content)

            if "articles" not in data:
                data["articles"] = []

            if "meta" not in data:
                data["meta"] = DEFAULT_STATE["meta"]

            return data

    except Exception:
        return DEFAULT_STATE


def save_articles(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -----------------------
# API LAYER
# -----------------------
@app.route("/api/articles", methods=["GET"])
def get_articles():
    return jsonify(load_articles())


@app.route("/api/articles", methods=["POST"])
def add_article():
    data = load_articles()
    payload = request.json

    if not isinstance(payload, dict):
        return jsonify({"status": "error", "message": "invalid payload"}), 400

    data["articles"].append(payload)
    save_articles(data)

    return jsonify({
        "status": "ok",
        "count": len(data["articles"])
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    save_articles(DEFAULT_STATE)
    return jsonify({"status": "reset"})


# -----------------------
# ADMIN UI MINIMALE
# -----------------------
ADMIN_HTML = """
<!doctype html>
<html>
<head>
    <title>SIGMAION CORE CONTROL</title>
</head>
<body>
    <h2>SIGMAION CONTROL</h2>

    <button onclick="loadData()">LOAD</button>
    <button onclick="addTest()">ADD TEST</button>
    <button onclick="resetData()">RESET</button>

    <pre id="out"></pre>

<script>
async function loadData(){
    try {
        const r = await fetch('/api/articles');
        const d = await r.json();
        document.getElementById('out').innerText =
            JSON.stringify(d, null, 2);
    } catch (e) {
        document.getElementById('out').innerText = "ERROR: " + e;
    }
}

async function addTest(){
    await fetch('/api/articles', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            title: "test",
            content: "auto-generated",
            timestamp: Date.now()
        })
    });

    loadData();
}

async function resetData(){
    await fetch('/api/reset', {method: 'POST'});
    loadData();
}

window.onload = loadData;
</script>

</body>
</html>
"""


@app.route("/")
def admin():
    return render_template_string(ADMIN_HTML)


# -----------------------
# START
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)