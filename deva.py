import os
import json
from datetime import datetime, time
from dateutil import tz
from twilio.rest import Client

# Inicializar Twilio con variables de entorno
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Zonas horarias
zona_local = tz.gettz("America/Argentina/Buenos_Aires")
zona_utc = tz.UTC

# Cargar eventos desde JSON
with open("eventos.json", "r", encoding="utf-8") as f:
    eventos = json.load(f)

# Obtener fecha y hora actual UTC
ahora_utc = datetime.now(tz=zona_utc)

enviado = False

for evento in eventos:
    # Obtener día y hora del evento
    dias = evento["dias"]
    hora_str = evento["hora"]  # Ej: "21:11"

    # Convertir hora del evento (hora local) a objeto datetime con fecha hoy
    hora_local = datetime.strptime(hora_str, "%H:%M").time()

    # Construir datetime local combinando fecha actual local + hora evento
    ahora_local = ahora_utc.astimezone(zona_local)
    fecha_local = ahora_local.date()
    evento_dt_local = datetime.combine(fecha_local, hora_local, tzinfo=zona_local)

    # Convertir datetime evento local a UTC para comparar
    evento_dt_utc = evento_dt_local.astimezone(zona_utc)

    # Comparar día de la semana y hora actual UTC con el evento
    dia_actual_utc = ahora_utc.strftime("%A").lower()
    hora_actual_utc = ahora_utc.strftime("%H:%M")

    # Importante: verificar si el día local del evento coincide con el día actual local
    dia_evento_local = evento_dt_local.strftime("%A").lower()

    if dia_evento_local in dias and hora_actual_utc == evento_dt_utc.strftime("%H:%M"):
        numero = evento["numero"]
        if not numero.startswith("whatsapp:"):
            numero = "whatsapp:+54" + numero.lstrip("+54").lstrip("0")

        mensaje = evento["mensaje"]
        nombre = evento.get("nombre", "Usuario")

        try:
            client.messages.create(
                body=mensaje,
                from_="whatsapp:+14155238886",
                to=numero
            )
            print(f"✅ Mensaje enviado a {nombre} ({numero}) a las {hora_actual_utc} UTC")
            enviado = True
        except Exception as e:
            print(f"❌ Error enviando a {nombre} ({numero}): {e}")

if not enviado:
    print("ℹ️ No hay mensajes programados para esta fecha y hora.")
