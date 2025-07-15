# main.py
import asyncio
import os

import discord
from discord.ext import commands

# Import the single settings instance from our config utility
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

        # The cog map now references the attributes of the 'settings' object
        cog_map = {
            "moderation.py": settings.ENABLE_COG_MODERATION,
            "messaging.py": settings.ENABLE_COG_MESSAGING,
            "info.py": settings.ENABLE_COG_INFO,
            "help.py": settings.ENABLE_COG_HELP,
        }

        for filename, is_enabled in cog_map.items():
            if is_enabled:
                try:
                    # We have to use a relative path here for the extension loader
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


async def main():
    bot = ModeratorBot()
    # Use the token from the settings object
    await bot.start(settings.BOT_TOKEN)


if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.makedirs("logs")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot shutting down.")
