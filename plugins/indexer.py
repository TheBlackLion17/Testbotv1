from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import parse_movie
from database.movie_db import MovieDB
from info import *


movie_db = MovieDB()


@Client.on_message(filters.chat(DUMP_CHANNELS) & (filters.document | filters.video))
async def index_movies(client, message):


filename = (
message.document.file_name
if message.document else
message.video.file_name
)


title, year, quality = parse_movie(filename)
key = f"{title.lower()}_{year}"


await movie_db.add_file(
key=key,
chat_id=message.chat.id,
message_id=message.message_id
)


# create post only for first file of that movie+year
if not await movie_db.is_new(key):
return


keyboard = InlineKeyboardMarkup(
[[InlineKeyboardButton("🎯 Get Files", callback_data=f"movie|get|{key}")]]
)


await client.send_message(
MOVIE_UPDATE_CHANNEL,
text=f"""
🎬 **{title} ({year})**
🎞️ Multiple Qualities Available
📤 Uploaded by Movies Hub
""",
reply_markup=keyboard
)
```python
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import parse_movie
from database.movie_db import MovieDB
from info import *


movie_db = MovieDB()


@Client.on_message(filters.chat(DUMP_CHANNELS) & (filters.document | filters.video))
async def index_movies(client, message):


filename = (
message.document.file_name
if message.document else
message.video.file_name
)


title, year, quality = parse_movie(filename)
key = f"{title.lower()}_{year}"


await movie_db.add_file(
key=key,
chat_id=message.chat.id,
message_id=message.message_id
)


if await movie_db.exists(key):
return


keyboard = InlineKeyboardMarkup(
[[InlineKeyboardButton("🎯 Get Files", callback_data=f"movie|get|{key}")]]
)


await client.send_message(
MOVIE_UPDATE_CHANNEL,
text=f"""
🎬 **{title} ({year})**
🎞️ Multiple Qualities Available
📤 Uploaded by Movies Hub
""",
reply_markup=keyboard
)
