from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URL  # updated name
from datetime import datetime, date

client = AsyncIOMotorClient(DATABASE_URL)  # updated here
db = client["bot_db"]
series_collection = db["series"]

# Store a file for File Bot
async def add_or_update_file(title, file_id, media_type, quality, file_date: date = date.today()):
    await series_collection.update_one(
        {"title": title, "date": file_date},
        {"$set": {
            "file_id": file_id,
            "media_type": media_type,
            "quality": quality,
            "date": file_date
        }},
        upsert=True
    )

# Flexible file lookup
async def get_file_by_payload_flexible(payload: str):
    file_data = await series_collection.find_one({"title": payload})
    if file_data:
        return file_data
    file_data = await series_collection.find_one({"title": {"$regex": f"^{payload}$", "$options": "i"}})
    if file_data:
        return file_data
    file_data = await series_collection.find_one({"title": {"$regex": payload, "$options": "i"}})
    return file_data
