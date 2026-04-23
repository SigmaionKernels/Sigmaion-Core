import os
import json

ROOT = "."

def load_manifest():
    with open("manifest.json", "r", encoding="utf-8") as f:
        return json.load(f)

def scan_repo():
    structure = {}
    for folder in os.listdir(ROOT):
        if os.path.isdir(folder):
            structure[folder] = os.listdir(folder)
    return structure

def validate(manifest, structure):
    errors = []

    for module in manifest["modules"]:
        name = module["name"]
        if name not in structure:
            errors.append(f"Missing module folder: {name}")
            continue

        expected_path = structure[name]

        if len(expected_path) == 0:
            errors.append(f"Empty module: {name}")

    return errors

def run():
    manifest = load_manifest()
    structure = scan_repo()

    errors = validate(manifest, structure)

    if not errors:
        print("SIGMAION: OK - SYSTEM COHERENT")
    else:
        print("SIGMAION: INCOHERENCE DETECTED")
        for e in errors:
            print("-", e)

if __name__ == "__main__":
    run()