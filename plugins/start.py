import os, re, json, base64, logging, random, asyncio

from Script import script
from database.users_chats_db import db
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

from info import (
    CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL,
    PICS, START_MESSAGE, SUPPORT_CHAT
)
from utils import temp

logger = logging.getLogger(__name__)

# ================= START MESSAGE ================= #

START_MESSAGE = """
👋 Hello {user} !

🎬 Welcome to {bot} 🍿  
Your ultimate destination for **Latest Movies & Series Updates**.

✨ What I can do for you:
• 📢 Instant movie update alerts  
• 🎞️ High-quality movie uploads  
• 🔎 Find related movies & series  
• ⚡ Fast & smooth experience  

📌 How to use:
1️⃣ Join our movie update channel  
2️⃣ Watch for new movie posts  
3️⃣ Click **🎯 Get Related Files**  
4️⃣ Enjoy all related content instantly  

💡 Tip: Add me to your group to enable auto-filtering.

🚀 Stay connected & enjoy unlimited entertainment!
"""

# ================= START HANDLER ================= #


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.chat.id
    old = insert(int(user_id))
    
    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None

    loading_sticker_message = await message.reply_sticker("CAACAgUAAxkBAAJZtmZSPxpeDEIwobQtSQnkeGbwNjsyAAJjDgACjPuwVS9WyYuOlsqENQQ")
    await asyncio.sleep(2)
    await loading_sticker_message.delete()
    
    text = f"""Hello {message.from_user.mention} \n\n➻ This Is An Advanced And Yet Powerful Rename Bot.\n\n➻ Using This Bot You Can Rename And Change Thumbnail Of Your Files.\n\n➻ You Can Also Convert Video To File Aɴᴅ File To Video.\n\n➻ This Bot Also Supports Custom Thumbnail And Custom Caption.\n\n<b>Bot Is Made By @AgsModsOG</b>"""
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", url="https://t.me/AgsModsOG"),
        InlineKeyboardButton("💬 Support", url="https://t.me/AgsModsOG")],
        [InlineKeyboardButton("🛠️ Help", callback_data='help'),
        InlineKeyboardButton("❤️‍🩹 About", callback_data='about')],
        [InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/ags_mods_bot")]
        ])
    
    await message.reply_photo(
        photo=START_PIC,
        caption=text,
        reply_markup=button,
        quote=True
        )
    return    
