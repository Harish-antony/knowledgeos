# KnowledgeOS — MVP (Milestone 1: Core RAG Loop)

Upload PDF/DOCX/TXT → ask questions → get answers with citations from your own documents.

## Stack
FastAPI + MongoDB (Motor) + sentence-transformers (local embeddings) + Emergent Universal LLM Key (`emergentintegrations`) + React (Vite).

## Architecture decisions
- **MongoDB, not Postgres/pgvector** — chunks stored as documents with an `embedding` array field.
- **In-app cosine similarity** — `services/vector_search.py` pulls a user's chunks and scores them with numpy at query time. Fine to ~10k chunks; swap in Atlas Vector Search or a dedicated vector DB when a workspace outgrows that.
- **Local embeddings** (`all-MiniLM-L6-v2` via sentence-transformers) — free, runs on your own server, no external key needed for embedding generation.
- **Google Gemini (free tier)** — used for the final answer-generation step (`services/llm.py`) via `google-generativeai`. Get a free key at aistudio.google.com — no credit card needed, generous daily quota. Swapped in from the Emergent Universal Key to avoid credit costs; if you want to switch providers later (paid OpenAI/Claude, or back to Emergent), only `services/llm.py` needs to change.
- **Auth**: email/password, bcrypt-hashed, stored in MongoDB, JWT bearer tokens — no external auth provider.

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in MONGO_URL and GEMINI_API_KEY (free, from aistudio.google.com)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env   # set VITE_BACKEND_URL
npm run dev
```

## What's built (Milestone 1)
- Register/login (JWT)
- Upload PDF/DOCX/TXT → text extraction → chunking → local embedding → MongoDB storage
- Ask a question → in-app cosine similarity search → top-5 chunks → Emergent LLM answers with citations
- Minimal single-page workspace: document sidebar + chat panel

## Deliberately deferred to later milestones
Landing page, dark-mode toggle UI (page is dark by default, just not themeable yet), analytics, admin dashboard, workspace/multi-member support, streaming responses, chat history sidebar, semantic search page separate from chat.

## Next milestone
Confirm this loop works end-to-end for you (upload a real doc, ask a real question), then we layer on the next module.
