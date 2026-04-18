from core.engine import SISS_ENGINE
from core.memory import store_memory
from core.retriever import retrieve
from core.memory_compressor import compress_memory

from core.executor import ACTION_EXECUTOR
from core.gms import GOAL_MANAGEMENT_SYSTEM
from core.msp import MULTI_STEP_PLANNER
from core.vfs import VALIDATION_FEEDBACK_SYSTEM


class SISS_AGENT:

    def __init__(self):
        self.engine = SISS_ENGINE()
        self.executor = ACTION_EXECUTOR()
        self.gms = GOAL_MANAGEMENT_SYSTEM()
        self.msp = MULTI_STEP_PLANNER()
        self.vfs = VALIDATION_FEEDBACK_SYSTEM()

        self.step_count = 0

    def step(self, input_text):

        # 1. RETRIEVAL
        context = retrieve(input_text)

        # 2. CORE ENGINE
        reasoning = self.engine.process(input_text)

        # 3. GOAL SYSTEM
        goal = self.gms.parse(input_text)

        # 4. PLANNING
        tasks = self.msp.plan(goal)

        # 5. EXECUTION
        results = []

        for task in tasks:
            result = self.executor.execute(task)
            results.append({
                "task": task,
                "result": result
            })

        # 6. VALIDATION
        vfs_result = self.vfs.evaluate(goal, results)

        # 7. MEMORY
        store_memory(input_text, {
            "reasoning": reasoning,
            "goal": goal,
            "tasks": tasks,
            "execution": results,
            "vfs": vfs_result
        })

        # 8. COMPRESSION
        self.step_count += 1
        compression = None

        if self.step_count % 10 == 0:
            compression = compress_memory()

        return {
            "input": input_text,
            "context": context,
            "reasoning": reasoning,
            "goal": goal,
            "tasks": tasks,
            "execution": results,
            "vfs": vfs_result,
            "compression": compression
        }