# plugins/commands.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import *

@Client.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", url="https://t.me/YourChannel")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help"),
         InlineKeyboardButton("👤 Settings", callback_data="settings")]
    ])
    
    await message.reply_photo(
        photo=PIC,
        caption=f"""
👋 Hello {message.from_user.mention}!

I am a high-speed 🔁 file renamer bot.
Send me any file and I'll rename it for you instantly.

""",
        reply_markup=btn
    )


@Client.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text("""
ℹ️ **How to Use:**
1. Send any video, document, or audio file.
2. I’ll ask for the new file name.
3. I’ll rename it and send it back — fast!

📌 Commands:
- `/start` - Show main menu
- `/help` - Show this help
- `/set_caption` - Set a custom caption
- `/view_caption` - View your current caption
- `/del_caption` - Delete your caption
- `/set_thumbnail` - Send photo to set thumbnail
- `/view_thumbnail` - Show saved thumbnail
- `/del_thumbnail` - Delete thumbnail
""", disable_web_page_preview=True)
