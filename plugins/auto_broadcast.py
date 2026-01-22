from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from os import environ

 # bot to forward to

# Listen for new messages in monitored channels
@Client.on_message(filters.chat(CHANNELS))
async def movie_update_broadcast(client, message):
    if message.document or message.video or message.audio:
        file_name = message.document.file_name if message.document else (
                    message.video.file_name if message.video else message.audio.file_name)

        broadcast_text = f"""
🎬 Title : {file_name}
🎗️ Genre : Stage 5 Productions
🗓️ Year : 2025
🎫 OTT : 23rd January 2025
🔊 Language : 𝗛𝗶𝗻𝗱𝗶
🎞️ Quality : 𝗛𝗗𝗥𝗶𝗽
📤 Upload : 𝗠𝗼𝘃𝗶𝗲𝘀 𝗛𝘂𝗯
        """

        # Forward the actual file
        await client.forward_messages(
            chat_id=MOVIE_UPDATE_CHANNEL,
            from_chat_id=message.chat.id,
            message_ids=message.message_id
        )

        # Add inline button
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🎯 Get Related", callback_data=f"forward_{message.chat.id}_{message.message_id}")]
            ]
        )

        # Send the broadcast text with inline button
        await client.send_message(
            chat_id=MOVIE_UPDATE_CHANNEL,
            text=broadcast_text,
            reply_markup=keyboard
        )

# Handle button click
@Client.on_callback_query()
async def button_click(client, callback_query):
    data = callback_query.data

    if data.startswith("forward_"):
        _, chat_id, msg_id = data.split("_")
        chat_id = int(chat_id)
        msg_id = int(msg_id)

        # Forward the message to target bot
        forwarded_msg = await client.forward_messages(
            chat_id=TARGET_BOT_USERNAME,
            from_chat_id=chat_id,
            message_ids=msg_id
        )

        # Notify the user
        await callback_query.answer("✅ Request sent! Check the related content.", show_alert=True)
