from telethon import TelegramClient, events
import random
import asyncio
import csv
import os
from datetime import datetime

# === 1. Your Telegram API credentials ===
api_id = 23218700      # Replace with your API ID
api_hash = '36691678b2c0b06f3fce447c2d2a5a88'  # Replace with your API hash
session_name = 'ghostbot'

# === 2. List of Telegram group names or usernames to post in ===
target_groups = [
    'МультиВселенная и в ней навигация 3'        # Replace with your group name or username
                                                 # Or t.me/groupname (just the handle)
]

# === 3. Setup Telegram client ===
client = TelegramClient(session_name, api_id, api_hash)

# === 4. Load message templates ===
def load_messages(file_path='messages.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# === 5. Save incoming messages to CSV log ===
async def log_message_to_csv(event):
    sender = await event.get_sender()
    sender_name = sender.username or sender.first_name or "Unknown"
    text = event.raw_text
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('logs/chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, sender_name, text])

# === 6. Listen for new messages in all joined groups ===
@client.on(events.NewMessage(chats=None))
async def handler(event):
    await log_message_to_csv(event)

# === 7. Periodically send messages to your chosen groups ===
async def send_periodic_messages():
    messages = load_messages()
    while True:
        await asyncio.sleep(random.randint(60, 180))  # Wait 1–3 minutes
        if messages:
            message = random.choice(messages)
            try:
                dialogs = await client.get_dialogs()
                for dialog in dialogs:
                    username = getattr(dialog.entity, 'username', None)
                    if dialog.is_group and (dialog.name in target_groups or (username and username in target_groups)):
                        await client.send_message(dialog.id, message)
                        chat_name = dialog.name or getattr(dialog.entity, 'username', 'Unknown Group')
                        print(f"Sent to {chat_name}: {message}")
            except Exception as e:
                print("Failed to send message:", e)

# === 8. Main run loop ===
async def main():
    os.makedirs('logs', exist_ok=True)
    await client.start()
    print("GhostBot is running.")
    await asyncio.gather(
        send_periodic_messages()
    )

client.loop.run_until_complete(main())