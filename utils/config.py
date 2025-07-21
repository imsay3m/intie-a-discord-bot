import os

from dotenv import load_dotenv


class Config:
    """
    A class to hold all bot configuration.
    It loads variables from the .env file upon initialization.
    """

    def __init__(self):
        load_dotenv(override=True)

        # --- Getters with Type Casting ---
        self.BOT_TOKEN = self._get_env_var("BOT_TOKEN")
        self.GUILD_ID = self._get_env_var("GUILD_ID", cast_to=int)
        self.ADMIN_ROLE_ID = self._get_env_var("ADMIN_ROLE_ID", cast_to=int)
        self.TASK_COMMAND_CHANNEL_ID = self._get_env_var(
            "TASK_COMMAND_CHANNEL_ID", cast_to=int
        )
        self.TASK_TARGET_CHANNEL_ID = self._get_env_var(
            "TASK_TARGET_CHANNEL_ID", cast_to=int
        )
        self.TASK_MESSAGE = self._get_env_var("TASK_MESSAGE")

        # --- Cog Enable/Disable Switches ---
        self.ENABLE_COG_MODERATION = self._get_boolean_env_var("ENABLE_COG_MODERATION")
        self.ENABLE_COG_MESSAGING = self._get_boolean_env_var("ENABLE_COG_MESSAGING")
        self.ENABLE_COG_INFO = self._get_boolean_env_var("ENABLE_COG_INFO")
        self.ENABLE_COG_HELP = self._get_boolean_env_var("ENABLE_COG_HELP")
        self.ENABLE_COG_TASK = self._get_boolean_env_var("ENABLE_COG_TASK")

    def _get_env_var(self, key: str, default=None, cast_to=str):
        """Helper to get a required environment variable."""
        value = os.getenv(key)
        if value is None:
            if default is not None:
                return default
            raise ValueError(f"❌ Missing required environment variable: {key}")
        try:
            return cast_to(value)
        except (ValueError, TypeError):
            raise ValueError(f"❌ Invalid format for environment variable: {key}")

    def _get_boolean_env_var(self, key: str) -> bool:
        """Helper to get an enable/disable switch. Defaults to True."""
        value = os.getenv(key, "True").lower()
        return value in ["true", "1", "t", "y", "yes"]


settings = Config()
