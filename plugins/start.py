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
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('• ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴜʀ ᴄʜᴀᴛ •', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('• ᴍᴀsᴛᴇʀ •', url="https://t.me/AgsModsOG"),
                    InlineKeyboardButton('• sᴜᴘᴘᴏʀᴛ •', url='https://t.me/AgsModsOG')
                ],[
                    InlineKeyboardButton('• ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ •', url="https://t.me/AgsModsOG")
                  ]]
        await message.reply(START_MESSAGE.format(user=message.from_user.mention if message.from_user else message.chat.title, bot=temp.B_LINK), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)                    
        await asyncio.sleep(2) 
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(a=message.chat.title, b=message.chat.id, c=message.chat.username, d=total, f=temp.B_LINK, e="Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title, message.chat.username)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention, message.from_user.username, temp.U_NAME))
    if len(message.command) != 2:
        buttons = [[
                    InlineKeyboardButton('• ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴜʀ ᴄʜᴀᴛ •', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('• ᴍᴀsᴛᴇʀ •', url="https://t.me/AgsModsOG"),
                    InlineKeyboardButton('• sᴜᴘᴘᴏʀᴛ •', url='https://t.me/AgsModsOG')
                ],[
                    InlineKeyboardButton('• ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ •', url="https://t.me/AgsModsOG")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        m=await message.reply_sticker("CAACAgUAAxkBAAEBfxNojk--UvtbpB5AiG9bDdYw4EOFMwACGxkAAvHLcVTiDQsdjHCtZjYE")
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=START_MESSAGE.format(user=message.from_user.mention, bot=temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🤖 Join Updates Channel", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton(" 🔄 Try Again", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text=FORCE_SUB_TEXT,
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.DEFAULT
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
                    InlineKeyboardButton('• ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴜʀ ᴄʜᴀᴛ •', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('• ᴍᴀsᴛᴇʀ •', url="https://t.me/AgsModsOG"),
                    InlineKeyboardButton('• sᴜᴘᴘᴏʀᴛ •', url='https://t.me/AgsModsOG')
                ],[
                    InlineKeyboardButton('• ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ •', url="https://t.me/AgsModsOG")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        m=await message.reply_sticker("CAACAgUAAxkBAAEBfxNojk--UvtbpB5AiG9bDdYw4EOFMwACGxkAAvHLcVTiDQsdjHCtZjYE")
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=START_MESSAGE.format(user=message.from_user.mention, bot=temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
