from flask import Flask, request, jsonify
import requests
from gtts import gTTS
import os

app = Flask(__name__)

TELEGRAM_TOKEN = '7791598672:AAGqFyRUhcg-CxmIvDPbNoIfrYxs0U7bLb4'
OPENROUTER_API_KEY = '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'
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"
CREADOR_ID = 7890463272

@app.route("/", methods=["GET"])
def index():
    return "SOPHIA WebApp v6.5 Activa"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")
    user_id = data.get("message", {}).get("from", {}).get("id", "")
    message_text = data.get("message", {}).get("text", "")

    if str(user_id) != str(CREADOR_ID):
        return jsonify({"respuesta": "❌ Acceso denegado. SOPHIA solo responde a su creador autorizado."})

    respuesta = generar_respuesta(message_text)
    enviar_mensaje(chat_id, respuesta)
    generar_audio(chat_id, respuesta)
    
    return jsonify({"respuesta": "✅ Mensaje enviado a Telegram con voz"})

def generar_respuesta(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Eres SOPHIA IA UltraAvanzada v6.5 con 82 módulos activos. Responde como asistente experta, leal y brillante."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        respuesta = r.json()
        return respuesta["choices"][0]["message"]["content"]
    except Exception as e:
        return "⚠️ No pude generar una respuesta. Revisa tu API Key, modelo o conexión."

def enviar_mensaje(chat_id, texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    requests.post(url, json=payload)

def generar_audio(chat_id, texto):
    tts = gTTS(text=texto, lang='es')
    filename = f"{chat_id}.mp3"
    tts.save(filename)

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
    with open(filename, 'rb') as voice:
        requests.post(url, data={"chat_id": chat_id}, files={"voice": voice})
    
    os.remove(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
