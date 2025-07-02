import os
import discord
from discord.ext import commands
import requests

# Intents einrichten (Pflicht ab discord.py v2)
intents = discord.Intents.default()
intents.voice_states = True  # wichtig für Mikrofon-Events
intents.message_content = True  # erlaubt später auch Nachrichtenlesen
intents.members = True  # falls du z. B. Nutzerinfos brauchst

# ENV Variablen auslesen
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_IDS = os.getenv("TELEGRAM_USER_IDS", "").split(",")  # Komma-getrennte Liste

# Bot initialisieren mit Intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Wenn Mikro angeschaltet wird (z.B. Stummschaltung aufgehoben)
    if before.self_mute and not after.self_mute:
        for user_id in TELEGRAM_USER_IDS:
            send_telegram_alert(user_id, f"🔊 {member.display_name} hat gerade sein Mikro eingeschaltet!")

def send_telegram_alert(user_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": user_id,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Fehler beim Senden an Telegram: {e}")

bot.run(DISCORD_TOKEN)
