from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.movie_db import MovieDB
from info import FORCE_SUB_CHANNEL

movie_db = MovieDB()


async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return member.status not in ("left", "kicked")
    except Exception:
        return False


@Client.on_callback_query(filters.regex("^movie\\|get"))
async def send_movie_files(client, query):

    _, _, key = query.data.split("|")

    if not await is_subscribed(client, query.from_user.id):
        await query.answer("Join channel first", show_alert=True)
        await query.message.reply(
            "🚫 **You must join our channel to get files**",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url="https://t.me/YourChannel"
                    )
                ]]
            )
        )
        return

    data = await movie_db.get(key)

    if not data:
        await query.answer("Files not found", show_alert=True)
        return

    await query.answer("📤 Sending files...", show_alert=False)

    await client.forward_messages(
        chat_id=query.from_user.id,
        from_chat_id=data["chat_id"],
        message_ids=data["files"]
    )
