# CasaOS Assistant

Telegram bot sederhana untuk memantau status server CasaOS.

Bot ini dapat digunakan untuk mengecek kondisi CPU, RAM, penyimpanan, baterai, dan koneksi server langsung melalui Telegram.

## Features

- Cek status CPU
- Cek penggunaan RAM
- Cek ruang disk yang tersedia
- Cek status baterai
- Cek koneksi server
- Akses bot dibatasi berdasarkan Telegram Chat ID
- Berjalan menggunakan Python

## Commands

| Command | Fungsi |
|---|---|
| `/start` | Menampilkan bantuan |
| `/help` | Menampilkan daftar perintah |
| `/status` | Melihat status server |
| `/ping` | Mengecek koneksi server |

## Requirements

- Python 3
- Server Linux / CasaOS
- Telegram Bot
- Telegram Chat ID

## Installation

Clone repository:

```bash
git clone https://github.com/deswun/casaos-assistant.git
cd casaos-assistant
```

Buat virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Buat file `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
ALLOWED_CHAT_ID=your_chat_id
```

Ganti:

- `your_bot_token` dengan token bot dari Telegram BotFather
- `your_chat_id` dengan Chat ID Telegram yang diizinkan menggunakan bot

## Run

Jalankan bot dengan:

```bash
python3 bot.py
```

Jika berhasil, bot akan aktif dan dapat digunakan melalui Telegram.

## Example

Gunakan `/status` di Telegram untuk mendapatkan informasi seperti:

```text
📊 Status Server CasaOS
━━━━━━━━━━━━━━━━━━━━
🖥️ CPU: 12.5%
🧠 RAM: 2.10 GB / 7.70 GB (27%)
💾 Disk Free: 450.20 GB
⚡ Power: 🔌 Tercolok Charger
━━━━━━━━━━━━━━━━━━━━
🟢 Sistem aktif normal.
```

## Project Structure

```text
casaos-assistant/
├── bot.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Notes

Project ini masih dalam tahap pengembangan dan fitur dapat bertambah di kemudian hari.

## License

This project is for personal and educational use.
