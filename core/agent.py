from core.engine import SISS_ENGINE
from core.memory import store_memory
from core.retriever import retrieve
from core.memory_compressor import compress_memory

from core.executor import ACTION_EXECUTOR
from core.gms import GOAL_MANAGEMENT_SYSTEM


class SISS_AGENT:

    def __init__(self):
        self.engine = SISS_ENGINE()
        self.executor = ACTION_EXECUTOR()
        self.gms = GOAL_MANAGEMENT_SYSTEM()

        self.step_count = 0

    # -------------------------
    # MSP MINIMALE (TEMPORANEO)
    # -------------------------
    def build_task(self, goal_text):
        """
        Planner semplificato: 1 goal → 1 task operativo
        (placeholder in attesa MSP completo)
        """

        if "file" in goal_text.lower() or "scrivi" in goal_text.lower():
            return {
                "tool": "write_file",
                "params": {
                    "path": "output/auto.txt",
                    "content": goal_text
                }
            }

        if "leggi" in goal_text.lower() or "read" in goal_text.lower():
            return {
                "tool": "read_file",
                "params": {
                    "path": "output/auto.txt"
                }
            }

        if "cmd" in goal_text.lower() or "run" in goal_text.lower():
            return {
                "tool": "run_command",
                "params": {
                    "command": "echo SISS_EXEC"
                }
            }

        # fallback
        return {
            "tool": "write_file",
            "params": {
                "path": "output/log.txt",
                "content": goal_text
            }
        }

    # -------------------------
    # CICLO PRINCIPALE
    # -------------------------
    def step(self, input_text):

        # 1. RETRIEVAL
        context = retrieve(input_text)

        # 2. CORE ENGINE (ragionamento)
        reasoning = self.engine.process(input_text)

        # 3. GOAL MANAGEMENT SYSTEM (GMS)
        goal = self.gms.parse(input_text)

        # 4. MSP (semplificato)
        task = self.build_task(goal["goal"])

        # 5. EXECUTOR (AE)
        execution_result = self.executor.execute(task)

        # 6. MEMORY STORE
        store_memory(input_text, {
            "reasoning": reasoning,
            "goal": goal,
            "task": task,
            "execution": execution_result
        })

        # 7. COMPRESSIONE PERIODICA
        self.step_count += 1
        compression = None

        if self.step_count % 10 == 0:
            compression = compress_memory()

        # 8. OUTPUT
        return {
            "input": input_text,
            "context": context,
            "reasoning": reasoning,
            "goal": goal,
            "task": task,
            "execution": execution_result,
            "compression": compression
        }

    # -------------------------
    # LOOP INTERATTIVO
    # -------------------------
    def loop(self):
        while True:
            user_input = input("SISS> ")

            if user_input.lower() in ["exit", "quit"]:
                break

            result = self.step(user_input)

            print("\n--- OUTPUT ---")
            print(result)
            print("\n")