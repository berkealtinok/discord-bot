import os
import discord
from discord.ext import commands
import requests

# ENV Variablen auslesen
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_IDS = os.getenv("TELEGRAM_USER_IDS", "").split(",")  # Komma-getrennte Liste

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

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
