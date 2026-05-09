import os
import logging
import requests
import base64
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM = "Sen Seat Leon 1M (Mk1) 2003 model araç konusunda uzman bir Türkçe asistansın. Motorlar: 1.4 16v, 1.6 8v/16v, 1.8 20v Turbo, 1.9 TDI, 2.8 VR6. Kullanıcı sana araç parçaları, arıza, motor veya herhangi bir şeyin fotoğrafını gönderebilir. Fotoğrafı analiz et ve araçla ilgili yorum yap. Cevaplarını kısa, net ve pratik tut. Türkçe yaz."

def ask_gemini_text(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": SYSTEM + "\n\nSoru: " + question}]}]}
    r = requests.post(url, json=body)
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def ask_gemini_photo(image_bytes, caption=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = SYSTEM + "\n\nKullanıcı bir fotoğraf gönderdi."
    if caption:
        prompt += f" Kullanıcının notu: {caption}"
    prompt += "\n\nFotoğrafı analiz et ve Seat Leon 1M 2003 ile ilgili yorum yap."
    body = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}}
            ]
        }]
    }
    r = requests.post(url, json=body)
    data = r.json()
    logging.info(f"Foto yanıt: {data}")
    return data["candidates"][0]["content"]["parts"][0]["text"]

def start(update, context):
    update.message.reply_text("🚗 Merhaba! Seat Leon 1M 2003 uzmanınızım.\n\nYazılı soru sorabilir veya araba parçası, arıza, motor fotoğrafı gönderebilirsiniz — analiz ederim!")

def handle_text(update, context):
    try:
        update.message.chat.send_action(ChatAction.TYPING)
        logging.info(f"Soru: {update.message.text}")
        yanit = ask_gemini_text(update.message.text)
        update.message.reply_text(yanit)
    except Exception as e:
        logging.error(f"HATA: {e}")
        update.message.reply_text(f"❌ Hata: {str(e)}")

def handle_photo(update, context):
    try:
        update.message.chat.send_action(ChatAction.TYPING)
        photo = update.message.photo[-1]
        file = context.bot.get_file(photo.file_id)
        image_bytes = file.download_as_bytearray()
        caption = update.message.caption or ""
        logging.info(f"Fotoğraf geldi, caption: {caption}")
        yanit = ask_gemini_photo(bytes(image_bytes), caption)
        update.message.reply_text(yanit)
    except Exception as e:
        logging.error(f"FOTO HATA: {e}")
        update.message.reply_text(f"❌ Hata: {str(e)}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == "__main__":
    main()
