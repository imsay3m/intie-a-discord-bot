import os

import discord
from discord import app_commands
from dotenv import load_dotenv

# --- Load Configuration ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

# --- Define Intents ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# --- Define a Single Test Command ---
@tree.command(
    name="ping", description="A simple test command.", guild=discord.Object(id=GUILD_ID)
)
async def ping(interaction: discord.Interaction):
    """Responds with Pong!"""
    await interaction.response.send_message("Pong!", ephemeral=True)


# --- Define Bot Startup ---
@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    print("Attempting to sync commands...")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"--- Synced {len(synced)} commands ---")
        if len(synced) > 0:
            print("✅ SUCCESS: Commands have been synced.")
            print(
                "Please FULLY RESTART your Discord client and check for the /ping command."
            )
        else:
            print("❌ FAILURE: Synced 0 commands.")
            print(
                "This confirms the issue is NOT in the cogs. The problem is your BOT_TOKEN, GUILD_ID, or bot permissions."
            )
    except Exception as e:
        print(f"❌ FAILED TO SYNC WITH ERROR: {e}")
    print("-----------------------------------------")


# --- Run the Bot ---
if __name__ == "__main__":
    if not all([BOT_TOKEN, GUILD_ID]):
        print("❌ ERROR: Missing BOT_TOKEN or GUILD_ID in your .env file.")
    else:
        client.run(BOT_TOKEN)
