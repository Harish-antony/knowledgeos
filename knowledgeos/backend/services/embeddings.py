import numpy as np
from sentence_transformers import SentenceTransformer

# Loaded once at startup — free, local, no external API needed.
# all-MiniLM-L6-v2: 384 dims, fast, good enough for MVP-scale semantic search.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = _model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def embed_query(text: str) -> list[float]:
    return _model.encode([text], normalize_embeddings=True)[0].tolist()


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr, b_arr = np.array(a), np.array(b)
    # Embeddings are already normalized, so dot product == cosine similarity
    return float(np.dot(a_arr, b_arr))
