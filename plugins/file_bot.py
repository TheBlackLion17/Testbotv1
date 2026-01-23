from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.posted_db import get_file_by_payload_flexible
from Script import script
from info import PICS

@Client.on_message(filters.private & filters.command("start"))
async def file_bot_start(client, message):
    args = message.text.split(maxsplit=1)

    # -------------------------
    # Case 1: User clicked a filter button with payload
    # -------------------------
    if len(args) > 1:
        payload = args[1]
        file_data = await get_file_by_payload_flexible(payload)

        if file_data:
            caption = f"✅ {file_data['title']}\n⚡ Quality: {file_data.get('quality','Unknown')}"
            if file_data["media_type"] == "document":
                await client.send_document(chat_id=message.chat.id, document=file_data["file_id"], caption=caption)
            elif file_data["media_type"] == "video":
                await client.send_video(chat_id=message.chat.id, video=file_data["file_id"], caption=caption)
            return

        await message.reply_text("⚠ Sorry, the file was not found in the database.")
        return

    # -------------------------
    # Case 2: Normal /start without payload
    # -------------------------
    # Get start text & pic
    start_text = script.START_TXT.format(message.from_user.first_name, "Welcome!")
    start_pic = PICS[0] if isinstance(PICS, list) else PICS

    # Optional buttons
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/YourChannel")],
            [InlineKeyboardButton("💬 Send a Comment", url=f"https://t.me/{client.username}?start=comment")]
        ]
    )

    # Send photo with caption and buttons
    await client.send_photo(
        chat_id=message.chat.id,
        photo=start_pic,
        caption=start_text,
        reply_markup=buttons
    )
