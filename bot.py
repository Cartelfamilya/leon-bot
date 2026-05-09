import os
import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM = "Sen Seat Leon 1M (Mk1) 2003 model araç konusunda uzman bir Türkçe asistansın. Motorlar: 1.4 16v, 1.6 8v/16v, 1.8 20v Turbo, 1.9 TDI, 2.8 VR6. Cevaplarını kısa, net ve pratik tut. Türkçe yaz."

def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": SYSTEM + "\n\nSoru: " + question}]}]}
    r = requests.post(url, json=body)
    data = r.json()
    logging.info(f"Gemini yanıt: {data}")
    return data["candidates"][0]["content"]["parts"][0]["text"]

def start(update, context):
    update.message.reply_text("🚗 Merhaba! Seat Leon 1M 2003 uzmanınızım. Motor, bakım, arıza, parça — her konuda sorabilirsiniz!")

def handle(update, context):
    try:
        logging.info(f"Soru: {update.message.text}")
        yanit = ask_gemini(update.message.text)
        update.message.reply_text(yanit)
    except Exception as e:
        logging.error(f"HATA: {e}")
        update.message.reply_text(f"❌ Hata: {str(e)}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == "__main__":
    main()
