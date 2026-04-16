import os
import markdown

CONTENT_DIR = "content"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read())

    out_name = os.path.basename(md_path).replace(".md", ".html")
    out_path = os.path.join(OUTPUT_DIR, out_name)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

for f in os.listdir(CONTENT_DIR):
    if f.endswith(".md"):
        convert(os.path.join(CONTENT_DIR, f))