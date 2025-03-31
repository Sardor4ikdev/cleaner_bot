import os
from telethon import TelegramClient, events

# Load environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.ChatAction)
async def delete_system_messages(event):
    if event.user_joined or event.user_added:
        await event.delete()  # Deletes "User joined the group" message
    elif event.user_left or event.user_kicked:
        await event.delete()  # Deletes "User left the group" message

print("Bot is running on Railway...")
client.run_until_disconnected()
