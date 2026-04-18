class VALIDATION_FEEDBACK_SYSTEM:

    def __init__(self, max_retries=1):
        self.max_retries = max_retries

    def evaluate(self, goal, execution_results):

        """
        input:
            goal (GMS)
            execution_results (AE output list)

        output:
            {
                "status": "pass | retry | fail",
                "score": float,
                "action": str
            }
        """

        score = self._compute_score(goal, execution_results)

        if score >= 0.75:
            return {
                "status": "pass",
                "score": score,
                "action": "continue"
            }

        elif score >= 0.4:
            return {
                "status": "retry",
                "score": score,
                "action": "rebuild_tasks"
            }

        else:
            return {
                "status": "fail",
                "score": score,
                "action": "stop"
            }

    def _compute_score(self, goal, results):

        # baseline heuristica semplice ma stabile

        if not results:
            return 0.0

        success_count = 0
        total = len(results)

        for r in results:
            if r["result"].get("status") == "success":
                success_count += 1

        base_score = success_count / total

        # bonus: coerenza con goal type
        if goal.get("type") == "action":
            base_score += 0.05

        if goal.get("priority", 3) == 1:
            base_score += 0.05

        return min(base_score, 1.0)