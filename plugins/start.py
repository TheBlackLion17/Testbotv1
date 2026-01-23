from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FORCE_SUB_CHANNEL, PICS
# ================================
# Force-subscribe check
# ================================
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
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
        channel_url = "https://t.me/joinchat/XXXXXXX"

    # Buttons for users not subscribed
    not_sub_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Join Channel", url=channel_url)],
            [InlineKeyboardButton("🔄 Try Again", callback_data="try_again")]
        ]
    )

    # Buttons for subscribed users
    subscribed_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎬 Movie Updates", url=channel_url)],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
        ]
    )

    # Force-subscribe check
    if not await is_subscribed(client, message.from_user.id):
        await client.send_photo(
            chat_id=message.chat.id,
            photo=PICS,
            caption="🚫 You must join our updates channel to use this bot!",
            reply_markup=not_sub_buttons
        )
        return

    # Normal start message with photo
    await client.send_photo(
        chat_id=message.chat.id,
        photo=PICS,
        caption=(
            "👋 **Welcome to Movies Hub Bot!**\n\n"
            "🎥 I provide movie files in multiple qualities.\n"
            "📢 Movies are posted in the update channel.\n\n"
            "Click **Get Files** on a movie post to receive files instantly 🚀"
        ),
        reply_markup=subscribed_buttons
    )


# ================================
# Callback for Try Again button
# ================================
@Client.on_callback_query(filters.regex("^try_again$"))
async def try_again_cb(client, query):
    user_id = query.from_user.id
    if await is_subscribed(client, user_id):
        await query.answer("✅ You are now subscribed!", show_alert=True)
        await query.message.edit(
            text="🎉 You have joined the channel! You can now use the bot normally.",
            reply_markup=None
        )
    else:
        await query.answer("🚫 You are still not subscribed!", show_alert=True)
