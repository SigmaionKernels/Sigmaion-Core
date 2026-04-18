class MULTI_STEP_PLANNER:

    def __init__(self, max_steps=5):
        self.max_steps = max_steps

    def plan(self, goal):

        goal_text = goal.get("goal", "")
        goal_type = goal.get("type", "generation")

        tasks = []

        # STEP 1 — LOG SEMPRE
        tasks.append({
            "id": 1,
            "tool": "write_file",
            "params": {
                "path": "output/log.txt",
                "content": f"[MSP] {goal_text}"
            },
            "depends_on": []
        })

        # STEP 2 — BRANCH LOGICO
        if goal_type == "action":

            tasks.append({
                "id": 2,
                "tool": "write_file",
                "params": {
                    "path": "output/action.txt",
                    "content": goal_text
                },
                "depends_on": [1]
            })

        elif goal_type == "analysis":

            tasks.append({
                "id": 2,
                "tool": "run_command",
                "params": {
                    "command": "echo ANALYSIS_MODE"
                },
                "depends_on": [1]
            })

            tasks.append({
                "id": 3,
                "tool": "write_file",
                "params": {
                    "path": "output/analysis.txt",
                    "content": goal_text
                },
                "depends_on": [2]
            })

        else:

            tasks.append({
                "id": 2,
                "tool": "write_file",
                "params": {
                    "path": "output/generated.txt",
                    "content": goal_text
                },
                "depends_on": [1]
            })

        return self._limit(tasks)

    def _limit(self, tasks):

        if len(tasks) > self.max_steps:
            tasks = tasks[:self.max_steps]

        # normalizzazione ID
        for i, t in enumerate(tasks, start=1):
            t["id"] = i

        return tasks