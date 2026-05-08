"""
main.py
Entry point Bot Telegram Berita Harian
Jalankan: python main.py
"""
import logging
import asyncio
from datetime import time as dtime

import pytz
from telegram.ext import (
    Application,
    CommandHandler,
)

from config.settings import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    SCHEDULE_GEOPOLITIK,
    SCHEDULE_FINANCIAL,
    SCHEDULE_BOLA,
    SCHEDULE_RINGKASAN_MALAM,
    TIMEZONE,
)
from handlers.commands import (
    cmd_start,
    cmd_help,
    cmd_jadwal,
    cmd_geopolitik,
    cmd_financial,
    cmd_bola,
    cmd_semuaberita,
)
from scheduler.jobs import (
    job_geopolitik,
    job_financial,
    job_bola,
    job_ringkasan_malam,
)

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ]
)
logger = logging.getLogger(__name__)


def parse_schedule_time(time_str: str):
    """Parse string HH:MM menjadi objek time."""
    h, m = map(int, time_str.strip().split(":"))
    return dtime(hour=h, minute=m, second=0, tzinfo=pytz.timezone(TIMEZONE))


def setup_scheduler(app: Application):
    """Daftarkan semua job ke APScheduler bawaan python-telegram-bot."""
    job_queue = app.job_queue
    tz = pytz.timezone(TIMEZONE)

    # Jadwal geopolitik
    t_geo = parse_schedule_time(SCHEDULE_GEOPOLITIK)
    job_queue.run_daily(
        lambda ctx: asyncio.create_task(job_geopolitik(ctx.bot)),
        time=t_geo,
        name="job_geopolitik",
    )
    logger.info(f"📅 Job geopolitik dijadwalkan: {SCHEDULE_GEOPOLITIK} WIB")

    # Jadwal financial
    t_fin = parse_schedule_time(SCHEDULE_FINANCIAL)
    job_queue.run_daily(
        lambda ctx: asyncio.create_task(job_financial(ctx.bot)),
        time=t_fin,
        name="job_financial",
    )
    logger.info(f"📅 Job financial dijadwalkan: {SCHEDULE_FINANCIAL} WIB")

    # Jadwal bola
    t_bola = parse_schedule_time(SCHEDULE_BOLA)
    job_queue.run_daily(
        lambda ctx: asyncio.create_task(job_bola(ctx.bot)),
        time=t_bola,
        name="job_bola",
    )
    logger.info(f"📅 Job bola dijadwalkan: {SCHEDULE_BOLA} WIB")

    # Jadwal ringkasan malam
    t_malam = parse_schedule_time(SCHEDULE_RINGKASAN_MALAM)
    job_queue.run_daily(
        lambda ctx: asyncio.create_task(job_ringkasan_malam(ctx.bot)),
        time=t_malam,
        name="job_ringkasan_malam",
    )
    logger.info(f"📅 Job ringkasan malam dijadwalkan: {SCHEDULE_RINGKASAN_MALAM} WIB")


def validate_config():
    """Validasi konfigurasi wajib."""
    errors = []
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        errors.append("❌ TELEGRAM_BOT_TOKEN belum diisi di file .env")
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "your_channel_or_group_id_here":
        errors.append("❌ TELEGRAM_CHAT_ID belum diisi di file .env")
    if errors:
        for e in errors:
            print(e)
        print("\n💡 Salin .env.example ke .env dan isi konfigurasi yang diperlukan.")
        raise SystemExit(1)


def main():
    """Fungsi utama — inisialisasi dan jalankan bot."""
    validate_config()

    logger.info("🚀 Memulai Bot Telegram Berita Harian...")
    logger.info(f"   Chat ID Target: {TELEGRAM_CHAT_ID}")
    logger.info(f"   Timezone: {TIMEZONE}")

    # Buat aplikasi bot
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Daftarkan command handler
    app.add_handler(CommandHandler("start",       cmd_start))
    app.add_handler(CommandHandler("help",        cmd_help))
    app.add_handler(CommandHandler("jadwal",      cmd_jadwal))
    app.add_handler(CommandHandler("geopolitik",  cmd_geopolitik))
    app.add_handler(CommandHandler("financial",   cmd_financial))
    app.add_handler(CommandHandler("bola",        cmd_bola))
    app.add_handler(CommandHandler("semuaberita", cmd_semuaberita))

    # Setup jadwal otomatis
    setup_scheduler(app)

    logger.info("✅ Bot siap! Menunggu pesan dan menjalankan jadwal...")
    logger.info("   Tekan Ctrl+C untuk menghentikan.")

    # Jalankan polling
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
