from motor.motor_asyncio import AsyncIOMotorClient


class MovieDB:
def __init__(self, mongo_url):
self.client = AsyncIOMotorClient(mongo_url)
self.db = self.client.moviebot
self.col = self.db.movies


async def add_file(self, key, chat_id, message_id):
await self.col.update_one(
{"key": key},
{
"$addToSet": {"files": message_id},
"$setOnInsert": {"chat_id": chat_id}
},
upsert=True
)


async def exists(self, key):
return await self.col.find_one({"key": key}) is not None


async def get(self, key):
return await self.col.find_one({"key": key})
