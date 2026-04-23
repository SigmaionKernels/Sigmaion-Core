import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CONTENT_FILE = os.path.join(BASE_DIR, "content", "index.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "docs", "content.html")

def load_content():
    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_html(data):
    items = data.get("entries", [])

    html = "<html><body style='background:black;color:#00ff66;font-family:monospace'>"
    html += "<h1>SIGMAION CONTENT</h1>"

    for i, item in enumerate(items):
        html += f"<div><h3>ENTRY {i+1}</h3><pre>{item}</pre></div><hr>"

    html += "</body></html>"
    return html

def main():
    data = load_content()
    html = build_html(data)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("SIGMAION BUILD COMPLETE")

if __name__ == "__main__":
    main()