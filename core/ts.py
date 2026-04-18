import threading
import time


class TEMPORAL_SCHEDULER:

    def __init__(self, agent, interval=5):
        self.agent = agent
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self, seed_input="auto"):

        if self.running:
            return {"status": "already_running"}

        self.running = True

        def loop():
            current_input = seed_input

            while self.running:

                try:
                    result = self.agent.step(current_input)

                    print("\n[TS LOOP OUTPUT]")
                    print(result)

                    # feedback loop semplice (auto-evoluzione input)
                    goal = result.get("goal", {})
                    current_input = goal.get("goal", seed_input)

                except Exception as e:
                    print("[TS ERROR]", str(e))

                time.sleep(self.interval)

        self.thread = threading.Thread(target=loop, daemon=True)
        self.thread.start()

        return {"status": "started"}

    def stop(self):
        self.running = False
        return {"status": "stopped"}