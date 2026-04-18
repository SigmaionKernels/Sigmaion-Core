import numpy as np
from core.memory import load_memory, save_memory


def relevance_score(item):
    """
    Stima grezza della rilevanza del record.
    Più lungo non significa migliore, ma qui serve come proxy iniziale.
    """

    text_len = len(item.get("text", ""))
    output_len = len(str(item.get("output", "")))

    return (text_len * 0.01) + (output_len * 0.01)


def redundancy_score(item, memory):
    """
    Conta quante volte un input simile è già presente.
    Versione semplice: match esatto sul testo.
    """

    count = 0

    for m in memory:
        if m.get("text") == item.get("text"):
            count += 1

    return count - 1  # esclude sé stesso


def entropy_penalty(item):
    """
    Penalità base per output troppo "rumoroso" o non strutturato.
    """

    output = str(item.get("output", ""))

    # proxy semplice: caratteri non alfanumerici
    noise = sum(
        1 for c in output
        if not c.isalnum() and c not in " .,-_"
    )

    return noise * 0.005


def compression_score(item, memory):
    """
    Score finale di sopravvivenza del record.
    """

    rel = relevance_score(item)
    red = redundancy_score(item, memory)
    ent = entropy_penalty(item)

    return rel - (0.3 * red) - ent


def compress_memory(threshold=0.5):
    """
    Processo di pruning della memoria:
    - valuta ogni record
    - elimina quelli sotto soglia
    - riscrive memoria compressa
    """

    memory = load_memory()

    if not memory:
        return {
            "before": 0,
            "after": 0,
            "removed": 0
        }

    compressed = []

    for item in memory:
        score = compression_score(item, memory)

        if score >= threshold:
            compressed.append(item)

    save_memory(compressed)

    return {
        "before": len(memory),
        "after": len(compressed),
        "removed": len(memory) - len(compressed),
        "threshold": threshold
    }