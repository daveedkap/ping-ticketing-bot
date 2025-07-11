import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
import os

MODE = os.environ.get("MODE", "prod") 
load_dotenv(dotenv_path=f".env.{MODE}")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

print(f"🔥 Starting bot in {MODE.upper()} mode...")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True  # Only needed if you're handling text messages
bot = commands.Bot(command_prefix="!", intents=intents)

# Keep-alive Flask server (only for Render prod)
if MODE == "prod":
    app = Flask('')

    @app.route('/')
    def home():
        return "✅ Bot is running!"

    def run():
        app.run(host='0.0.0.0', port=8080)

    Thread(target=run).start()

# Setup command loading
async def setup_hook():
    await bot.load_extension("commands.ticket_request")
    await bot.load_extension("commands.epic_request")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')

    guild = discord.Object(id=GUILD_ID)
    synced = await bot.tree.sync(guild=guild)
    print(f"✅ Synced {len(synced)} slash command(s) to guild {GUILD_ID}.")

bot.run(TOKEN)
