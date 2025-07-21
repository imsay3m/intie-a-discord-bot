import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands

from utils import response_utils
from utils.config import settings


class ModeratorBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.tree.interaction_check = self.is_in_guild

    async def is_in_guild(self, interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ My commands can only be used inside a server.", ephemeral=True
            )
            return False
        return True

    async def setup_hook(self):
        from utils.database import init_db

        print("Database: Initializing...")
        init_db()

        print("--- Loading Cogs ---")
        cog_map = {
            "moderation.py": settings.ENABLE_COG_MODERATION,
            "messaging.py": settings.ENABLE_COG_MESSAGING,
            "info.py": settings.ENABLE_COG_INFO,
            "help.py": settings.ENABLE_COG_HELP,
            "task.py": settings.ENABLE_COG_TASK,
        }

        for filename, is_enabled in cog_map.items():
            if is_enabled:
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"✅ Loaded cog: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load cog {filename}: {e}")
            else:
                print(f"⏩ Skipped loading disabled cog: {filename}")

        print("--- Registering and Syncing Commands ---")
        guild_obj = discord.Object(id=settings.GUILD_ID)
        self.tree.copy_global_to(guild=guild_obj)
        try:
            synced = await self.tree.sync(guild=guild_obj)
            print(f"--- Synced {len(synced)} commands to the guild. ---")
        except Exception as e:
            print(f"❌ FAILED TO SYNC: {e}")

    async def on_ready(self):
        print("-----------------------------------------")
        print(f"✅ Logged in as {self.user}")
        print(f"🤖 Bot is ready and online!")
        print("-----------------------------------------")


bot = ModeratorBot()


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    """
    Catches all errors from slash commands globally.
    """
    if isinstance(error, app_commands.CheckFailure):
        # This error is raised when a decorator check (like @admin_only) fails.
        await response_utils.send_error_message(
            interaction, "You do not have the required permissions to use this command."
        )
    else:
        print(
            f"An unhandled error occurred in command '{interaction.command.name if interaction.command else 'unknown'}': {error}"
        )
        await response_utils.send_error_message(
            interaction, "An unexpected error occurred. Please try again later."
        )


async def main():
    await bot.start(settings.BOT_TOKEN)


if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.makedirs("logs")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot shutting down.")
