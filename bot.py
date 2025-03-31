from telethon import TelegramClient, events

# Replace these with your actual credentials
api_id = 22116740  # Your API ID
api_hash = "9e98787f02048d5a7255bb22b8bf999b"  # Your API Hash
bot_token = "7820351897:AAGz08eHTCjpUn6me3D6By-4DpKqwh6S8vg"  # Your bot token

client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.ChatAction)
async def delete_system_messages(event):
    if event.user_joined or event.user_added:
        await event.delete()  # Deletes the join message

print("Bot is running...")
client.run_until_disconnected()
