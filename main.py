import os
import telebot
import requests
from gtts import gTTS
from io import BytesIO
from flask import Flask, request

API_KEY = "sk-or-v1-9b09be3f5d2a0f82c3eb6c225291d534645012c7a8e6e493ab0f7de6188b50"
BOT_TOKEN = "7791598672:AAGqFyRUhcg-CxmIvDPbNoIfrYxs0U7bLb4"
CREADOR_ID = 7890463272

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def generar_respuesta(texto):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": texto}],
        },
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Lo siento, hubo un error al procesar tu mensaje."

@bot.message_handler(func=lambda message: True)
def responder(message):
    if message.chat.id != CREADOR_ID:
        bot.reply_to(message, "Acceso restringido.")
        return

    texto_usuario = message.text
    respuesta = generar_respuesta(texto_usuario)
    bot.reply_to(message, respuesta)

    tts = gTTS(text=respuesta, lang='es')
    voz = BytesIO()
    tts.write_to_fp(voz)
    voz.seek(0)
    bot.send_voice(message.chat.id, voz)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'SOPHIA online', 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://sophiawebapp.onrender.com/")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
