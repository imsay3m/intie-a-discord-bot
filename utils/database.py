import sqlite3
import threading

# --- DATABASE INITIALIZATION ---

# Use thread-local data to ensure thread safety for database connections
local_storage = threading.local()


def get_db_connection():
    """
    Establishes a thread-safe database connection.
    Creates the database and table if they don't exist.
    """
    if not hasattr(local_storage, "connection"):
        local_storage.connection = sqlite3.connect(
            "moderation.db", check_same_thread=False
        )
        local_storage.connection.row_factory = sqlite3.Row
    return local_storage.connection


def init_db():
    """
    Initializes the database and creates the 'warnings' table if it's missing.
    This function should be called once when the bot starts up.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                moderator_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        conn.commit()
        print("Database: 'warnings' table initialized successfully.")

    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        # The connection is kept open for the bot's lifecycle
        pass


# --- DATABASE FUNCTIONS ---


def add_warning(guild_id: int, user_id: int, moderator_id: int, reason: str):
    """
    Adds a warning for a user to the database.
    """
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, moderator_id, reason),
        )
        conn.commit()
        print(f"Database: Logged warning for user {user_id} in guild {guild_id}.")
    except sqlite3.Error as e:
        print(f"Database error on add_warning: {e}")


def get_warnings(guild_id: int, user_id: int) -> list:
    """
    Retrieves all warnings for a specific user in a guild.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM warnings WHERE guild_id = ? AND user_id = ? ORDER BY timestamp DESC",
            (guild_id, user_id),
        )
        warnings = cursor.fetchall()
        return [dict(row) for row in warnings]
    except sqlite3.Error as e:
        print(f"Database error on get_warnings: {e}")
        return []


def clear_warnings(guild_id: int, user_id: int) -> int:
    """
    Clears all warnings for a specific user in a guild.
    Returns the number of warnings removed.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM warnings WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error on clear_warnings: {e}")
        return 0
