import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import re

print("🔥 Bot file is running...")

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = 1380979689375535235

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

PRIORITY_LEVELS = ["lowest", "low", "high", "highest"]
LOCATION_OPTIONS = ["Backlog", "Current Sprint"]

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
    priority="Priority level (lowest, low, high, highest)",
    story_point_estimate="Estimated story points (decimals allowed, must be > 0)",
    epic="(Optional) Epic ticket ID (e.g. PSB-57)",
    location="Where should this ticket go?"
)
@app_commands.choices(location=[
    app_commands.Choice(name="Backlog", value="Backlog"),
    app_commands.Choice(name="Current Sprint", value="Current Sprint")
])
async def ticket_request(
    interaction: discord.Interaction,
    assignee: discord.Member,
    description: str,
    priority: str,
    story_point_estimate: float,
    location: app_commands.Choice[str],
    epic: str = None  # Optional
):
    priority = priority.lower()
    if priority not in PRIORITY_LEVELS:
        await interaction.response.send_message(
            f"❌ Invalid priority '{priority}'. Please use one of: {', '.join(PRIORITY_LEVELS)}", ephemeral=True
        )
        return

    if story_point_estimate <= 0:
        await interaction.response.send_message(
            "❌ Story point estimate must be greater than 0.", ephemeral=True
        )
        return

    if epic and not re.fullmatch(r"[A-Z]{2,10}-\d+", epic):
        await interaction.response.send_message(
            "❌ Epic format must be like PSB-57 (uppercase letters, dash, number).", ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📝 New Ticket Request",
        color=discord.Color.blue()
    )
    embed.add_field(name="Assignee", value=assignee.mention, inline=False)
    embed.add_field(name="Priority", value=priority, inline=False)
    embed.add_field(name="Description", value=description, inline=False)
    embed.add_field(name="Story Points", value=str(story_point_estimate), inline=False)
    embed.add_field(name="Location", value=location.value, inline=False)

    if epic:
        embed.add_field(name="Epic", value=epic, inline=False)

    embed.set_footer(text="Use this to create a Jira ticket.")
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
