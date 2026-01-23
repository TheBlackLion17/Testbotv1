from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URL
from datetime import datetime

client = AsyncIOMotorClient(DATABASE_URL)
db = client["bot_db"]
comments_collection = db["comments"]

async def save_comment(user_id: int, text: str):
    await comments_collection.insert_one({
        "user_id": user_id,
        "text": text,
        "date": datetime.utcnow()
    })

async def get_comments(user_id: int = None):
    query = {"user_id": user_id} if user_id else {}
    cursor = comments_collection.find(query)
    return [doc async for doc in cursor]
