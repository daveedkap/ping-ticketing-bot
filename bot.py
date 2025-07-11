import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from flask import Flask
from threading import Thread

print("🔥 Bot is starting...")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask keep-alive server for Render
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Load command extensions
async def setup_hook():
    await bot.load_extension("commands.ticket_request")
    await bot.load_extension("commands.epic_request")

bot.setup_hook = setup_hook 

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        # Sync to your production server only
        synced = await bot.tree.sync(guild=discord.Object(id=1380979689375535235))
        print(f'🔁 Synced {len(synced)} commands.')
    except Exception as e:
        print(f'❌ Sync failed: {e}')
    
    print("✅ Commands registered:")
    for cmd in bot.tree.get_commands(guild=discord.Object(id=1380979689375535235)):
        print(f" - /{cmd.name}")

# Start Flask server in background thread
Thread(target=run).start()

# Run the bot
bot.run(TOKEN)
