import numpy as np
from core.memory import load_memory
from core.embedder import embed

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=3):

    data = load_memory()
    q_vec = embed(query)

    scored = []

    for item in data:
        score = cosine_similarity(q_vec, item["vector"])
        scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in scored[:top_k]]