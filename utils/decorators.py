from discord import Interaction, app_commands, utils

from .config import settings


def is_admin(interaction: Interaction) -> bool:
    """The raw check function."""
    admin_role = utils.get(interaction.guild.roles, id=settings.ADMIN_ROLE_ID)
    if not admin_role:
        return False
    return admin_role in interaction.user.roles


def admin_only():
    """A decorator that checks if the user is an admin."""
    return app_commands.check(is_admin)
