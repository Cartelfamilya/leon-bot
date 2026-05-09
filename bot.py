import os
import logging
import google.generativeai as genai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

logging.info(f"TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else 'YOK'}")
logging.info(f"GEMINI_API_KEY: {GEMINI_API_KEY[:10] if GEMINI_API_KEY else 'YOK'}")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM = "Sen Seat Leon 1M (Mk1) 2003 model araç konusunda uzman bir Türkçe asistansın. Motorlar: 1.4 16v, 1.6 8v/16v, 1.8 20v Turbo, 1.9 TDI, 2.8 VR6. Cevaplarını kısa, net ve pratik tut. Türkçe yaz."

def start(update, context):
    update.message.reply_text("🚗 Merhaba! Seat Leon 1M 2003 uzmanınızım. Motor, bakım, arıza, parça — her konuda sorabilirsiniz!")

def handle(update, context):
    try:
        logging.info(f"Soru geldi: {update.message.text}")
        response = model.generate_content(SYSTEM + "\n\nSoru: " + update.message.text)
        logging.info(f"Yanıt: {response.text[:100]}")
        update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"HATA: {e}")
        update.message.reply_text(f"❌ Hata: {str(e)}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
