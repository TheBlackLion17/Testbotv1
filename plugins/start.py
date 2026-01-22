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

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):

    # ---------- GROUP / SUPERGROUP ---------- #
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:

        buttons = [
            [
                InlineKeyboardButton(
                    "📢 Updates",
                    url=f"https://t.me/{SUPPORT_CHAT}"
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ Help",
                    url=f"https://t.me/{temp.U_NAME}?start=help"
                )
            ]
        ]

        await message.reply(
            text=START_MESSAGE.format(
                user=message.from_user.mention if message.from_user else message.chat.title,
                bot=client.mention
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )

        await asyncio.sleep(2)

        if not await db.get_chat(message.chat.id):
            total = await client.get_chat_members_count(message.chat.id)

            await client.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT_G.format(
                    a=message.chat.title,
                    b=message.chat.id,
                    c=message.chat.username,
                    d=total,
                    e="Unknown",
                    f=client.mention
                )
            )

            await db.add_chat(
                message.chat.id,
                message.chat.title,
                message.chat.username
            )
        return

    # ---------- PRIVATE CHAT ---------- #
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(
            message.from_user.id,
            message.from_user.first_name
        )

        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(
                message.from_user.id,
                message.from_user.mention,
                message.from_user.username,
                temp.U_NAME
            )
        )

    # ---------- NORMAL START ---------- #
    if len(message.command) != 2:

        buttons = [
            [
                InlineKeyboardButton(
                    "➕ Add Me To Your Group",
                    url=f"https://t.me/{temp.U_NAME}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔎 Search",
                    switch_inline_query_current_chat=""
                ),
                InlineKeyboardButton(
                    "🔈 Channel",
                    url="https://t.me/mkn_bots_updates"
                )
            ],
            [
                InlineKeyboardButton(
                    "🕸️ Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    "✨ About",
                    callback_data="about"
                )
            ]
        ]

        sticker = await message.reply_sticker(
            "CAACAgUAAxkBAAEBvlVk7YKnYxIHVnKW2PUwoibIR2ygGAACBAADwSQxMYnlHW4Ls8gQHgQ"
        )

        await asyncio.sleep(2)

        await message.reply_photo(
            photo=random.choice(PICS),
            caption=START_MESSAGE.format(
                user=message.from_user.mention,
                bot=client.mention
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

        return await sticker.delete()
