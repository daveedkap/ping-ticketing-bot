import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

print("🔥 Bot file is running...")

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = 1380979689375535235

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

PRIORITY_LEVELS = ["lowest", "low", "high", "highest"]

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    try:
        synced = await client.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(e)

@client.tree.command(name="ticket-request", description="Submit a structured ticket request", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    assignee="Tag a user to assign",
    description="Short description of the task",
    priority="Priority level (lowest, low, high, highest)"
)
async def ticket_request(interaction: discord.Interaction, assignee: discord.Member, description: str, priority: str):
    priority = priority.lower()
    if priority not in PRIORITY_LEVELS:
        await interaction.response.send_message(
            f"❌ Invalid priority '{priority}'. Please use one of: {', '.join(PRIORITY_LEVELS)}", ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📝 New Ticket Request",
        color=discord.Color.blue()
    )
    embed.add_field(name="Assignee", value=assignee.mention, inline=False)
    embed.add_field(name="Priority", value=priority, inline=False)
    embed.add_field(name="Description", value=description, inline=False)
    embed.set_footer(text="Use this to create a Jira ticket.")

    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
