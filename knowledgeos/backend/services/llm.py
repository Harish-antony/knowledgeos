import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are KnowledgeOS, an internal company knowledge assistant.
Answer the user's question using ONLY the provided document excerpts below.
If the excerpts don't contain enough information to answer, say so clearly —
do not make up an answer. Keep answers concise and reference which excerpt
(by number) supports each claim, like [1], [2]."""

# gemini-2.0-flash: free tier via Google AI Studio (aistudio.google.com),
# no credit card required. Generous daily free quota, good enough for MVP testing.
_model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=SYSTEM_PROMPT,
)


async def generate_answer(question: str, chunks: list[dict], session_id: str | None) -> str:
    context = "\n\n".join(
        f"[{i+1}] (from {c['filename']}): {c['chunk_text']}" for i, c in enumerate(chunks)
    )
    prompt = f"Document excerpts:\n{context}\n\nQuestion: {question}"

    response = await _model.generate_content_async(prompt)
    return response.text