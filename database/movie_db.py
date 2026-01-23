from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URL, DATABASE_NAME


class MovieDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(DATABASE_URL)
        self.db = self.client[DATABASE_NAME]
        self.col = self.db.movies

    # 🔹 Add file to movie (same name + year → same key)
    async def add_file(self, key: str, title: str, year: str, chat_id: int, message_id: int):
        await self.col.update_one(
            {"key": key},
            {
                "$setOnInsert": {
                    "key": key,
                    "title": title,
                    "year": year,
                    "chat_id": chat_id
                },
                "$addToSet": {
                    "files": message_id
                }
            },
            upsert=True
        )

    # 🔹 Check if movie already exists
    async def exists(self, key: str) -> bool:
        movie = await self.col.find_one({"key": key})
        return movie is not None

    # 🔹 Get movie data
    async def get(self, key: str):
        return await self.col.find_one({"key": key})

    # 🔹 Get all movies (optional – admin/stats)
    async def get_all(self):
        return self.col.find({})

    # 🔹 Delete a movie (admin use)
    async def delete(self, key: str):
        await self.col.delete_one({"key": key})

    # 🔹 Count total movies
    async def count(self) -> int:
        return await self.col.count_documents({})


# ✅ Global instance (import this everywhere)
movie_db = MovieDB()
