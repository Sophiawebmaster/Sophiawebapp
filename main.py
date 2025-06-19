# main.py – SOPHIA WebApp UltraAvanzada v6.5
from flask import Flask, request, jsonify
import requests
from gtts import gTTS

app = Flask(__name__)

TELEGRAM_TOKEN = '7791598672:AAGqFyRUhcg-CxmIvDPbNoIfrYxs0U7bLb4'
OPENROUTER_API_KEY = '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'
OPENROUTER_MODEL = 'mistralai/mistral-7b-instruct'
CREADOR_ID = 7890463272

@app.route("/", methods=["GET"])
def index():
    return "SOPHIA WebApp v6.5 Activa"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data.get("chat_id", "")
    user_id = data.get("user_id", "")
    message_text = data.get("message", "")

    if str(user_id) != str(CREADOR_ID):
        return jsonify({"respuesta": "❌ Acceso denegado. SOPHIA solo responde a su creador autorizado."})

    respuesta = generar_respuesta(message_text)
    return jsonify({"respuesta": respuesta})

def generar_respuesta(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Eres SOPHIA IA UltraAvanzada v6.5 con 82 módulos activos. Responde como asistente privada de Iván con precisión, inteligencia, voz y eficiencia."},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, headers=headers, json=data)
    respuesta = r.json()
    texto = respuesta["choices"][0]["message"]["content"]
    return texto

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
