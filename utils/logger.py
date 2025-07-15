from datetime import datetime

LOG_FILE = "logs/moderation_actions.log"


def log_action(
    moderator: str, action: str, target: str, reason: str = "No reason provided"
):
    """
    Logs a moderation action to the specified log file.

    Args:
        moderator (str): The ID of the moderator performing the action.
        action (str): The type of action (e.g., KICK, BAN, WARN).
        target (str): The ID of the user being actioned.
        reason (str): The reason for the action.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"[{timestamp}] MODERATOR_ID={moderator} | ACTION={action.upper()} | TARGET_ID={target} | REASON='{reason}'\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
