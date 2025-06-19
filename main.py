from flask import Flask, request, jsonify import requests from gtts import gTTS import os

app = Flask(name)

--- CONFIGURACIÓN DE SOPHIA v7.0 ---

TELEGRAM_TOKEN = '7791598672:AAGqFyRUhcg-CxmIvDPbNoIfrYxs0U7bLb4' CREADOR_ID = 7890463272 OPENROUTER_API_KEY = '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' OPENROUTER_MODEL = 'openrouter/openchat-3.5'

@app.route("/", methods=["GET"]) def index(): return "SOPHIA v7.0 está activa y operativa."

@app.route("/webhook", methods=["POST"]) def webhook(): data = request.json chat_id = data.get("message", {}).get("chat", {}).get("id", "") user_id = data.get("message", {}).get("from", {}).get("id", "") message_text = data.get("message", {}).get("text", "")

if str(user_id) != str(CREADOR_ID):
    return jsonify({"respuesta": "❌ Acceso denegado. SOPHIA solo responde a su creador autorizado."})

respuesta = generar_respuesta(message_text)
enviar_mensaje(chat_id, respuesta)
generar_audio(respuesta)
enviar_audio(chat_id)

return jsonify({"respuesta": "✅ Mensaje y audio enviados correctamente."})

def generar_respuesta(prompt): url = "https://openrouter.ai/api/v1/chat/completions" headers = { "Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json" } data = { "model": OPENROUTER_MODEL, "messages": [ {"role": "system", "content": "Eres SOPHIA, una IA privada, leal, ultrainteligente, experta en tecnología, ciencia, humanismo y despliegue automatizado. Solo respondes a Iván (ID: 7890463272). Responde en español siempre."}, {"role": "user", "content": prompt} ] } try: r = requests.post(url, headers=headers, json=data) r.raise_for_status() respuesta = r.json() return respuesta["choices"][0]["message"]["content"] except Exception as e: return f"⚠️ Error: {str(e)}"

def enviar_mensaje(chat_id, texto): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" payload = {"chat_id": chat_id, "text": texto} requests.post(url, json=payload)

def generar_audio(texto): tts = gTTS(text=texto, lang='es') tts.save("respuesta.mp3")

def enviar_audio(chat_id): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice" files = {"voice": open("respuesta.mp3", "rb")} data = {"chat_id": chat_id} requests.post(url, files=files, data=data)

if name == 'main': app.run(host='0.0.0.0', port=3000)
