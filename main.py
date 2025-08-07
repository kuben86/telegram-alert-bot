from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram bot token and chat ID (hardcoded for now)
TELEGRAM_TOKEN = "8168936180:AAEQ8D70YgGXeVS-WhDY8cPi8szazPobqcU"
TELEGRAM_CHAT_ID = "-1002881738496"

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







