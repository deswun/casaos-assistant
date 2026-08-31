# CasaOS Assistant

Simple Telegram bot for monitoring a CasaOS server.

CasaOS Assistant monitors basic system resources and can automatically send alerts when the server experiences high CPU temperature or a change in power status.

## Features

- CPU usage monitoring
- CPU temperature monitoring
- RAM usage monitoring
- Disk space monitoring
- Battery and power status
- Server uptime
- Automatic high-temperature alerts
- Automatic power status alerts
- Telegram-based monitoring
- Chat ID access restriction

## Commands

| Command | Description |
|---|---|
| `/start` | Show available commands |
| `/help` | Show available commands |
| `/status` | Show complete server status |
| `/temp` | Check current CPU temperature |
| `/uptime` | Check server uptime |
| `/ping` | Check server connection |

## Automatic Alerts

CasaOS Assistant runs a background monitor and checks the server every 10 seconds.

### High CPU Temperature

The default temperature threshold is **75°C**.

When the CPU temperature reaches the threshold, the bot sends an alert to Telegram.

Temperature alerts have a **5-minute cooldown** to prevent message spam.

### Power Status

The bot detects changes in the server's power status.

It can notify you when:

- The charger is disconnected or power is lost.
- The charger is connected again and power returns to normal.

## Requirements

- Linux server
- CasaOS
- Python 3
- Telegram Bot
- Telegram Chat ID

## Installation

Clone the repository:

```bash
git clone https://github.com/deswun/casaos-assistant.git
cd casaos-assistant
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project directory:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
ALLOWED_CHAT_ID=your_chat_id
```

Replace:

- `your_bot_token` with your Telegram Bot Token.
- `your_chat_id` with your Telegram Chat ID.

## Run

Start the bot:

```bash
python3 bot.py
```

If everything is configured correctly, the bot will start monitoring the server and send an online notification to Telegram.

## Example

Use `/status` to get a summary of the server:

```text
📊 CasaOS Server Status
━━━━━━━━━━━━━━━━━━━━
🖥️ CPU: 12.5% (Temperature: 48.0°C)
🧠 RAM: 2.10 GB / 7.70 GB (27%)
💾 Disk Free: 450.20 GB
⚡ Power: 🔌 Charger Connected
⏱️ Uptime: 2 days 5 hours 20 minutes
━━━━━━━━━━━━━━━━━━━━
🟢 System is running normally.
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

## Version

**Current version: 1.1**

### v1.1 Changes

- Added CPU temperature monitoring
- Added `/temp` command
- Added `/uptime` command
- Added automatic high-temperature alerts
- Added automatic power status alerts
- Added background monitoring
- Added temperature alert cooldown

## License

This project is for personal and educational use.
