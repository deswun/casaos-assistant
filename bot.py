import os
import time
import requests
import psutil
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    """Mengirim pesan teks ke Telegram."""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        print(f"[Error kirim pesan]: {e}")

def get_system_status():
    """Membaca metrik hardware laptop/server."""
    cpu_usage = psutil.cpu_percent(interval=0.5)
    
    ram = psutil.virtual_memory()
    ram_used = ram.used / (1024 ** 3)
    ram_total = ram.total / (1024 ** 3)
    
    disk = psutil.disk_usage('/')
    disk_free = disk.free / (1024 ** 3)
    
    battery = psutil.sensors_battery()
    if battery:
        plugged = "🔌 Tercolok Charger" if battery.power_plugged else "🔋 Baterai"
        battery_text = f"{battery.percent}% ({plugged})"
    else:
        battery_text = "Tidak terdeteksi"

    return (
        "📊 *Status Server CasaOS*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🖥️ *CPU:* `{cpu_usage}%`\n"
        f"🧠 *RAM:* `{ram_used:.2f} GB` / `{ram_total:.2f} GB` (`{ram.percent}%`)\n"
        f"💾 *Disk Free:* `{disk_free:.2f} GB`\n"
        f"⚡ *Power:* `{battery_text}`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟢 _Sistem aktif normal._"
    )

def main():
    print(f"🤖 Bot CasaOS Assistant Aktif...")
    print(f"👉 Target Chat ID: {ALLOWED_CHAT_ID}")
    
    # Kirim tes langsung saat bot menyala
    if ALLOWED_CHAT_ID:
        send_message(ALLOWED_CHAT_ID, "🚀 *CasaOS Assistant v1.0 telah online!*")

    offset = None

    while True:
        try:
            params = {"offset": offset, "timeout": 5}
            response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=10)
            data = response.json()

            if "result" in data:
                for update in data["result"]:
                    # Geser offset agar pesan yang sudah dibaca tidak diulang
                    offset = update["update_id"] + 1

                    if "message" not in update:
                        continue

                    message = update["message"]
                    chat_id = str(message["chat"]["id"])
                    text = message.get("text", "").strip()

                    print(f"📩 Pesan masuk dari {chat_id}: '{text}'")

                    # Validasi ID pengirim
                    if chat_id != str(ALLOWED_CHAT_ID).strip():
                        print(f"⛔ Akses ditolak untuk chat_id: {chat_id}")
                        continue

                    # Respon perintah
                    if text in ["/start", "/help"]:
                        send_message(
                            chat_id,
                            "👋 *Halo Andre!*\n\n"
                            "Gunakan perintah berikut:\n"
                            "🔹 `/status` - Cek CPU, RAM, Disk, Baterai\n"
                            "🔹 `/ping` - Cek koneksi server"
                        )
                    elif text == "/status":
                        send_message(chat_id, get_system_status())
                    elif text == "/ping":
                        send_message(chat_id, "🏓 *Pong!* Server CasaOS Anda aktif.")

        except Exception as e:
            print(f"[Error Loop]: {e}")
            time.sleep(3)

        time.sleep(1)

if __name__ == "__main__":
    main()