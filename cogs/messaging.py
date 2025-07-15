import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from utils import logger

# Import utils directly
from utils.decorators import admin_only


# This helper function will now serve both commands in this cog.
def parse_color(color_string: str) -> discord.Color:
    """
    Parses a user-provided string into a discord.Color object.
    Accepts common color names or a hex code (e.g., '#FF00FF').
    """
    color_string = color_string.lower().strip()
    color_map = {
        "blue": discord.Color.blue(),
        "red": discord.Color.red(),
        "green": discord.Color.green(),
        "orange": discord.Color.orange(),
        "purple": discord.Color.purple(),
        "gold": discord.Color.gold(),
        "teal": discord.Color.teal(),
        "magenta": discord.Color.magenta(),
        "yellow": discord.Color.yellow(),
        "white": 0xFFFFFF,
        "black": 0x000001,
    }
    if color_string in color_map:
        return color_map[color_string]
    if color_string.startswith("#"):
        try:
            return discord.Color(int(color_string[1:], 16))
        except ValueError:
            return discord.Color.default()
    return discord.Color.default()


# The class name is now more generic to reflect its purpose.
class Messaging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- ANNOUNCE COMMAND ---
    @app_commands.command(
        name="announce", description="Broadcasts a custom embedded announcement."
    )
    @app_commands.describe(
        title="The title of the announcement embed.",
        description="The main body of the announcement. Use '\\n' for new lines.",
        color="Optional: Color name (e.g., 'blue') or hex code (e.g., '#5865F2').",
    )
    @admin_only()
    async def announce(
        self,
        interaction: discord.Interaction,
        color: str,
        title: str,
        description: str,
    ):
        await interaction.response.defer(ephemeral=True)

        processed_description = description.replace("\\n", "\n")
        embed_color = parse_color(color) if color else discord.Color.blue()

        embed = discord.Embed(
            title=title, description=processed_description, color=embed_color
        )

        try:
            await interaction.channel.send(embed=embed)
        except discord.Forbidden:
            return await interaction.edit_original_response(
                content="❌ I do not have permission to send messages in this channel."
            )

        await interaction.edit_original_response(
            content="✅ Your custom announcement has been posted."
        )
        await asyncio.sleep(5)
        await interaction.delete_original_response()

    # --- SAY COMMAND (Now in the same cog) ---
    @app_commands.command(
        name="say", description="Sends an embedded message as the bot anonymously."
    )
    @app_commands.describe(
        message="The message to say. Use '\\n' for a new line.",
        color="Optional color name (e.g., 'red', 'blue') or hex code (e.g., '#FF5733').",
    )
    @admin_only()
    async def say(self, interaction: discord.Interaction, color: str, message: str):
        await interaction.response.defer(ephemeral=True)

        processed_message = message.replace("\\n", "\n")
        embed_color = parse_color(color) if color else discord.Color(0x2B2D31)

        embed = discord.Embed(description=processed_message, color=embed_color)

        try:
            await interaction.channel.send(embed=embed)
            logger.log_action(
                str(interaction.user.id),
                "SAY (EMBED)",
                f"channel:{interaction.channel.id}",
                processed_message,
            )
        except discord.Forbidden:
            return await interaction.edit_original_response(
                content="❌ I do not have permission to send messages in this channel."
            )

        await interaction.edit_original_response(
            content="✅ Your embedded message has been sent anonymously and logged."
        )
        await asyncio.sleep(5)
        await interaction.delete_original_response()


async def setup(bot):
    await bot.add_cog(Messaging(bot))
