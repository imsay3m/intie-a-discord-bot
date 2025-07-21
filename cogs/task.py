import asyncio
from typing import Optional

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
        description="Posts the predefined task message with optional mentions.",
    )
    @app_commands.describe(
        mentions="Optional: Mention one or more users, separated by spaces."
    )
    @admin_only()
    async def task(
        self, interaction: discord.Interaction, mentions: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)

        if interaction.channel.id != settings.TASK_COMMAND_CHANNEL_ID:
            command_channel = self.bot.get_channel(settings.TASK_COMMAND_CHANNEL_ID)
            mention_str = (
                command_channel.mention
                if command_channel
                else f"`#{settings.TASK_COMMAND_CHANNEL_ID}`"
            )
            await interaction.edit_original_response(
                content=f"❌ This command can only be used in the {mention_str} channel."
            )
            await asyncio.sleep(10)
            return await interaction.delete_original_response()

        target_channel = self.bot.get_channel(settings.TASK_TARGET_CHANNEL_ID)
        if not target_channel:
            return await interaction.edit_original_response(
                content=f"❌ **Error:** The target channel could not be found."
            )

        mention_prefix = ""
        if mentions:
            mention_prefix = mentions

        processed_message = settings.TASK_MESSAGE.replace("\\n", "\n")
        final_message = (
            f"{mention_prefix}\n\n{processed_message}"
            if mention_prefix
            else processed_message
        )
        allowed_mentions = discord.AllowedMentions(
            everyone=True,
            users=True,
            roles=True,
            replied_user=False,
        )

        try:
            await target_channel.send(final_message, allowed_mentions=allowed_mentions)
        except discord.Forbidden:
            return await interaction.edit_original_response(
                content=f"❌ **Error:** I don't have permission to send messages or mentions in {target_channel.mention}."
            )
        except Exception as e:
            print(f"Error sending task message: {e}")
            return await interaction.edit_original_response(
                content=f"❌ An unexpected error occurred."
            )

        await interaction.edit_original_response(
            content=f"✅ Successfully sent the task message to {target_channel.mention}."
        )
        await asyncio.sleep(5)
        await interaction.delete_original_response()


async def setup(bot):
    await bot.add_cog(Task(bot))
