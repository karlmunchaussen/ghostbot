from telethon import TelegramClient, events
import random
import asyncio
import csv
import os
from datetime import datetime

# === 1. Your Telegram API credentials ===
api_id = 123456      # Replace with your API ID
api_hash = 'abcdef1234567890abcdef1234567890'  # Replace with your API hash
session_name = 'ghostbot'

# === 2. List of group names or usernames to post in ===
target_groups = [
    'ExampleGroup1',
    'ExampleGroup2',
]

# === 3. Setup Telegram client ===
client = TelegramClient(session_name, api_id, api_hash)

# === 4. Load scheduled messages ===
def load_messages(file_path='messages.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# === 5. Log incoming group messages ===
async def log_message_to_csv(event):
    sender = await event.get_sender()
    sender_name = sender.username or sender.first_name or "Unknown"
    text = event.raw_text
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('logs/chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, sender_name, text])

# === 6. Message listener ===
@client.on(events.NewMessage(chats=None))
async def handler(event):
    await log_message_to_csv(event)

# === 7. Periodic message sender ===
async def send_periodic_messages():
    messages = load_messages()
    while True:
        await asyncio.sleep(random.randint(60, 180))  # Wait 1–3 minutes
        if messages:
            message = random.choice(messages)
            try:
                dialogs = await client.get_dialogs()
                for dialog in dialogs:
                    if dialog.is_group:
                        username = getattr(dialog.entity, 'username', None)
                        if dialog.name in target_groups or (username and username in target_groups):
                            chat_name = dialog.name or username or 'Unknown Group'
                            await client.send_message(dialog.id, message)
                            print(f"Sent to {chat_name}: {message}")
            except Exception as e:
                print("Failed to send message:", e)

# === 8. Start the bot ===
async def main():
    os.makedirs('logs', exist_ok=True)
    await client.start()
    print("GhostBot is running.")
    await asyncio.gather(
        send_periodic_messages()
    )

client.loop.run_until_complete(main())