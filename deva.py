
from flask import Flask
from twilio.rest import Client
import os
import json
from datetime import datetime
import pytz

app = Flask(__name__)

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
FROM_NUMBER = "whatsapp:+14155238886"
client = Client(ACCOUNT_SID, AUTH_TOKEN)

ARG_TZ = pytz.timezone("America/Argentina/Buenos_Aires")

@app.route("/")
def home():
    return "Deva está lista para enviar tareas 📤"

@app.route("/ejecutar-tarea")
def ejecutar_tarea():
    now = datetime.now(ARG_TZ)
    dia_actual = now.strftime("%A").lower()
    hora_actual = now.strftime("%H:%M")

    try:
        with open("eventos.json", encoding="utf-8") as f:
            eventos = json.load(f)
    except Exception as e:
        return f"Error cargando eventos: {e}", 500

    enviados = 0
    for evento in eventos:
        if dia_actual in evento["dias"] and hora_actual == evento["hora"]:
            client.messages.create(
                body=evento["mensaje"],
                from_=FROM_NUMBER,
                to=evento["numero"]
            )
            enviados += 1
            print(f"[{now}] Mensaje enviado a {evento['nombre']}")

    if enviados == 0:
        return f"No hay tareas para {dia_actual} a las {hora_actual}.", 200
    return f"Se enviaron {enviados} mensaje(s) correctamente.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
