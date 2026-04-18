import subprocess
import os


def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {"status": "success", "data": f.read()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def run_command(command):
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "status": "success" if r.returncode == 0 else "error",
            "stdout": r.stdout,
            "stderr": r.stderr
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


TOOLS = {
    "write_file": write_file,
    "read_file": read_file,
    "run_command": run_command
}


class ACTION_EXECUTOR:

    def execute(self, task):
        tool = task.get("tool")
        params = task.get("params", {})

        if tool not in TOOLS:
            return {"status": "error", "message": "invalid tool"}

        return TOOLS[tool](**params)