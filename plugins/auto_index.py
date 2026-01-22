from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import CHANNELS, MOVIE_UPDATE_CHANNEL, TARGET_BOT

@Client.on_message(filters.chat(CHANNELS) & filters.media)
async def auto_broadcast(bot, message):

    media_type = message.media
    if media_type not in (
        enums.MessageMediaType.DOCUMENT,
        enums.MessageMediaType.VIDEO,
        enums.MessageMediaType.AUDIO
    ):
        return

    media = getattr(message, media_type.value, None)
    if not media or not media.file_name:
        return

    file_name = media.file_name

    # 🔹 Extract title (simple logic – you can improve later)
    title = file_name.rsplit(".", 1)[0]

    caption = f"""
🎬 <b>New Movie Uploaded</b>

🎞️ <b>Title:</b> {title}
📦 <b>Quality:</b> HDRip
🔊 <b>Language:</b> Hindi
📤 <b>Source:</b> Movies Hub
"""

    # 🔘 Inline button → opens another bot
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "🔍 Get Movie Files",
                url=f"https://t.me/{TARGET_BOT}?start={title.replace(' ', '_')}"
            )
        ]]
    )

    await bot.send_message(
        chat_id=MOVIE_UPDATE_CHANNEL,
        text=caption,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True
    )
