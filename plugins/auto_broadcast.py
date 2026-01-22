from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS
from os import environ

MOVIE_UPDATE_CHANNEL = int(environ.get("MOVIE_UPDATE_CHANNEL", "0"))
TARGET_BOT = environ.get("TARGET_BOT_USERNAME")  # without @

@Client.on_message(filters.chat(CHANNELS))
async def auto_movie_broadcast(client, message):

    if not (message.document or message.video or message.audio):
        return

    title = (
        message.document.file_name
        if message.document else
        message.video.file_name
        if message.video else
        "New Movie"
    )

    media_group_id = message.media_group_id or "single"

    text = f"""
🎬 Title : {title}
🎗️ Genre : Stage 5 Productions
🗓️ Year : 2025
🎫 OTT : 23rd January 2025
🔊 Language : Hindi
🎞️ Quality : HDRip
📤 Upload : Movies Hub
"""

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "🎯 Get Related Files",
                callback_data=f"sendall|{message.chat.id}|{media_group_id}"
            )
        ]]
    )

    await client.send_message(
        chat_id=MOVIE_UPDATE_CHANNEL,
        text=text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^sendall"))
async def send_all_files(client, query):

    _, chat_id, group_id = query.data.split("|")
    chat_id = int(chat_id)

    await query.answer("📤 Sending all files…", show_alert=False)

    if group_id == "single":
        # Send last message only
        await client.forward_messages(
            chat_id=TARGET_BOT,
            from_chat_id=chat_id,
            message_ids=query.message.reply_to_message.message_id
        )
        return

    # Fetch all messages in media group
    messages = []
    async for msg in client.get_chat_history(chat_id, limit=50):
        if msg.media_group_id == group_id:
            messages.append(msg.message_id)

    if messages:
        await client.forward_messages(
            chat_id=TARGET_BOT,
            from_chat_id=chat_id,
            message_ids=messages
        )
