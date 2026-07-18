import os
from motor.motor_asyncio import AsyncIOMotorClient
import certifi

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ.get("DB_NAME", "knowledgeos")

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
db = client[DB_NAME]

# Collections
users_col = db["users"]
documents_col = db["documents"]
chunks_col = db["chunks"]
chat_sessions_col = db["chat_sessions"]
messages_col = db["messages"]
