import os
import discord
from discord import app_commands
from discord.ext import commands

class EpicRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="epic-request",
        description="Submit a new Epic for planning and tracking"
    )
    @app_commands.describe(
        title="A short, clear name for the epic",
        description="High-level overview of the epic's purpose",
        goal="What success looks like / why this epic matters",
        assignee="(Optional) Who's driving or leading this epic"
    )
    async def epic_request(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        goal: str,
        assignee: discord.Member = None
    ):
        await interaction.response.defer()

        embed = discord.Embed(
            title="📌 New Epic Request",
            color=discord.Color.purple()
        )

        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Goal", value=goal, inline=False)

        if assignee:
            embed.add_field(name="Assignee", value=assignee.mention, inline=False)
        else:
            embed.add_field(name="Assignee", value="(Unassigned)", inline=False)

        embed.set_footer(text="Use this to create a high-level Epic in Jira.")
        await interaction.followup.send(embed=embed)  # ✅ Final response

    async def cog_load(self):
        GUILD_ID = int(os.getenv("GUILD_ID"))
        print("📦 Registering /epic-request to GUILD_ID:", GUILD_ID)
        self.bot.tree.add_command(self.epic_request, guild=discord.Object(id=GUILD_ID))

async def setup(bot: commands.Bot):
    await bot.add_cog(EpicRequest(bot))
