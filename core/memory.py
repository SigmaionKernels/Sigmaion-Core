import json
import os
from core.embedder import embed

MEM_FILE = "memory_store/vectors.json"

def load_memory():
    if not os.path.exists(MEM_FILE):
        return []

    with open(MEM_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    os.makedirs("memory_store", exist_ok=True)

    with open(MEM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def store_memory(text, output):
    data = load_memory()

    data.append({
        "text": text,
        "output": output,
        "vector": embed(text)
    })

    save_memory(data)