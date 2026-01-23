from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FORCE_SUB_CHANNEL

# ================================
# Force-subscribe check function
# ================================
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        # Log user status for debugging
        print(f"[ForceSub] User {user_id} status: {member.status}")
        return member.status not in ("left", "kicked")
    except Exception as e:
        print(f"[ForceSub Error] {e}")
        return False


# ================================
# /start command
# ================================
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):

    # Determine join channel URL dynamically
    if isinstance(FORCE_SUB_CHANNEL, str):
        channel_url = f"https://t.me/{FORCE_SUB_CHANNEL}"
    else:
        # For private channels, replace with your invite link
        channel_url = "https://t.me/Movies_Hub_OG"

    # Check force-subscribe
    if not await is_subscribed(client, message.from_user.id):
        await message.reply_text(
            "🚫 You must join our updates channel to use this bot!",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url=channel_url
                    )
                ]]
            )
        )
        return

    # Normal start message
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎬 Movie Updates", url=channel_url)],
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
