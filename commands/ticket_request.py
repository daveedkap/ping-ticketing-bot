import re
import os
import discord
from discord import app_commands
from discord.ext import commands

class TicketRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MODE = os.getenv("MODE")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))
        self.PROD_CHANNEL_ID = int(os.getenv("PROD_CHANNEL_ID"))

    @app_commands.command(
        name="ticket-request",
        description="Submit a structured ticket request"
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
        self,
        interaction: discord.Interaction,
        description: str,
        story_point_estimate: float,
        priority: app_commands.Choice[str],
        location: app_commands.Choice[str],
        assignee: discord.Member = None,
        epic: str = None,
        work_type: app_commands.Choice[str] = None
    ):
        await interaction.response.defer()

        if self.MODE == "test":
            if interaction.channel_id != self.TEST_CHANNEL_ID:
                if interaction.channel_id == self.PROD_CHANNEL_ID:
                    await interaction.followup.send(
                        "⚠️ This is the **staging bot** for development only.\nPlease use the official `ping-ticketing-bot` for real ticket submissions in this channel.",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        "🚫 You can't use this command in this channel.", ephemeral=True
                    )
                return

        elif self.MODE == "prod":
            if interaction.channel_id != self.PROD_CHANNEL_ID:
                await interaction.followup.send(
                    "🚫 You can't use this command in this channel.", ephemeral=True
                )
                return

        if story_point_estimate <= 0:
            await interaction.followup.send(
                "❌ Story point estimate must be greater than 0.", ephemeral=True
            )
            return

        if epic and not re.fullmatch(r"[A-Z]{2,10}-\d+", epic):
            await interaction.followup.send(
                "❌ Epic format must be like PSB-57 (uppercase letters, dash, number).", ephemeral=True
            )
            return

        work_type_value = work_type.value if work_type else "Task"

        # EMBED CONSTRUCTION
        embed = discord.Embed(
            title="📝 New Ticket Request",
            color=discord.Color.blue()
        )

        embed.add_field(name="Assignee", value=assignee.mention if assignee else "(Unassigned)", inline=False)
        embed.add_field(name="Priority", value=priority.value, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Story Points", value=str(story_point_estimate), inline=False)
        embed.add_field(name="Location", value=location.value, inline=False)

        if epic:
            embed.add_field(name="Epic", value=epic, inline=False)

        embed.add_field(name="Work Type", value=work_type_value, inline=False)
        embed.set_footer(text="Use this to create a Jira ticket.")

        await interaction.followup.send(embed=embed) 

    async def cog_load(self):
        print("📦 Registering /ticket-request to GUILD_ID:", self.GUILD_ID)
        self.bot.tree.add_command(self.ticket_request, guild=discord.Object(id=self.GUILD_ID))

async def setup(bot: commands.Bot):
    await bot.add_cog(TicketRequest(bot))
