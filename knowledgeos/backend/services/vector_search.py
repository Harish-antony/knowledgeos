from db import chunks_col
from services.embeddings import embed_query, cosine_similarity


async def search_relevant_chunks(user_id: str, question: str, top_k: int = 5) -> list[dict]:
    """
    MVP vector search: pull the user's chunks, score them in-app with cosine
    similarity. Fine up to ~10k chunks; migrate to Atlas Vector Search or a
    dedicated vector DB when a workspace crosses that scale.
    """
    query_embedding = embed_query(question)

    cursor = chunks_col.find({"user_id": user_id})
    scored = []
    async for chunk in cursor:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    return [
        {
            "document_id": c["document_id"],
            "filename": c["filename"],
            "chunk_text": c["text"],
            "score": round(score, 4),
        }
        for score, c in top
    ]
