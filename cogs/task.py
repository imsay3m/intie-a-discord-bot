import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from utils.config import settings
from utils.decorators import admin_only


class Task(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="task",
        description="Posts the predefined task message to a specific channel.",
    )
    @admin_only()
    async def task(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if interaction.channel.id != settings.TASK_COMMAND_CHANNEL_ID:
            command_channel = self.bot.get_channel(settings.TASK_COMMAND_CHANNEL_ID)
            mention = (
                command_channel.mention
                if command_channel
                else f"`#{settings.TASK_COMMAND_CHANNEL_ID}`"
            )
            await interaction.edit_original_response(
                content=f"❌ This command can only be used in the {mention} channel."
            )
            await asyncio.sleep(10)
            return await interaction.delete_original_response()

        target_channel = self.bot.get_channel(settings.TASK_TARGET_CHANNEL_ID)

        if not target_channel:
            await interaction.edit_original_response(
                content=f"❌ **Error:** The target channel with ID `{settings.TASK_TARGET_CHANNEL_ID}` could not be found."
            )
            return
        processed_message = settings.TASK_MESSAGE.replace("\\n", "\n")

        try:
            await target_channel.send(processed_message)
        except discord.Forbidden:
            await interaction.edit_original_response(
                content=f"❌ **Error:** I don't have permission to send messages in the {target_channel.mention} channel."
            )
            return
        except Exception as e:
            print(f"Error sending task message: {e}")
            await interaction.edit_original_response(
                content="❌ An unexpected error occurred while posting the task message."
            )
            return

        await interaction.edit_original_response(
            content=f"✅ Successfully sent the task message to {target_channel.mention}."
        )
        await asyncio.sleep(5)
        await interaction.delete_original_response()


async def setup(bot):
    await bot.add_cog(Task(bot))
