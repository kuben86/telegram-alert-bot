from flask import Flask, request
import telegram
import logging

# === Telegram Configuration ===
TELEGRAM_TOKEN = "8168936180:AAEQ8D70YgGXeVS-WhDY8cPi8szazPobqcU"
TELEGRAM_CHAT_ID = "-1002881738496"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# === Flask App ===
app = Flask(__name__)

# === Trade State Management ===
trade_state = {
    "in_trade": False,
    "direction": None,
    "entry": None,
    "sl": None
}

# === Logging Setup ===
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_data(as_text=True).strip()
    logging.info(f"Alert received: {data}")

    if "ENTRY_LONG" in data:
        values = parse_entry(data, long=True)
        if values:
            trade_state.update({"in_trade": True, "direction": "long", **values})
            send_message(f"📈 LONG ENTRY\nEntry: {values['entry']:.2f}\nSL: {values['sl']:.2f}")
    elif "ENTRY_SHORT" in data:
        values = parse_entry(data, long=False)
        if values:
            trade_state.update({"in_trade": True, "direction": "short", **values})
            send_message(f"📉 SHORT ENTRY\nEntry: {values['entry']:.2f}\nSL: {values['sl']:.2f}")
    elif "TP" in data:
        if trade_state["in_trade"]:
            if (trade_state["direction"] == "long" and "TP" in data and "LONG" in data) or \
               (trade_state["direction"] == "short" and "TP" in data and "SHORT" in data):
                tp_label = data.split(" | ")[0]
                send_message(f"✅ {tp_label} HIT\nExit at market.\nEntry was {trade_state['entry']:.2f}")
                trade_state.update({"in_trade": False, "direction": None})
    return "", 200

def parse_entry(text, long=True):
    try:
        fields = dict(field.strip().split("=") for field in text.split("|")[1:])
        entry = max(float(fields["high1"]), float(fields["high2"])) if long else min(float(fields["low1"]), float(fields["low2"]))
        entry += 0.01 if long else -0.01
        sl = float(fields["sl"])
        return {"entry": entry, "sl": sl}
    except Exception as e:
        logging.error(f"Error parsing alert: {e}")
        return None

def send_message(msg):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    except Exception as e:
        logging.error(f"Telegram error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)















