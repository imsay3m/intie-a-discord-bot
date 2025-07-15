import discord


async def send_ephemeral_followup(
    interaction: discord.Interaction,
    message: str,
    color=discord.Color.green(),
    delete_after: int = None,
):
    """Sends a standardized ephemeral followup message."""
    embed = discord.Embed(description=message, color=color)
    await interaction.followup.send(
        embed=embed, ephemeral=True, delete_after=delete_after
    )


async def send_error_message(interaction: discord.Interaction, message: str):
    """Sends a standardized ephemeral error message."""
    embed = discord.Embed(description=f"❌ {message}", color=discord.Color.red())
    if not interaction.response.is_done():
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.followup.send(embed=embed, ephemeral=True)
