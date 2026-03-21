import os
import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# ----------------- Ayarlar -----------------
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # .env veya Render Environment Variable
TARGET_CHAT_ID = "6179118477"  # Hedef kanal kullanıcı adı veya chat id

# Haber listesi (istediğin kadar ekleyebilirsin)
haberler = [
    {
        "baslik": "Yeni yapay zeka teknolojisi tanıtıldı!",
        "kaynak": "Kendi Kanalın",
        "gorsel": "https://i.imgur.com/xyz123.jpg"
    },
    {
        "baslik": "Blockchain tabanlı oyunlar popülerleşiyor",
        "kaynak": "Kendi Kanalın",
        "gorsel": "https://i.imgur.com/abc456.jpg"
    }
]

# ----------------- Logging -----------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----------------- Bot Uygulaması -----------------
app = ApplicationBuilder().token(TOKEN).build()
bot = Bot(TOKEN)

# ----------------- Komutlar -----------------
async def start(update, context):
    await update.message.reply_text(
        "Merhaba! Bot aktif. 30 dakikada bir otomatik olarak haber paylaşacak."
    )

async def haber(update, context):
    for h in haberler:
        mesaj = f"📰 Başlık: {h['baslik']}\n🌐 Kaynak: {h['kaynak']}"
        await bot.send_photo(chat_id=TARGET_CHAT_ID, photo=h['gorsel'], caption=mesaj)

# Komutları ekle
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("haber", haber))

# ----------------- Otomatik Paylaşım -----------------
scheduler = BackgroundScheduler()

def paylas_haber():
    for h in haberler:
        mesaj = f"📰 Başlık: {h['baslik']}\n🌐 Kaynak: {h['kaynak']}"
        asyncio.run(bot.send_photo(chat_id=TARGET_CHAT_ID, photo=h['gorsel'], caption=mesaj))

# 30 dakikada bir paylaş
scheduler.add_job(paylas_haber, 'interval', minutes=30)
scheduler.start()

# ----------------- Botu Başlat -----------------
if __name__ == "__main__":
    logging.info("Bot başlatıldı, sürekli aktif...")
    app.run_polling()
