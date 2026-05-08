"""
utils/formatter.py
Format pesan Telegram dengan MarkdownV2
"""
from datetime import datetime
import pytz
from typing import List, Dict
from config.settings import TIMEZONE


def get_wib_time() -> str:
    """Waktu sekarang dalam WIB."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    return f"{hari[now.weekday()]}, {now.day} {bulan[now.month-1]} {now.year} | {now.strftime('%H:%M')} WIB"


def escape_md(text: str) -> str:
    """Escape karakter khusus untuk MarkdownV2 Telegram."""
    special = r"\_*[]()~`>#+-=|{}.!"
    for ch in special:
        text = text.replace(ch, f"\\{ch}")
    return text


def format_geopolitik(news_list: List[Dict]) -> str:
    """Format pesan berita geopolitik."""
    waktu = get_wib_time()
    lines = [
        f"🌍 *UPDATE GEOPOLITIK GLOBAL*",
        f"📅 _{escape_md(waktu)}_",
        f"{'─' * 30}",
        "",
    ]
    if not news_list:
        lines.append("_Tidak ada berita terbaru saat ini\\._")
    else:
        for i, item in enumerate(news_list, 1):
            title = escape_md(item["title"])
            source = escape_md(item.get("source", ""))
            summary = escape_md(item.get("summary", ""))
            link = item.get("link", "")

            lines.append(f"*{i}\\. {title}*")
            if source:
                lines.append(f"   📰 _{source}_")
            if summary:
                lines.append(f"   {summary}")
            if link:
                lines.append(f"   🔗 [Baca selengkapnya]({link})")
            lines.append("")

    lines += [
        f"{'─' * 30}",
        "🤖 _Bot Berita Harian_",
        "🕐 _Update otomatis setiap hari_",
    ]
    return "\n".join(lines)


def format_financial(global_news: List[Dict], indo_news: List[Dict]) -> str:
    """Format pesan berita keuangan global + Indonesia."""
    waktu = get_wib_time()
    lines = [
        f"💹 *UPDATE FINANCIAL & EKONOMI*",
        f"📅 _{escape_md(waktu)}_",
        f"{'─' * 30}",
        "",
        "🌐 *PASAR GLOBAL*",
        "",
    ]

    if not global_news:
        lines.append("_Tidak ada berita terbaru\\._\n")
    else:
        for i, item in enumerate(global_news, 1):
            title = escape_md(item["title"])
            source = escape_md(item.get("source", ""))
            summary = escape_md(item.get("summary", ""))
            link = item.get("link", "")
            lines.append(f"*{i}\\. {title}*")
            if source:
                lines.append(f"   📰 _{source}_")
            if summary:
                lines.append(f"   {summary}")
            if link:
                lines.append(f"   🔗 [Baca selengkapnya]({link})")
            lines.append("")

    lines += [
        f"{'─' * 30}",
        "",
        "🇮🇩 *EKONOMI & KEUANGAN INDONESIA*",
        "",
    ]

    if not indo_news:
        lines.append("_Tidak ada berita terbaru\\._\n")
    else:
        for i, item in enumerate(indo_news, 1):
            title = escape_md(item["title"])
            source = escape_md(item.get("source", ""))
            summary = escape_md(item.get("summary", ""))
            link = item.get("link", "")
            lines.append(f"*{i}\\. {title}*")
            if source:
                lines.append(f"   📰 _{source}_")
            if summary:
                lines.append(f"   {summary}")
            if link:
                lines.append(f"   🔗 [Baca selengkapnya]({link})")
            lines.append("")

    lines += [
        f"{'─' * 30}",
        "🤖 _Bot Berita Harian_",
        "🕐 _Update otomatis setiap hari_",
    ]
    return "\n".join(lines)


def format_bola(news_list: List[Dict]) -> str:
    """Format pesan berita sepak bola Eropa."""
    waktu = get_wib_time()
    lines = [
        f"⚽ *UPDATE SEPAK BOLA EROPA*",
        f"📅 _{escape_md(waktu)}_",
        f"{'─' * 30}",
        "",
        "🏆 _Premier League \\| La Liga \\| Serie A \\| Bundesliga \\| Ligue 1 \\| UCL_",
        "",
    ]

    if not news_list:
        lines.append("_Tidak ada berita terbaru saat ini\\._")
    else:
        for i, item in enumerate(news_list, 1):
            title = escape_md(item["title"])
            source = escape_md(item.get("source", ""))
            summary = escape_md(item.get("summary", ""))
            link = item.get("link", "")
            lines.append(f"*{i}\\. {title}*")
            if source:
                lines.append(f"   📰 _{source}_")
            if summary:
                lines.append(f"   {summary}")
            if link:
                lines.append(f"   🔗 [Baca selengkapnya]({link})")
            lines.append("")

    lines += [
        f"{'─' * 30}",
        "🤖 _Bot Berita Harian_",
        "🕐 _Update otomatis setiap hari_",
    ]
    return "\n".join(lines)


def format_ringkasan_malam(
    geo_news: List[Dict],
    fin_news: List[Dict],
    bola_news: List[Dict]
) -> str:
    """Format ringkasan malam: top 2 dari setiap kategori."""
    waktu = get_wib_time()
    lines = [
        f"🌙 *RINGKASAN BERITA MALAM INI*",
        f"📅 _{escape_md(waktu)}_",
        f"{'─' * 30}",
        "",
        "🌍 *GEOPOLITIK*",
    ]
    for item in geo_news[:2]:
        title = escape_md(item["title"])
        link = item.get("link", "")
        if link:
            lines.append(f"• [{title}]({link})")
        else:
            lines.append(f"• {title}")
    lines += ["", "💹 *FINANCIAL*"]
    for item in fin_news[:2]:
        title = escape_md(item["title"])
        link = item.get("link", "")
        if link:
            lines.append(f"• [{title}]({link})")
        else:
            lines.append(f"• {title}")
    lines += ["", "⚽ *BOLA EROPA*"]
    for item in bola_news[:2]:
        title = escape_md(item["title"])
        link = item.get("link", "")
        if link:
            lines.append(f"• [{title}]({link})")
        else:
            lines.append(f"• {title}")
    lines += [
        "",
        f"{'─' * 30}",
        "🤖 _Bot Berita Harian \\| Sampai jumpa besok pagi\\!_",
    ]
    return "\n".join(lines)
