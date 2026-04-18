from core.engine import SISS_ENGINE
from core.memory import store_memory
from core.retriever import retrieve
from core.memory_compressor import compress_memory


class SISS_AGENT:

    def __init__(self):
        self.engine = SISS_ENGINE()
        self.step_count = 0

    def step(self, input_text):

        # 1. Recupero contesto semantico
        context = retrieve(input_text)

        # 2. Elaborazione core engine (pipeline + truth + complexity)
        result = self.engine.process(input_text)

        # 3. Persistenza memoria (RAG store)
        store_memory(input_text, result)

        # 4. Contatore cicli agent
        self.step_count += 1

        # 5. Compressione periodica memoria (riduzione entropia)
        compression = None
        if self.step_count % 10 == 0:
            compression = compress_memory()

        # 6. Output strutturato agente
        return {
            "input": input_text,
            "context": context,
            "result": result,
            "compression": compression,
            "step": self.step_count
        }

    def loop(self):
        while True:
            user_input = input("AGENT> ")

            if user_input.strip().lower() == "exit":
                break

            output = self.step(user_input)

            print(output)