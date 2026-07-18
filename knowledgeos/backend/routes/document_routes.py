import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from db import documents_col, chunks_col
from auth import get_current_user_id
from services.document_processing import extract_text, chunk_text
from services.embeddings import embed_texts
from models.schemas import DocumentOut

router = APIRouter(prefix="/api/documents", tags=["documents"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_FILE_SIZE_MB = 20


@router.post("", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...), user_id: str = Depends(get_current_user_id)
):
    ext = file.filename.lower().split(".")[-1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds {MAX_FILE_SIZE_MB}MB limit")

    document_id = str(uuid.uuid4())
    doc_record = {
        "id": document_id,
        "user_id": user_id,
        "filename": file.filename,
        "file_type": ext,
        "status": "processing",
        "chunk_count": 0,
        "uploaded_at": datetime.utcnow(),
    }
    await documents_col.insert_one(doc_record)

    try:
        text = extract_text(file.filename, content)
        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("No extractable text found in document")

        embeddings = embed_texts(chunks)
        chunk_docs = [
            {
                "id": str(uuid.uuid4()),
                "document_id": document_id,
                "user_id": user_id,
                "filename": file.filename,
                "text": chunk,
                "embedding": embedding,
                "chunk_index": i,
            }
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
        ]
        await chunks_col.insert_many(chunk_docs)

        await documents_col.update_one(
            {"id": document_id},
            {"$set": {"status": "ready", "chunk_count": len(chunks)}},
        )
        doc_record["status"] = "ready"
        doc_record["chunk_count"] = len(chunks)
    except Exception as e:
        await documents_col.update_one(
            {"id": document_id}, {"$set": {"status": "failed", "error": str(e)}}
        )
        raise HTTPException(status_code=422, detail=f"Failed to process document: {e}")

    return DocumentOut(**doc_record)


@router.get("", response_model=list[DocumentOut])
async def list_documents(user_id: str = Depends(get_current_user_id)):
    docs = await documents_col.find({"user_id": user_id}).sort("uploaded_at", -1).to_list(200)
    return [DocumentOut(**d) for d in docs]


@router.delete("/{document_id}")
async def delete_document(document_id: str, user_id: str = Depends(get_current_user_id)):
    doc = await documents_col.find_one({"id": document_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await documents_col.delete_one({"id": document_id})
    await chunks_col.delete_many({"document_id": document_id})
    return {"ok": True}
