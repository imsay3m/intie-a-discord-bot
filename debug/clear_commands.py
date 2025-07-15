import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# --- Configuration & Bot Definition ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))


class ClearBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("--- CLEARING COMMANDS ---")

        # 1. Clear all commands for the specific guild
        guild_obj = discord.Object(id=GUILD_ID)
        self.tree.clear_commands(guild=guild_obj)
        await self.tree.sync(guild=guild_obj)
        print(f"✅ Cleared all commands for guild: {GUILD_ID}")

        # 2. Clear all global commands
        self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=None)
        print("✅ Cleared all global commands.")

        print("--- Command cache cleared. You can now stop this script (Ctrl+C). ---")

        await self.close()

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} to perform command cleanup.")


# --- Run the cleanup script ---
if __name__ == "__main__":
    clear_bot = ClearBot()
    clear_bot.run(BOT_TOKEN)
