class VALIDATION_FEEDBACK_SYSTEM:

    def __init__(self, pass_threshold=0.75, retry_threshold=0.4):
        self.pass_threshold = pass_threshold
        self.retry_threshold = retry_threshold

    def evaluate(self, goal, execution_results):

        if not execution_results:
            return {
                "status": "fail",
                "score": 0.0,
                "action": "stop"
            }

        score = self._score(execution_results, goal)

        if score >= self.pass_threshold:
            return {
                "status": "pass",
                "score": score,
                "action": "continue"
            }

        if score >= self.retry_threshold:
            return {
                "status": "retry",
                "score": score,
                "action": "rebuild_tasks"
            }

        return {
            "status": "fail",
            "score": score,
            "action": "stop"
        }

    def _score(self, results, goal):

        success = 0
        total = len(results)

        for r in results:
            if r["result"].get("status") == "success":
                success += 1

        base = success / total if total > 0 else 0

        # bonus minimal coerente
        if goal.get("type") == "action":
            base += 0.05

        if goal.get("priority", 3) == 1:
            base += 0.05

        if base > 1:
            base = 1

        return base