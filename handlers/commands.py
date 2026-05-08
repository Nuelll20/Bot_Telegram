"""
handlers/commands.py
Handler perintah /start, /help, /geopolitik, /financial, /bola, /semuaberita
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
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
    get_wib_time,
    escape_md,
)
from config.settings import (
    MAX_NEWS_GEOPOLITIK,
    MAX_NEWS_FINANCIAL,
    MAX_NEWS_BOLA,
    SCHEDULE_GEOPOLITIK,
    SCHEDULE_FINANCIAL,
    SCHEDULE_BOLA,
    SCHEDULE_RINGKASAN_MALAM,
)

logger = logging.getLogger(__name__)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start"""
    waktu = escape_md(get_wib_time())
    msg = f"""🤖 *SELAMAT DATANG DI BOT BERITA HARIAN\\!*
📅 _{waktu}_

Saya adalah bot yang mengirimkan update berita otomatis setiap hari tentang:

🌍 *Geopolitik Global* — Konflik, diplomasi, hubungan internasional
💹 *Financial Global* — Pasar saham, komoditas, ekonomi dunia
🇮🇩 *Keuangan Indonesia* — IHSG, BI Rate, ekonomi nasional
⚽ *Sepak Bola Eropa* — Premier League, La Liga, UCL & lebih

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 *PERINTAH TERSEDIA:*

/geopolitik — Berita geopolitik terkini
/financial — Update keuangan global \\+ Indonesia
/bola — Berita sepak bola Eropa
/semuaberita — Semua berita sekaligus
/jadwal — Lihat jadwal update otomatis
/help — Bantuan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ *JADWAL UPDATE OTOMATIS \\(WIB\\):*
🌍 Geopolitik: `{escape_md(SCHEDULE_GEOPOLITIK)}`
💹 Financial: `{escape_md(SCHEDULE_FINANCIAL)}`
⚽ Bola: `{escape_md(SCHEDULE_BOLA)}`
🌙 Ringkasan Malam: `{escape_md(SCHEDULE_RINGKASAN_MALAM)}`
"""
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /help"""
    msg = """📖 *PANDUAN PENGGUNAAN BOT*

*Perintah Manual:*
/geopolitik — Ambil berita geopolitik sekarang
/financial — Ambil berita keuangan sekarang
/bola — Ambil berita bola sekarang
/semuaberita — Kirim semua kategori sekarang
/jadwal — Lihat jadwal pengiriman otomatis

*Catatan:*
• Bot ini mengirim berita *otomatis setiap hari* sesuai jadwal
• Sumber berita dari BBC, Reuters, CNBC, Kompas, Detik, dll
• Berita dibatasi 24 jam terakhir agar selalu fresh

Jika ada pertanyaan, hubungi admin bot\\.
"""
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)


async def cmd_jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /jadwal"""
    msg = f"""⏰ *JADWAL UPDATE OTOMATIS*
_Semua waktu dalam WIB \\(UTC\\+7\\)_

━━━━━━━━━━━━━━━━━━━━
🌍 *Geopolitik Global*
   → Setiap hari jam `{escape_md(SCHEDULE_GEOPOLITIK)}`

💹 *Financial & Ekonomi*
   → Setiap hari jam `{escape_md(SCHEDULE_FINANCIAL)}`

⚽ *Sepak Bola Eropa*
   → Setiap hari jam `{escape_md(SCHEDULE_BOLA)}`

🌙 *Ringkasan Malam*
   → Setiap hari jam `{escape_md(SCHEDULE_RINGKASAN_MALAM)}`
━━━━━━━━━━━━━━━━━━━━

Gunakan perintah manual untuk mendapatkan berita *sekarang juga*\\.
"""
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)


async def cmd_geopolitik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /geopolitik — kirim berita geopolitik on-demand."""
    await update.message.reply_text(
        "⏳ _Sedang mengambil berita geopolitik\\.\\.\\._",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    try:
        news = await get_geopolitik_news(MAX_NEWS_GEOPOLITIK)
        msg  = format_geopolitik(news)
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2,
                                        disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Error cmd_geopolitik: {e}")
        await update.message.reply_text("❌ Gagal mengambil berita. Coba lagi nanti.")


async def cmd_financial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /financial — kirim berita keuangan on-demand."""
    await update.message.reply_text(
        "⏳ _Sedang mengambil data financial\\.\\.\\._",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    try:
        global_news = await get_financial_global_news(MAX_NEWS_FINANCIAL)
        indo_news   = await get_financial_indonesia_news(MAX_NEWS_FINANCIAL)
        msg = format_financial(global_news, indo_news)
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2,
                                        disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Error cmd_financial: {e}")
        await update.message.reply_text("❌ Gagal mengambil berita. Coba lagi nanti.")


async def cmd_bola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /bola — kirim berita bola on-demand."""
    await update.message.reply_text(
        "⏳ _Sedang mengambil berita sepak bola\\.\\.\\._",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    try:
        news = await get_bola_eropa_news(MAX_NEWS_BOLA)
        msg  = format_bola(news)
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2,
                                        disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Error cmd_bola: {e}")
        await update.message.reply_text("❌ Gagal mengambil berita. Coba lagi nanti.")


async def cmd_semuaberita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /semuaberita — kirim semua kategori sekaligus."""
    await update.message.reply_text(
        "⏳ _Mengambil semua berita, harap tunggu\\.\\.\\._",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    try:
        geo_news    = await get_geopolitik_news(MAX_NEWS_GEOPOLITIK)
        global_news = await get_financial_global_news(MAX_NEWS_FINANCIAL)
        indo_news   = await get_financial_indonesia_news(MAX_NEWS_FINANCIAL)
        bola_news   = await get_bola_eropa_news(MAX_NEWS_BOLA)

        # Kirim masing-masing sebagai pesan terpisah
        await update.message.reply_text(
            format_geopolitik(geo_news),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True
        )
        await update.message.reply_text(
            format_financial(global_news, indo_news),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True
        )
        await update.message.reply_text(
            format_bola(bola_news),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error cmd_semuaberita: {e}")
        await update.message.reply_text("❌ Gagal mengambil berita. Coba lagi nanti.")
