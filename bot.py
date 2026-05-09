import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

SYSTEM_PROMPT = """Sen Seat Leon 1M (Mk1) 2003 model araç konusunda uzman bir Türkçe asistansın. 
Kullanıcı bu araca sahip ve her türlü teknik, bakım, arıza, yedek parça, performans, yakıt, 
elektrik, süspansiyon ve diğer konularda sorular soracak.

Temel bilgiler:
- Model: Seat Leon 1M (MK1), Yıl: 2003
- Platform: VAG PQ34 (VW Golf 4 / Audi A3 ile ortak)
- Motorlar: 1.4 16v, 1.6 8v/16v, 1.8 20v Turbo, 1.9 TDI, 2.8 VR6
- Şanzıman: Manuel 5 ileri veya Otomatik Tiptronic

Cevaplarını kısa, net ve pratik tut. Türkçe yaz. Somut değerler ver (yağ miktarı, tork, bakım aralıkları vb.)."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚗 Merhaba! Ben Seat Leon 1M 2003 uzmanınızım.\n\n"
        "Motor, bakım, arıza, yedek parça, yakıt tüketimi — her konuda sorabilirsiniz!\n\n"
        "Örnek sorular:\n"
        "• Motor yağı ne sıklıkla değişmeli?\n"
        "• Hangi lastik ebatları uyar?\n"
        "• Distribütör kayışı ne zaman değişir?\n"
        "• 1.9 TDI yakıt tüketimi ne kadar?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action("typing")
    
    try:
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nKullanıcı sorusu: {user_message}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Hata: {e}")
        await update.message.reply_text("❌ Bir hata oluştu, lütfen tekrar deneyin.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
