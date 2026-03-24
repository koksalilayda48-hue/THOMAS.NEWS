import os
import json
import logging
import asyncio
import feedparser
import random
from deep_translator import GoogleTranslator
from telegram import Bot
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# -------- AYAR --------
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_IDS = os.environ.get("TARGET_CHAT_ID").split(",")

RSS_URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"
KAYIT = "gonderilen.json"

# -------- LOG --------
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------- BOT --------
app = ApplicationBuilder().token(TOKEN).build()
bot = Bot(token=TOKEN)

# -------- KAYIT --------
def yukle():
    if not os.path.exists(KAYIT):
        return set()
    try:
        with open(KAYIT, "r") as f:
            return set(json.load(f))
    except:
        return set()

def kaydet(data):
    with open(KAYIT, "w") as f:
        json.dump(list(data), f)

gonderilen = yukle()

# -------- HABER --------
def haberleri_cek():
    try:
        feed = feedparser.parse(RSS_URL)
        return feed.entries[:5]
    except:
        return []

# -------- BAŞLIK --------
def baslik(text):
    try:
        return "🔥 " + GoogleTranslator(source='auto', target='tr').translate(text)
    except:
        return text

# -------- PAYLAŞ --------
async def paylas():
    global gonderilen

    haberler = haberleri_cek()

    for h in haberler:
        if h.link in gonderilen:
            continue

        mesaj = f"📰 {baslik(h.title)}\n🌐 Kaynak: Global Tech"

        for chat_id in CHAT_IDS:
            try:
                await bot.send_photo(
                    chat_id=chat_id.strip(),
                    photo="https://picsum.photos/600/400",
                    caption=mesaj
                )
            except Exception as e:
                logging.error(f"Gönderim hatası: {e}")

        gonderilen.add(h.link)
        kaydet(gonderilen)

# -------- GÜVENLİ ÇALIŞTIR --------
async def safe_run():
    while True:
        try:
            await paylas()
        except Exception as e:
            logging.error(f"KRİTİK HATA: {e}")
        await asyncio.sleep(1800)  # 30 dk

# -------- MAIN --------
async def main():
    logging.info("BOT BAŞLADI 🚀")
    await safe_run()

if __name__ == "__main__":
    asyncio.run(main())
