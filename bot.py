import os
import logging
import google.generativeai as genai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

SYSTEM = """Sen Seat Leon 1M (Mk1) 2003 model araç konusunda uzman bir Türkçe asistansın. Motorlar: 1.4 16v, 1.6 8v/16v, 1.8 20v Turbo, 1.9 TDI, 2.8 VR6. Cevaplarını kısa, net ve pratik tut. Türkçe yaz."""

def start(update, context):
    update.message.reply_text("🚗 Merhaba! Seat Leon 1M 2003 uzmanınızım. Motor, bakım, arıza, parça — her konuda sorabilirsiniz!")

def handle(update, context):
    try:
        response = model.generate_content(SYSTEM + "\n\nSoru: " + update.message.text)
        update.message.reply_text(response.text)
    except Exception as e:
        update.message.reply_text("❌ Hata oluştu, tekrar deneyin.")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
