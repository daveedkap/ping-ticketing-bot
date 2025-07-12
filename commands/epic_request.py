import os
import discord
from discord import app_commands
from discord.ext import commands

class EpicRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MODE = os.getenv("MODE")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))
        self.PROD_CHANNEL_ID = int(os.getenv("PROD_CHANNEL_ID"))

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
        try:
            await interaction.response.defer()
        except discord.NotFound:
            print("⚠️ Interaction expired or bot still starting up.")
            try:
                await interaction.followup.send(
                    "⚠️ Bot is still waking up from sleep. Please try again in a few seconds!",
                    ephemeral=True
                )
            except Exception:
                pass  # In case followup isn't available either
            return

        # CHANNEL RESTRICTION LOGIC
        if self.MODE == "test":
            if interaction.channel_id != self.TEST_CHANNEL_ID:
                if interaction.channel_id == self.PROD_CHANNEL_ID:
                    await interaction.followup.send(
                        "⚠️ This is the **development bot** for development only.\nPlease use the official `ping-ticketing-bot` for real ticket submissions in this channel.",
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

        # EMBED CONSTRUCTION
        embed = discord.Embed(
            title="📌 New Epic Request",
            color=discord.Color.purple()
        )

        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Goal", value=goal, inline=False)

        embed.add_field(
            name="Assignee",
            value=assignee.mention if assignee else "(Unassigned)",
            inline=False
        )

        embed.set_footer(text="Use this to create a high-level Epic in Jira.")
        await interaction.followup.send(embed=embed)

    async def cog_load(self):
        print("📦 Registering /epic-request to GUILD_ID:", self.GUILD_ID)
        self.bot.tree.add_command(self.epic_request, guild=discord.Object(id=self.GUILD_ID))

async def setup(bot: commands.Bot):
    await bot.add_cog(EpicRequest(bot))
