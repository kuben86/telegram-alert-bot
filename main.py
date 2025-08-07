from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Your Telegram bot settings (set these in Render environment variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_data(as_text=True)

    # Send message to Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": data
    }
    requests.post(telegram_url, data=payload)

    return "ok", 200









