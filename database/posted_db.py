from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URL
from datetime import datetime

client = AsyncIOMotorClient(DATABASE_URL)
db = client["bot_db"]
series_collection = db["series"]

# Series tracking
async def get_series(series_name: str, date: datetime.date):
    return await series_collection.find_one({"series_name": series_name, "date": date})

async def add_or_update_series(series_name: str, episodes: list, quality: str, date: datetime.date):
    await series_collection.update_one(
        {"series_name": series_name, "date": date},
        {"$set": {"episodes": episodes, "quality": quality, "sent": False}},
        upsert=True
    )

async def mark_series_sent(series_name: str, date: datetime.date):
    await series_collection.update_one(
        {"series_name": series_name, "date": date},
        {"$set": {"sent": True}}
    )

# File Bot storage
async def add_or_update_file(title, file_id, media_type, quality, date):
    await series_collection.update_one(
        {"title": title, "date": date},
        {"$set": {"file_id": file_id, "media_type": media_type, "quality": quality}},
        upsert=True
    )

async def get_file_by_payload(payload):
    return await series_collection.find_one({"title": payload})
