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

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    try:
        synced = await client.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(e)

@client.tree.command(
    name="ticket-request",
    description="Submit a structured ticket request",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    assignee="(Optional) Tag a user to assign",
    description="2+ sentence description of the task, the more detail the better",
    story_point_estimate="Estimated story points (must be > 0)",
    epic="(Optional) Epic/Parent ticket ID (e.g. PSB-57)",
    priority="Select a priority level",
    location="Where should this ticket go?",
    work_type="(Optional) Choose the work type (defaults to Task)"
)
@app_commands.choices(
    priority=[
        app_commands.Choice(name="Highest", value="highest"),
        app_commands.Choice(name="High", value="high"),
        app_commands.Choice(name="Medium", value="medium"),
        app_commands.Choice(name="Low", value="low"),
        app_commands.Choice(name="Lowest", value="lowest"),
    ],
    location=[
        app_commands.Choice(name="Backlog", value="Backlog"),
        app_commands.Choice(name="Current Sprint", value="Current Sprint"),
    ],
    work_type=[
        app_commands.Choice(name="Bug", value="Bug"),
        app_commands.Choice(name="Story", value="Story"),
        app_commands.Choice(name="Task", value="Task"),
    ]
)
async def ticket_request(
    interaction: discord.Interaction,
    description: str,
    story_point_estimate: float,
    priority: app_commands.Choice[str],
    location: app_commands.Choice[str],
    assignee: discord.Member = None,
    epic: str = None,
    work_type: app_commands.Choice[str] = None  # ✅ Optional
):
    # Validate story point
    if story_point_estimate <= 0:
        await interaction.response.send_message(
            "❌ Story point estimate must be greater than 0.", ephemeral=True
        )
        return

    # Validate epic format (if provided)
    if epic and not re.fullmatch(r"[A-Z]{2,10}-\d+", epic):
        await interaction.response.send_message(
            "❌ Epic format must be like PSB-57 (uppercase letters, dash, number).", ephemeral=True
        )
        return

    # Default work_type if not provided
    work_type_value = work_type.value if work_type else "Task"

    # Build embedded ticket summary
    embed = discord.Embed(
        title="📝 New Ticket Request",
        color=discord.Color.blue()
    )

    if assignee:
        embed.add_field(name="Assignee", value=assignee.mention, inline=False)
    else:
        embed.add_field(name="Assignee", value="(Unassigned)", inline=False)

    embed.add_field(name="Priority", value=priority.value, inline=False)
    embed.add_field(name="Description", value=description, inline=False)
    embed.add_field(name="Story Points", value=str(story_point_estimate), inline=False)
    embed.add_field(name="Location", value=location.value, inline=False)

    if epic:
        embed.add_field(name="Epic", value=epic, inline=False)

    embed.add_field(name="Work Type", value=work_type_value, inline=False)

    embed.set_footer(text="Use this to create a Jira ticket.")
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
