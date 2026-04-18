import subprocess
import os


# TOOL REGISTRY (whitelist)
def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"File scritto: {path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def read_file(path):
    try:
        if not os.path.exists(path):
            return {"status": "error", "message": "File non trovato"}

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        return {"status": "success", "data": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# REGISTRO TOOL
TOOLS = {
    "write_file": write_file,
    "read_file": read_file,
    "run_command": run_command
}


class ACTION_EXECUTOR:

    def __init__(self):
        self.tools = TOOLS

    def execute(self, task):
        """
        task = {
            "tool": "write_file",
            "params": {
                "path": "output/test.txt",
                "content": "hello"
            }
        }
        """

        tool_name = task.get("tool")
        params = task.get("params", {})

        if tool_name not in self.tools:
            return {
                "status": "error",
                "message": f"Tool non valido: {tool_name}"
            }

        try:
            result = self.tools[tool_name](**params)
            return result

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }