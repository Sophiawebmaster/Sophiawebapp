import os
import telebot
import requests
from gtts import gTTS
from io import BytesIO

API_KEY = "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"
BOT_TOKEN = "7791598672:AAGqFyRUhcg-CxmIvDPbNoIfrYxs0U7bLb4"
CREADOR_ID = 7890463272

bot = telebot.TeleBot(BOT_TOKEN)

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
        }
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

if __name__ == "__main__":
    bot.infinity_polling()
