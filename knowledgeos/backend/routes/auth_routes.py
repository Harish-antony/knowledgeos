import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from db import users_col
from auth import hash_password, verify_password, create_access_token
from models.schemas import RegisterRequest, LoginRequest, AuthResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(body: RegisterRequest):
    existing = await users_col.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "email": body.email,
        "full_name": body.full_name,
        "password_hash": hash_password(body.password),
        "created_at": datetime.utcnow(),
    }
    await users_col.insert_one(user_doc)

    token = create_access_token(user_id)
    return AuthResponse(
        token=token,
        user={"id": user_id, "email": body.email, "full_name": body.full_name},
    )


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest):
    user = await users_col.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user["id"])
    return AuthResponse(
        token=token,
        user={"id": user["id"], "email": user["email"], "full_name": user["full_name"]},
    )
