import os
from telethon import TelegramClient, events
from telethon.errors import MessageDeleteForbiddenError, ChatAdminRequiredError, UserAdminInvalidError

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
    async for message in client.iter_messages(chat_id, limit=None):
        if message.action:  # Detects system messages (user joined, left, etc.)
            try:
                # Only attempt to delete messages that are text and deletable
                if message.text:  # Check if the message has text content (system messages do)
                    await message.delete()
                    count += 1
                    print(f"Deleted system message: {str(message)}")
                else:
                    print(f"Skipped message (non-text or un-deletable): {str(message)}")
            except MessageDeleteForbiddenError:
                print(f"Error: Unable to delete message, deletion forbidden in chat {chat_id}")
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
        # Check if the action is either user joining (via link or manually) or user added
        if event.user_joined or event.user_added or event.user_left or event.user_kicked:
            # Log and delete the event for users entering via link or other actions
            print(f"Detected system action: {event}")
            await event.delete()  # Delete system message (user joined, left, etc.)
            print(f"✅ Deleted new system message in chat {event.chat_id}")
    except MessageDeleteForbiddenError:
        print(f"Error: Unable to delete new system message, deletion forbidden in chat {event.chat_id}")
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
