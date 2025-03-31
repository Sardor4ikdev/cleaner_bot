import os
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, ChatAdminRequiredError, UserAdminInvalidError

# Load environment variables safely
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

if not all([api_id, api_hash, bot_token]):
    raise ValueError("API_ID, API_HASH, or BOT_TOKEN is missing in environment variables.")

api_id = int(api_id)  # Convert API_ID to integer safely

client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

async def delete_past_system_messages(chat_id):
    """Deletes all system messages from the beginning of the group."""
    count = 0
    async for message in client.iter_messages(chat_id):
        if message.action:  # Detects system messages (user joined, left, etc.)
            try:
                await message.delete()
                count += 1
                print(f"Deleted system message: {str(message)}")
            except ChatAdminRequiredError:
                print(f"Error: Bot does not have permission to delete messages in chat {chat_id}")
                break
            except UserAdminInvalidError:
                print(f"Error: Bot's admin rights are invalid in chat {chat_id}")
                break
            except Exception as e:
                print(f"Error deleting message: {e}")
    print(f"✅ Deleted {count} system messages in chat {chat_id}")

@client.on(events.ChatAction)
async def delete_new_system_messages(event):
    """Deletes new system messages as they appear."""
    try:
        if event.user_joined or event.user_added or event.user_left or event.user_kicked:
            await event.delete()
            print(f"✅ Deleted new system message in chat {event.chat_id}")
    except ChatAdminRequiredError:
        print(f"Error: Bot does not have permission to delete messages in chat {event.chat_id}")
    except UserAdminInvalidError:
        print(f"Error: Bot's admin rights are invalid in chat {event.chat_id}")
    except Exception as e:
        print(f"⚠ Error deleting new system message: {e}")

@client.on(events.NewMessage(pattern="/clean"))
async def clean_old_system_messages(event):
    """Command handler: Deletes all past system messages when the bot admin sends /clean."""
    chat = await event.get_chat()
    await event.reply("🧹 Cleaning system messages...")
    await delete_past_system_messages(chat.id)
    await event.reply("✅ All system messages deleted!")

print("🚀 Bot is running on Railway...")
client.run_until_disconnected()
