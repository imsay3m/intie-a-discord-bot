# Discord Moderator Bot

![Bot Showcase](PLACEHOLDER_FOR_A_GENERAL_SHOWCASE_IMAGE.png)

A powerful, modular, and anonymous Discord server moderation bot built with Python and the `discord.py` library. This bot is designed to help moderation teams manage their community efficiently while maintaining a unified and official presence. All public-facing moderation actions are anonymous, logged internally for accountability, and presented in clean, professional embeds.

---

## ✨ Features

This bot provides a complete suite of tools for professional server management.

### 🕵️ Anonymous Moderation & Logging

All moderation actions are designed to be anonymous to the public, appearing as official server actions rather than actions from an individual admin.

-   **Invisible Actions**: Commands do not trigger the public "User used /command" message.
-   **Clean Embeds**: Public notifications are sent as clean, anonymous embeds without moderator names or timestamps.
-   **Internal Accountability**: Every action (`kick`, `ban`, `warn`, `say`, etc.) is logged in a private `moderation_actions.log` file with the responsible moderator's ID, the target's ID, and a timestamp.

_Screenshot placeholder for an anonymous kick/ban message_
`![Anonymous Kick](<PLACEHOLDER_FOR_ANONYMOUS_KICK.png>)`

### 🛡️ Core Moderation Commands

A full suite of essential tools for moderators.

-   `/kick <member> [reason]`: Kicks a member from the server.
-   `/ban <member> [reason]`: Bans a member from the server.
-   `/unban <user_id> [reason]`: Unbans a user using their ID.
-   `/warn <member> <reason>`: Issues a silent warning to a member, logging it to the database and sending a private confirmation to the admin.

### ✍️ Content & Messaging Tools

Control the flow of information in your server with powerful messaging commands.

-   `/announce <title> <description> [color]`: Broadcasts a beautiful, custom-titled, and color-coded anonymous embed. Supports newlines with `\n`.
-   `/say <message> [color]`: Sends a simple anonymous embed with a custom message and color. Perfect for quick, official statements.

_Screenshot placeholder for a custom announce message_
`![Custom Announce](<PLACEHOLDER_FOR_ANNOUNCE.png>)`

### 🗄️ Persistent Warning System

A robust warning system powered by a local SQLite database.

-   **Persistent Storage**: Warnings are saved in a `moderation.db` file and persist through bot restarts.
-   `/warnings <member>`: **(Admin-only)** Privately view the detailed warning history of a member, including who warned them and when.
-   `/history <member>`: **(Admin-only)** Publicly post a user's warning history to the channel, which automatically deletes after 1 minute for transparency.
-   `/clearwarnings <member>`: Permanently remove all warnings for a specific member.

_Screenshot placeholder for the /history command_
`![History Command](<PLACEHOLDER_FOR_HISTORY.png>)`

### 헬 Dynamic Help & Information System

User-friendly commands to help server members understand the bot and the community.

-   **/help**: An interactive, MEE6-style help menu with a dropdown to browse commands by category (Moderation, Messaging, etc.). It dynamically lists all commands, their parameters, and marks admin-only commands with a lock icon 🔒.
-   **/info <question>**: An interactive FAQ command with autocomplete. Users can select a question from a list, and the bot will provide a clean, embedded answer. The Q&A list can be easily updated in the `faq.json` file without any code changes.

_Screenshot placeholder for the /help command_
`![Help Command](<PLACEHOLDER_FOR_HELP.png>)`

---

## ⚙️ Technical Design

This bot is built with scalability and best practices in mind.

-   **Modular Cogs**: Commands are neatly organized into cogs (`moderation.py`, `messaging.py`, etc.), making the project easy to extend.
-   **Utility-Driven**: Core logic for permissions, database interactions, embed creation, and response handling is centralized in the `utils/` directory.
-   **Secure**: Uses a `.env` file to keep sensitive information like the bot token out of the codebase.
-   **Robust Error Handling**: Gracefully handles permissions errors and prevents commands from being used in DMs.
-   **Modern `discord.py`**: Utilizes modern features like `setup_hook` for reliable startup, `app_commands` for slash commands, and `discord.ui.View` for interactive components.

---

## 🚀 Getting Started

Ready to set up the bot? All detailed instructions are available on our project **[Wiki](https://github.com/imsay3m/intie-a-discord-bot/wiki)**.

Follow these steps in order for a successful setup:

1.  **[Discord Application Setup](https://github.com/imsay3m/intie-a-discord-bot/wiki/Discord-Setup)**: First, create your bot on the Discord Developer Portal to get your necessary Token and IDs.
2.  **[Cloning the Repository](https://github.com/imsay3m/intie-a-discord-bot/wiki#step-2-get-the-code-by-cloning-the-repository)**: Download the bot's code to your machine.
3.  **Choose Your Hosting Method**:
    -   **[Running the Bot Locally](https://github.com/imsay3m/intie-a-discord-bot/wiki/Running-the-Bot-Locally)** (Recommended for development or 24/7 hosting)
    -   **[Running the Bot on Google Colab](https://github.com/imsay3m/intie-a-discord-bot/wiki/Running-the-Bot-on-Google-Colab)** (Easy for quick testing)
4.  **[Customizing FAQs](<https://github.com/imsay3m/intie-a-discord-bot/wiki/Customizing-the-FAQ-(-info-Command)>)**: How to easily update the answers for the `/info` command.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/imsay3m/intie-a-discord-bot/issues).

---
