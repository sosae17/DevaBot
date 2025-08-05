
from flask import Flask, request
from twilio.rest import Client
import os
import json

app = Flask(__name__)

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
NUMERO_ADMIN = os.environ.get("NUMERO_ADMIN")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

try:
    with open("contactos.json", encoding="utf-8") as f:
        contactos = json.load(f)
except FileNotFoundError:
    contactos = {}

@app.route("/")
def index():
    return "Deva está escuchando 🧏‍♀️"

@app.route("/webhook", methods=["POST"])
def webhook():
    from_number = request.form.get("From")
    mensaje = request.form.get("Body")

    nombre = contactos.get(from_number, from_number)

    texto = f"📩 {nombre} respondió:\n{mensaje}"
    client.messages.create(
        body=texto,
        from_="whatsapp:+14155238886",
        to=NUMERO_ADMIN
    )
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
