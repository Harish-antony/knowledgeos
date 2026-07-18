import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import chat_sessions_col, messages_col
from auth import get_current_user_id
from services.vector_search import search_relevant_chunks
from services.llm import generate_answer
from models.schemas import ChatRequest, ChatResponse, Citation

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def ask_question(body: ChatRequest, user_id: str = Depends(get_current_user_id)):
    session_id = body.session_id or str(uuid.uuid4())

    session = await chat_sessions_col.find_one({"id": session_id, "user_id": user_id})
    if not session:
        await chat_sessions_col.insert_one(
            {
                "id": session_id,
                "user_id": user_id,
                "title": body.question[:60],
                "created_at": datetime.utcnow(),
            }
        )

    relevant_chunks = await search_relevant_chunks(user_id, body.question, top_k=5)
    if not relevant_chunks:
        raise HTTPException(
            status_code=400,
            detail="No documents found. Upload documents before asking questions.",
        )

    try:
        answer = await generate_answer(body.question, relevant_chunks, session_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")

    await messages_col.insert_many(
        [
            {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "user_id": user_id,
                "role": "user",
                "content": body.question,
                "created_at": datetime.utcnow(),
            },
            {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "user_id": user_id,
                "role": "assistant",
                "content": answer,
                "citations": relevant_chunks,
                "created_at": datetime.utcnow(),
            },
        ]
    )

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        citations=[Citation(**c) for c in relevant_chunks],
    )


@router.get("/{session_id}/messages")
async def get_messages(session_id: str, user_id: str = Depends(get_current_user_id)):
    msgs = await messages_col.find({"session_id": session_id, "user_id": user_id}).sort(
        "created_at", 1
    ).to_list(500)
    for m in msgs:
        m.pop("_id", None)
    return {"messages": msgs}


@router.get("/sessions")
async def list_sessions(user_id: str = Depends(get_current_user_id)):
    sessions = await chat_sessions_col.find({"user_id": user_id}).sort(
        "created_at", -1
    ).to_list(100)
    for s in sessions:
        s.pop("_id", None)
    return {"sessions": sessions}