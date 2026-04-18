import re


class GOAL_MANAGEMENT_SYSTEM:

    def __init__(self):
        pass

    def parse(self, input_text):

        goal_type = self._detect_type(input_text)

        return {
            "goal": self._extract_goal(input_text),
            "success_criteria": self._generate_criteria(input_text),
            "constraints": self._extract_constraints(input_text),
            "priority": self._compute_priority(input_text),
            "type": goal_type
        }

    def _extract_goal(self, text):
        return text.strip()

    def _generate_criteria(self, text):
        criteria = []

        if "file" in text.lower():
            criteria.append("file creato correttamente")

        if "save" in text.lower():
            criteria.append("output persistito")

        if len(text) > 50:
            criteria.append("output sintetizzato")

        return criteria or ["output valido generato"]

    def _extract_constraints(self, text):
        constraints = []

        if "non" in text.lower():
            constraints.append("rispettare vincoli espliciti")

        constraints.append("no errori runtime")

        return constraints

    def _compute_priority(self, text):
        if any(k in text.lower() for k in ["urgente", "ora", "subito"]):
            return 1
        if len(text) > 80:
            return 2
        return 3

    def _detect_type(self, text):

        if "file" in text.lower() or "write" in text.lower():
            return "action"

        if "analizza" in text.lower() or "analyze" in text.lower():
            return "analysis"

        return "generation"