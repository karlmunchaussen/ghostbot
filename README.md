# GhostBot 🕵️‍♂️

**GhostBot** is a simple Telegram automation script built with [Telethon](https://github.com/LonamiWebs/Telethon).  
It logs group chat activity and periodically posts randomized messages to select groups.

This project is great for learning how to:
- Interact with Telegram via Python
- Simulate human-like behavior in chat environments
- Collect and analyze group messages

---

## 🚀 Features

- ✅ Monitors all joined group chats in real time
- ✅ Logs incoming messages to a CSV file
- ✅ Sends scheduled messages at random intervals (60–180 seconds)
- ✅ Only posts in groups you manually whitelist

---

## 🛠️ Requirements

- Python 3.10+
- A Telegram account (login required on first run)
- Telegram API credentials (see below)

Install dependencies:

```bash
pip install telethon
