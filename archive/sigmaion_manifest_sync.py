import os
import json

ROOT = "."

def load_existing_manifest():
    try:
        with open("manifest.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"system": "SIGMAION", "modules": []}

def scan_folders():
    modules = []

    for item in os.listdir(ROOT):
        if os.path.isdir(item):
            files = os.listdir(item)

            modules.append({
                "name": item,
                "path": f"./{item}",
                "files": files
            })

    return modules

def build_manifest():
    manifest = load_existing_manifest()
    manifest["modules"] = scan_folders()
    return manifest

def save_manifest(manifest):
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def run():
    manifest = build_manifest()
    save_manifest(manifest)
    print("SIGMAION: MANIFEST SYNC COMPLETE")

if __name__ == "__main__":
    run()