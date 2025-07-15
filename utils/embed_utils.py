import discord


def create_log_embed(
    interaction: discord.Interaction,
    title: str,
    description: str,
    color: discord.Color,
    reason: str = None,
) -> discord.Embed:
    """Creates a standardized embed for moderation logs."""
    embed = discord.Embed(title=title, description=description, color=color)

    if reason:
        embed.add_field(name="Reason", value=reason, inline=False)

    embed.set_footer(text=f"Moderator: {interaction.user.display_name}")
    embed.timestamp = discord.utils.utcnow()

    return embed
