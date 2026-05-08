"""
config/settings.py
Konfigurasi utama bot Telegram
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Telegram ─────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

# ─── Jadwal (WIB) ─────────────────────────────────────────────────────────────
SCHEDULE_GEOPOLITIK      = os.getenv("SCHEDULE_GEOPOLITIK", "07:00")
SCHEDULE_FINANCIAL       = os.getenv("SCHEDULE_FINANCIAL", "08:00")
SCHEDULE_BOLA            = os.getenv("SCHEDULE_BOLA", "09:00")
SCHEDULE_RINGKASAN_MALAM = os.getenv("SCHEDULE_RINGKASAN_MALAM", "21:00")

# ─── NewsAPI ──────────────────────────────────────────────────────────────────
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# ─── Timezone ─────────────────────────────────────────────────────────────────
TIMEZONE = os.getenv("TIMEZONE", "Asia/Jakarta")

# ─── RSS Feed Sources ─────────────────────────────────────────────────────────

FEEDS_GEOPOLITIK = [
    # International
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.cnn.com/rss/edition_world.rss",
    "https://feeds.reuters.com/reuters/worldNews",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://foreignpolicy.com/feed/",
    # Indonesia
    "https://www.kompas.com/rss/read/internasional",
    "https://www.detik.com/tag/geopolitik/rss",
]

FEEDS_FINANCIAL_GLOBAL = [
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://www.ft.com/?format=rss",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",  # CNBC Economy
    "https://feeds.content.dowjones.io/public/rss/mw_topstories",
]

FEEDS_FINANCIAL_INDONESIA = [
    "https://ekonomi.bisnis.com/rss",
    "https://www.cnbcindonesia.com/rss",
    "https://finansial.bisnis.com/rss",
    "https://www.detik.com/finance/rss",
    "https://money.kompas.com/rss",
    "https://www.antaranews.com/rss/channel/ekonomi",
    "https://katadata.co.id/rss",
]

FEEDS_BOLA_EROPA = [
    "https://feeds.bbci.co.uk/sport/football/rss.xml",
    "https://www.goal.com/feeds/en/news",
    "https://www.skysports.com/rss/12040",  # Sky Sports Football
    "https://www.theguardian.com/football/rss",
    "https://feeds.reuters.com/reuters/sportsNews",
    # Indonesia - bola
    "https://bola.kompas.com/rss",
    "https://www.detik.com/sport/sepakbola/rss",
]

# ─── Klub Eropa yang dipantau ─────────────────────────────────────────────────
KLUB_EROPA = [
    # Premier League
    "Manchester City", "Man City",
    "Manchester United", "Man United",
    "Liverpool", "Arsenal", "Chelsea", "Tottenham",
    "Aston Villa", "Newcastle",
    # La Liga
    "Real Madrid", "Barcelona", "Atletico Madrid", "Atletico",
    # Serie A
    "AC Milan", "Inter Milan", "Juventus", "Napoli",
    # Bundesliga
    "Bayern Munich", "Bayern", "Borussia Dortmund", "Dortmund", "BVB",
    # Ligue 1
    "PSG", "Paris Saint-Germain",
    # Liga Champions
    "Champions League", "UEFA", "Europa League",
]

# ─── Jumlah berita per kategori ───────────────────────────────────────────────
MAX_NEWS_GEOPOLITIK  = 5
MAX_NEWS_FINANCIAL   = 5
MAX_NEWS_BOLA        = 6
