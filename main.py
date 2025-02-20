import discord
from discord.ext import commands, tasks
import json
import time
import os
# Bot Token
TOKEN = "MTMzOTg5MTg1NDI3OTE4NDQwNA.GnBpoF._QAv7My6xlQ8E2rPChb_9zlgZEKc5SeDYrHzF0"  # 🔹 Replace with your actual token

# Server & Channel Info
GUILD_ID = 1339192279470178375  # 🔹 Your server ID
CHANNEL_ID = 1339899780368695398  # 🔹 The channel to rename
USER_ID = 1330077541091770408  # 🔹 The user/bot to track
NEW_NAME = "bot-status•🟩"  # 🔹 Name when online
ORIGINAL_NAME = "bot-status•🟥"  # 🔹 Name when offline

# Cooldown Timer
COOLDOWN = 600  # 600 seconds (10 minutes)
last_status = None  # Track last known status
last_rename_time = 0  # Track last rename time

# Intents & Bot Setup
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

# Load settings from a JSON file
SETTINGS_FILE = "ticket_settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"ticket_category": None, "output_channel": None}, f)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

settings = load_settings()
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.load_extension("ticket")
    await bot.load_extension("mod")
    await bot.load_extension("embed")
    await bot.load_extension("chat")
    await bot.load_extension("help")
# Load ticket system
    check_status.start()  # Start status tracking

# Track user/bot status & rename channel
@tasks.loop(seconds=30)
async def check_status():
    global last_status, last_rename_time

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ ERROR: Guild not found!")
        return

    channel = guild.get_channel(CHANNEL_ID)
    user = guild.get_member(USER_ID)

    if not user:
        print("❌ ERROR: User not found!")
        return
    if not channel:
        print("❌ ERROR: Channel not found!")
        return

    current_status = user.status == discord.Status.online
    if current_status == last_status:  # Prevent redundant updates
        return

    current_time = time.time()
    if current_time - last_rename_time < COOLDOWN:  # 🔹 Enforce cooldown
        print(f"⏳ Cooldown active. Next change in {COOLDOWN - (current_time - last_rename_time):.0f} sec")
        return

    last_status = current_status  # Update last status
    last_rename_time = current_time  # Update last rename time

    new_name = NEW_NAME if current_status else ORIGINAL_NAME
    if channel.name != new_name:
        await channel.edit(name=new_name)
        print(f"✅ Changed channel name to '{new_name}'")



bot.run(TOKEN)
