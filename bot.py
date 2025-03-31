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

# Debugging the chat action events
@client.on(events.ChatAction)
async def delete_system_messages(event):
    """Deletes system messages for user join, user added, user left, user kicked actions."""
    try:
        # Logging every detected event for debugging
        print(f"Detected event: {event}")
        
        if event.user_joined:  # When a user joins the group
            print(f"User joined: {event.user_id}")
            await event.delete()  # Attempt to delete the "user joined" message
            print(f"✅ Deleted user joined message in chat {event.chat_id}")

        elif event.user_added:  # When a user is added to the group manually
            print(f"User added: {event.user_id}")
            await event.delete()  # Attempt to delete the "user added" message
            print(f"✅ Deleted user added message in chat {event.chat_id}")

        elif event.user_left:  # When a user leaves the group
            print(f"User left: {event.user_id}")
            await event.delete()  # Attempt to delete the "user left" message
            print(f"✅ Deleted user left message in chat {event.chat_id}")

        elif event.user_kicked:  # When a user is kicked from the group
            print(f"User kicked: {event.user_id}")
            await event.delete()  # Attempt to delete the "user kicked" message
            print(f"✅ Deleted user kicked message in chat {event.chat_id}")

    except MessageDeleteForbiddenError:
        print(f"❌ Error: Unable to delete system message, deletion forbidden in chat {event.chat_id}")
    except ChatAdminRequiredError:
        print(f"❌ Error: Bot does not have permission to delete messages in chat {event.chat_id}")
    except UserAdminInvalidError:
        print(f"❌ Error: Bot's admin rights are invalid in chat {event.chat_id}")
    except Exception as e:
        print(f"⚠ Error deleting system message: {e}")

@client.on(events.NewMessage(pattern="/clean"))
async def clean_old_system_messages(event):
    """Command handler: Deletes all past system messages when the bot admin sends /clean."""
    chat = await event.get_chat()
    await event.reply("🧹 Cleaning system messages...")
    
    # Delete all past system messages
    count = 0
    async for message in client.iter_messages(chat.id, limit=None):
        if message.action:  # Detect system messages like "user joined", "user left"
            try:
                print(f"Checking message: {message.id} - {message.text}")
                if message.text:  # If the message has text, attempt to delete it
                    await message.delete()
                    count += 1
                    print(f"✅ Deleted system message: {str(message)}")
            except Exception as e:
                print(f"⚠ Error deleting message {message.id}: {e}")

    await event.reply(f"✅ Deleted {count} system messages!")

print("🚀 Bot is running...")
client.run_until_disconnected()
