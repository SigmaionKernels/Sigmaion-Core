class GOAL_MANAGEMENT_SYSTEM:

    def parse(self, input_text):
        input_text = input_text.strip()

        return {
            "goal": input_text,
            "type": self._detect_type(input_text),
            "priority": self._priority(input_text),
            "success_criteria": self._success_criteria(input_text),
            "constraints": self._constraints(input_text)
        }

    def _detect_type(self, text):
        t = text.lower()

        if any(k in t for k in ["scrivi", "crea file", "salva", "write"]):
            return "action"

        if any(k in t for k in ["analizza", "study", "parse", "valuta"]):
            return "analysis"

        return "generation"

    def _priority(self, text):
        t = text.lower()

        if "urgente" in t or "critical" in t:
            return 1
        if "importante" in t:
            return 2

        return 3

    def _success_criteria(self, text):
        return [
            "task eseguiti senza errori",
            "output generato",
            "pipeline completata"
        ]

    def _constraints(self, text):
        return [
            "no crash AE",
            "no loop infinito",
            "execution bounded"
        ]