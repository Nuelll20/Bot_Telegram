"""
scheduler/jobs.py
Job terjadwal — broadcast otomatis ke channel/group
"""
import logging
from telegram import Bot
from telegram.constants import ParseMode

from services.rss_fetcher import (
    get_geopolitik_news,
    get_financial_global_news,
    get_financial_indonesia_news,
    get_bola_eropa_news,
)
from utils.formatter import (
    format_geopolitik,
    format_financial,
    format_bola,
    format_ringkasan_malam,
)
from config.settings import (
    TELEGRAM_CHAT_ID,
    MAX_NEWS_GEOPOLITIK,
    MAX_NEWS_FINANCIAL,
    MAX_NEWS_BOLA,
)

logger = logging.getLogger(__name__)


async def _send_message(bot: Bot, text: str):
    """Helper: kirim pesan ke channel/group target."""
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )
        logger.info("✅ Pesan berhasil dikirim ke channel.")
    except Exception as e:
        logger.error(f"❌ Gagal kirim pesan: {e}")


async def job_geopolitik(bot: Bot):
    """Job: kirim berita geopolitik."""
    logger.info("🌍 Menjalankan job geopolitik...")
    news = await get_geopolitik_news(MAX_NEWS_GEOPOLITIK)
    msg  = format_geopolitik(news)
    await _send_message(bot, msg)


async def job_financial(bot: Bot):
    """Job: kirim berita financial global + Indonesia."""
    logger.info("💹 Menjalankan job financial...")
    global_news = await get_financial_global_news(MAX_NEWS_FINANCIAL)
    indo_news   = await get_financial_indonesia_news(MAX_NEWS_FINANCIAL)
    msg = format_financial(global_news, indo_news)
    await _send_message(bot, msg)


async def job_bola(bot: Bot):
    """Job: kirim berita sepak bola Eropa."""
    logger.info("⚽ Menjalankan job bola...")
    news = await get_bola_eropa_news(MAX_NEWS_BOLA)
    msg  = format_bola(news)
    await _send_message(bot, msg)


async def job_ringkasan_malam(bot: Bot):
    """Job: kirim ringkasan malam — top highlight dari semua kategori."""
    logger.info("🌙 Menjalankan job ringkasan malam...")
    geo_news  = await get_geopolitik_news(3)
    fin_news  = await get_financial_global_news(3)
    bola_news = await get_bola_eropa_news(3)
    msg = format_ringkasan_malam(geo_news, fin_news, bola_news)
    await _send_message(bot, msg)
