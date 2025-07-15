import discord


def is_target_valid(
    interaction: discord.Interaction, target: discord.Member
) -> str | None:
    """
    Validates if a member is a valid moderation target.
    Returns an error message string if invalid, otherwise returns None.
    """
    if target.id == interaction.client.user.id:
        return "❌ You cannot use this command on me."

    if target.id == interaction.user.id:
        return f"❌ You cannot {interaction.command.name} yourself."

    if target.top_role >= interaction.user.top_role:
        return "❌ You cannot moderate a member with an equal or higher role."

    return None
