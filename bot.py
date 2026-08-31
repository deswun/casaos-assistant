import os
import time
import threading
import datetime
import requests
import psutil
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Temperature threshold (Celsius)
TEMP_THRESHOLD = 75.0

# Previous power status tracker
last_power_plugged = None
last_alert_time = 0

def send_message(chat_id, text):
    """Send a text message to Telegram."""
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
        print(f"[Message send error]: {e}")

def get_cpu_temp():
    """Read laptop CPU temperature (Linux)."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        
        # Look for coretemp, cpu_thermal, or the first available sensor
        for name in ['coretemp', 'cpu_thermal', 'k10temp', 'acpitz']:
            if name in temps and temps[name]:
                return temps[name][0].current
        
        # Fallback to the first available sensor
        first_entry = next(iter(temps.values()))
        if first_entry:
            return first_entry[0].current
    except Exception:
        pass
    return None

def get_uptime():
    """Calculate how long the server has been running."""
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days = uptime.days
    
    if days > 0:
        return f"{days} days {hours} hours {minutes} minutes"
    return f"{hours} hours {minutes} minutes"

def get_system_status():
    """Read laptop/server hardware metrics."""
    cpu_usage = psutil.cpu_percent(interval=0.5)
    
    ram = psutil.virtual_memory()
    ram_used = ram.used / (1024 ** 3)
    ram_total = ram.total / (1024 ** 3)
    
    disk = psutil.disk_usage('/')
    disk_free = disk.free / (1024 ** 3)
    
    battery = psutil.sensors_battery()
    if battery:
        plugged = "🔌 Charger Connected" if battery.power_plugged else "🔋 Battery"
        battery_text = f"{battery.percent}% ({plugged})"
    else:
        battery_text = "Not detected"

    temp = get_cpu_temp()
    temp_text = f"`{temp}°C`" if temp is not None else "`N/A`"

    return (
        "📊 *CasaOS Server Status*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🖥️ *CPU:* `{cpu_usage}%` (Temperature: {temp_text})\n"
        f"🧠 *RAM:* `{ram_used:.2f} GB` / `{ram_total:.2f} GB` (`{ram.percent}%`)\n"
        f"💾 *Disk Free:* `{disk_free:.2f} GB`\n"
        f"⚡ *Power:* `{battery_text}`\n"
        f"⏱️ *Uptime:* `{get_uptime()}`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟢 _System is running normally._"
    )

def background_monitor():
    """Background thread for automatic temperature and power status alerts."""
    global last_power_plugged, last_alert_time
    
    # Initialize the initial power status
    initial_battery = psutil.sensors_battery()
    if initial_battery:
        last_power_plugged = initial_battery.power_plugged

    while True:
        try:
            # 1. Check for Power Status Changes (Charger Unplugged / Plugged In)
            battery = psutil.sensors_battery()
            if battery and last_power_plugged is not None:
                if battery.power_plugged != last_power_plugged:
                    if battery.power_plugged:
                        msg = f"🔌 *Power Back to Normal*\nLaptop is connected to the charger again. (Battery: `{battery.percent}%`)"
                    else:
                        msg = f"⚠️ *Warning: Power Disconnected!*\nThe laptop charger was disconnected/power was lost. The server is running on battery (`{battery.percent}%`)."
                    
                    send_message(ALLOWED_CHAT_ID, msg)
                    last_power_plugged = battery.power_plugged

            # 2. Check CPU Temperature Threshold (5-minute minimum alert cooldown to prevent spam)
            current_temp = get_cpu_temp()
            current_time = time.time()
            if current_temp and current_temp >= TEMP_THRESHOLD:
                if current_time - last_alert_time > 300:  # 300 seconds = 5 minutes
                    msg = (
                        f"🚨 *High Temperature Warning!*\n"
                        f"Laptop CPU temperature reached `{current_temp}°C` (Threshold: `{TEMP_THRESHOLD}°C`).\n"
                        f"Check the ventilation or running processes."
                    )
                    send_message(ALLOWED_CHAT_ID, msg)
                    last_alert_time = current_time

        except Exception as e:
            print(f"[Background Monitor Error]: {e}")

        time.sleep(10)  # Check every 10 seconds

def main():
    print(f"🤖 CasaOS Assistant v1.1 Bot Active...")
    
    if ALLOWED_CHAT_ID:
        send_message(ALLOWED_CHAT_ID, "🚀 *CasaOS Assistant v1.1 Online!* (Auto-Alert Active)")

    # Run the background monitor in a separate thread
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()

    offset = None

    while True:
        try:
            params = {"offset": offset, "timeout": 5}
            response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=10)
            data = response.json()

            if "result" in data:
                for update in data["result"]:
                    offset = update["update_id"] + 1

                    if "message" not in update:
                        continue

                    message = update["message"]
                    chat_id = str(message["chat"]["id"])
                    text = message.get("text", "").strip()

                    if chat_id != str(ALLOWED_CHAT_ID).strip():
                        continue

                    if text in ["/start", "/help"]:
                        send_message(
                            chat_id,
                            "👋 *CasaOS Assistant v1.1*\n\n"
                            "Available Commands:\n"
                            "🔹 `/status` - System status summary\n"
                            "🔹 `/temp` - Check laptop CPU temperature\n"
                            "🔹 `/uptime` - Server uptime\n"
                            "🔹 `/ping` - Check connection"
                        )
                    elif text == "/status":
                        send_message(chat_id, get_system_status())
                    elif text == "/temp":
                        temp = get_cpu_temp()
                        if temp:
                            send_message(chat_id, f"🌡️ *Current CPU Temperature:* `{temp}°C`")
                        else:
                            send_message(chat_id, "⚠️ Temperature sensor is not supported or cannot be read on this OS.")
                    elif text == "/uptime":
                        send_message(chat_id, f"⏱️ *Server Uptime:* `{get_uptime()}`")
                    elif text == "/ping":
                        send_message(chat_id, "🏓 *Pong!* Server responded quickly.")

        except Exception as e:
            print(f"[Loop Error]: {e}")
            time.sleep(3)

        time.sleep(1)

if __name__ == "__main__":
    main()