class MULTI_STEP_PLANNER:
    """
    MSP v2:
    trasforma un GOAL strutturato in una sequenza di task eseguibili (FIFO con dipendenze base)
    """

    def __init__(self, max_steps=5):
        self.max_steps = max_steps

    def plan(self, goal):
        """
        input:
            goal = {
                "goal": str,
                "type": "action | analysis | generation",
                "priority": int,
                "success_criteria": [],
                "constraints": []
            }

        output:
            list[task]
        """

        goal_text = goal.get("goal", "")
        goal_type = goal.get("type", "generation")

        tasks = []

        # STEP 1 — LOGGING SEMPRE PRESENTE
        tasks.append({
            "id": 1,
            "tool": "write_file",
            "params": {
                "path": "output/log.txt",
                "content": f"[MSP LOG] {goal_text}"
            },
            "depends_on": []
        })

        # STEP 2 — BRANCH LOGICO PRINCIPALE
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
                    "command": "echo ANALYSIS_MODE_ACTIVE"
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

        else:  # generation / default

            tasks.append({
                "id": 2,
                "tool": "write_file",
                "params": {
                    "path": "output/generated.txt",
                    "content": goal_text
                },
                "depends_on": [1]
            })

        # STEP 3 — LIMITATORE DI COMPLESSITÀ
        return self._apply_limits(tasks)

    def _apply_limits(self, tasks):
        """
        evita overengineering: tronca e normalizza la pipeline
        """

        if len(tasks) > self.max_steps:
            tasks = tasks[:self.max_steps]

        # normalizzazione ID (sicurezza pipeline)
        for i, task in enumerate(tasks, start=1):
            task["id"] = i

        return tasks