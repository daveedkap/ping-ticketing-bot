import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

print("🔥 Bot is starting...")

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_hook():
    await bot.load_extension("commands.ticket_request")
    await bot.load_extension("commands.epic_request")

bot.setup_hook = setup_hook  # ✅ assign it like this — no decorator

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=1380979689375535235))
        print(f'🔁 Synced {len(synced)} commands.')
    except Exception as e:
        print(f'❌ Sync failed: {e}')
    
    print("✅ Commands registered:")
    for cmd in bot.tree.get_commands(guild=discord.Object(id=1380979689375535235)):
        print(f" - /{cmd.name}")

bot.run(TOKEN)
