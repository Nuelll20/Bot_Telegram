# 🤖 Bot Telegram Berita Harian

Bot Telegram yang mengirimkan update berita otomatis setiap hari tentang:
- 🌍 **Geopolitik Global** — Konflik, diplomasi, hubungan internasional
- 💹 **Financial Global** — Pasar saham, komoditas, ekonomi dunia
- 🇮🇩 **Keuangan Indonesia** — IHSG, ekonomi nasional, kebijakan BI
- ⚽ **Sepak Bola Eropa** — Premier League, La Liga, Serie A, UCL, dll

---

## 📋 Persyaratan

- Python 3.10+
- Akun Telegram
- Token Bot Telegram (dari [@BotFather](https://t.me/BotFather))

---

## 🚀 Cara Setup

### 1. Clone / Download proyek ini

```bash
cd telegram-newsbot
```

### 2. Buat Virtual Environment (disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Buat file `.env`

Salin file contoh:
```bash
cp .env.example .env
```

Edit file `.env` dan isi konfigurasi:

```env
# Token bot dari @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCDefGhIJKlmNOpqRSTUvwXYZ

# ID channel atau group tujuan
# Untuk channel publik: @namaChannel
# Untuk channel/group private: gunakan chat ID (angka negatif)
# Cara dapat chat ID: tambahkan @userinfobot ke group, lalu /start
TELEGRAM_CHAT_ID=@nama_channel_anda

# Jadwal (format 24 jam, WIB)
SCHEDULE_GEOPOLITIK=07:00
SCHEDULE_FINANCIAL=08:00
SCHEDULE_BOLA=09:00
SCHEDULE_RINGKASAN_MALAM=21:00
```

### 5. Setup Bot di Telegram

**Buat Bot Baru:**
1. Buka [@BotFather](https://t.me/BotFather) di Telegram
2. Ketik `/newbot`
3. Ikuti instruksi, beri nama dan username bot
4. Copy token yang diberikan ke file `.env`

**Tambahkan Bot ke Channel/Group:**
1. Buka channel atau group Telegram Anda
2. Tambahkan bot sebagai **Admin** dengan izin "Post Messages"
3. Copy Chat ID channel ke file `.env`

> **💡 Cara dapat Chat ID:**
> - Untuk channel: gunakan format `@username_channel`
> - Untuk group/channel private: tambahkan [@userinfobot](https://t.me/userinfobot), forward pesan dari group ke bot tersebut

### 6. Jalankan Bot

```bash
python main.py
```

Bot akan mulai berjalan dan mengirim berita sesuai jadwal yang telah ditentukan.

---

## 📌 Perintah Bot

| Perintah | Fungsi |
|----------|--------|
| `/start` | Tampilkan info bot dan jadwal |
| `/help` | Bantuan penggunaan |
| `/jadwal` | Lihat jadwal update otomatis |
| `/geopolitik` | Ambil berita geopolitik sekarang |
| `/financial` | Ambil berita keuangan sekarang |
| `/bola` | Ambil berita sepak bola sekarang |
| `/semuaberita` | Kirim semua kategori berita sekarang |

---

## ⏰ Jadwal Broadcast Otomatis (Default WIB)

| Waktu | Kategori |
|-------|----------|
| 07:00 | 🌍 Geopolitik Global |
| 08:00 | 💹 Financial & Ekonomi |
| 09:00 | ⚽ Sepak Bola Eropa |
| 21:00 | 🌙 Ringkasan Malam (semua kategori) |

Jadwal dapat diubah di file `.env`.

---

## 📰 Sumber Berita (RSS Feed)

### Geopolitik
- BBC World News
- CNN International
- Reuters World
- Al Jazeera
- Foreign Policy
- Kompas Internasional
- Detik Geopolitik

### Financial Global
- Bloomberg Markets
- Financial Times
- Reuters Business
- MarketWatch
- CNBC Economy

### Keuangan Indonesia
- Bisnis Indonesia
- CNBC Indonesia
- Detik Finance
- Kompas Money
- Antara Ekonomi
- Katadata

### Sepak Bola Eropa
- BBC Sport Football
- Goal.com
- Sky Sports Football
- The Guardian Football
- Bola Kompas
- Detik Sport

---

## 🔧 Konfigurasi Lanjutan

### Menambah RSS Feed Baru

Edit `config/settings.py`, tambahkan URL RSS ke list yang sesuai:

```python
FEEDS_GEOPOLITIK = [
    "https://url-rss-baru.com/feed",
    # ... feed lainnya
]
```

### Menambah Klub Eropa yang Dipantau

```python
KLUB_EROPA = [
    "Nama Klub Baru",
    # ... klub lainnya
]
```

### Mengubah Jumlah Berita

```python
MAX_NEWS_GEOPOLITIK = 5   # Jumlah berita geopolitik
MAX_NEWS_FINANCIAL  = 5   # Jumlah berita finansial
MAX_NEWS_BOLA       = 6   # Jumlah berita bola
```

---

## 🖥️ Menjalankan di Server (Production)

### Menggunakan systemd (Linux)

Buat file service `/etc/systemd/system/newsbot.service`:

```ini
[Unit]
Description=Telegram News Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/telegram-newsbot
ExecStart=/path/to/telegram-newsbot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktifkan:
```bash
sudo systemctl enable newsbot
sudo systemctl start newsbot
sudo systemctl status newsbot
```

### Menggunakan Screen / tmux

```bash
screen -S newsbot
python main.py
# Ctrl+A, D untuk detach
```

---

## 📁 Struktur Proyek

```
telegram-newsbot/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env.example             # Template konfigurasi
├── .env                     # Konfigurasi Anda (jangan di-commit!)
├── bot.log                  # Log file (auto-generated)
├── config/
│   └── settings.py          # Semua konfigurasi & RSS feeds
├── handlers/
│   └── commands.py          # Handler perintah bot
├── services/
│   └── rss_fetcher.py       # Pengambil & filter berita RSS
├── scheduler/
│   └── jobs.py              # Job broadcast otomatis
└── utils/
    └── formatter.py         # Format pesan Telegram
```

---

## 🛡️ Catatan Keamanan

- **Jangan upload file `.env` ke GitHub** — tambahkan ke `.gitignore`
- Gunakan environment variables di server production
- Bot token bersifat rahasia, jangan dibagikan

---

## 🐛 Troubleshooting

**Bot tidak merespons:**
- Pastikan token di `.env` benar
- Pastikan bot sudah di-start dengan `/start`

**Berita tidak terkirim ke channel:**
- Pastikan bot sudah menjadi admin channel dengan izin posting
- Pastikan `TELEGRAM_CHAT_ID` benar (coba gunakan chat ID numerik)

**Error saat fetch berita:**
- Beberapa RSS feed mungkin memblokir request — hal ini normal
- Bot akan tetap berjalan dengan feed yang tersedia

---

Dibuat dengan ❤️ menggunakan Python + python-telegram-bot
