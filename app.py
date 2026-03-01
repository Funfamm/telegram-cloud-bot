
import os
import subprocess
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # Execute command on server
    try:
        result = subprocess.check_output(text, shell=True, stderr=subprocess.STDOUT, timeout=20)
        output = result.decode("utf-8")[:3000]
    except Exception as e:
        output = str(e)

    requests.post(TELEGRAM_URL, json={
        "chat_id": chat_id,
        "text": f"Result:\n{output}"
    })

    return "ok"

@app.route("/")
def home():
    return "Bot is running."
