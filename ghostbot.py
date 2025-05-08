from telethon import TelegramClient, events
import random
import asyncio
import csv
import os
import json
from datetime import datetime

# === 1. Your Telegram API credentials ===
api_id   = 123456789 # replace with your API ID
api_hash = '1234567890abcdef1234567890abcdef' # replace with your API Hash   
session_name = 'ghostbot'

# === 2. Groups to post into ===
target_groups = [
    'group'    # replace with your group names or @handles
]

# === 3. Paths ===
GIFS_DIR     = 'gifs'
LOG_CSV_PATH = 'logs/chat_log.csv'
TRIGGERS_PATH = 'triggers.json'

# === 4. Create the Telegram client ===
client = TelegramClient(session_name, api_id, api_hash)

# === 5. Load keyword triggers ===
def load_triggers(path=TRIGGERS_PATH):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

triggers = load_triggers()

# === 6. Load available GIFs ===
def load_gifs(path=GIFS_DIR):
    return [
        os.path.join(path, fn)
        for fn in os.listdir(path)
        if fn.lower().endswith('.mp4')
    ]

gifs = load_gifs()

# === 7. Logging incoming messages ===
async def log_message_to_csv(event):
    sender = await event.get_sender()
    name   = sender.username or sender.first_name or 'Unknown'
    text   = event.raw_text
    ts     = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.makedirs(os.path.dirname(LOG_CSV_PATH), exist_ok=True)
    with open(LOG_CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ts, name, text])

# === 8. Find and pick a trigger response ===
def get_trigger_response(text):
    text_l = text.lower()
    for keyword, replies in triggers.items():
        if keyword in text_l:
            return random.choice(replies)
    return None

# === 9. Handler: log + reply if trigger found ===
@client.on(events.NewMessage(chats=None))
async def on_new_message(event):
    # 1️⃣ Fetch the chat object for this message
    chat = await event.get_chat()
    # 2️⃣ Derive the “name” (group title) or @handle
    chat_name = getattr(chat, 'title', None) or getattr(chat, 'username', None)
    # 3️⃣ Bail out if this chat isn’t in your allowed list
    if chat_name not in target_groups:
        return

    # — Now we know it’s a target group, so proceed —

    # 4️⃣ Log the message
    await log_message_to_csv(event)

    # 5️⃣ Don’t reply to yourself
    sender = await event.get_sender()
    me = await client.get_me()
    if sender.id == me.id:
        return

    # 6️⃣ Check for keyword triggers
    response = get_trigger_response(event.raw_text)
    if response:
        await asyncio.sleep(random.randint(5, 15))
        try:
            await event.reply(response)
            print(f"Replied in {chat_name}: {response}")
        except Exception as e:
            print("Reply failed:", e)

# === 10. Scheduled GIF posting ===
async def send_hourly_gifs():
    while True:
        await asyncio.sleep(3600)  # 1 hour
        if not gifs:
            print("⚠️ No GIFs found in 'gifs/'")
            continue

        gif = random.choice(gifs)
        try:
            dialogs = await client.get_dialogs()
            for d in dialogs:
                if d.is_group:
                    uname = getattr(d.entity, 'username', None)
                    if d.name in target_groups or (uname and uname in target_groups):
                        await client.send_file(d.id, gif)
                        print(f"Sent GIF {os.path.basename(gif)} to {d.name or uname}")
        except Exception as e:
            print("Failed to send GIF:", e)

# === 11. Run the bot ===
async def main():
    await client.start()
    print("GhostBot v0.2 running…")
    await asyncio.gather(
        send_hourly_gifs()
    )

client.loop.run_until_complete(main())