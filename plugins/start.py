from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FORCE_SUB_CHANNEL

# Force-subscribe check
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return member.status not in ("left", "kicked")
    except Exception:
        return False


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):

    # Check force-subscribe
    if not await is_subscribed(client, message.from_user.id):
        await message.reply_text(
            "🚫 You must join our updates channel to use this bot!",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url="https://t.me/Movies_Hub_OG")
                ]]
            )
        )
        return

    # Normal start message
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎬 Movie Updates", url=f"https://t.me/{FORCE_SUB_CHANNEL}")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
        ]
    )

    await message.reply_text(
        text=(
            "👋 **Welcome to Movies Hub Bot!**\n\n"
            "🎥 I provide movie files in multiple qualities.\n"
            "📢 Movies are posted in the update channel.\n\n"
            "Click **Get Files** on a movie post to receive files instantly 🚀"
        ),
        reply_markup=buttons,
        disable_web_page_preview=True
    )
