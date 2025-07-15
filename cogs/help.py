import discord
from discord import app_commands
from discord.ext import commands


def is_admin_command(command: app_commands.Command) -> bool:
    for check in command.checks:
        if "is_admin" in check.__qualname__:
            return True
    return False


# --- The Dropdown View ---
class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=180)
        self.bot = bot
        self.add_item(self.create_dropdown())

    def create_dropdown(self) -> discord.ui.Select:
        options = [
            discord.SelectOption(
                label=cog_name, description=f"Commands from the {cog_name} category."
            )
            for cog_name in self.bot.cogs
            if cog_name != "Help"
        ]

        select = discord.ui.Select(
            placeholder="Select a category to see its commands...",
            options=options,
            custom_id="help_dropdown",
        )
        select.callback = self.dropdown_callback
        return select

    async def dropdown_callback(self, interaction: discord.Interaction):
        cog_name = interaction.data["values"][0]
        cog = self.bot.get_cog(cog_name)

        if not cog:
            await interaction.response.send_message(
                "This category could not be found.", ephemeral=True
            )
            return

        embed = self.create_help_embed(cog)

        await interaction.response.edit_message(embed=embed)

    def create_help_embed(self, cog: commands.Cog) -> discord.Embed:
        embed = discord.Embed(
            title=f"Help: {cog.qualified_name} Commands", color=discord.Color.blue()
        )

        commands_list = cog.get_app_commands()
        if not commands_list:
            embed.description = "No commands found in this category."
        else:
            for command in sorted(commands_list, key=lambda c: c.name):

                params = " ".join([f"<{p.name}>" for p in command.parameters])
                admin_marker = " 🔒" if is_admin_command(command) else ""

                embed.add_field(
                    name=f"`/{command.name} {params}`{admin_marker}",
                    value=f"_{command.description}_",
                    inline=False,
                )

        if "🔒" in embed.fields[0].name:
            embed.set_footer(text="🔒 This command is admin-only.")

        return embed


# --- The Help Cog ---
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="help", description="Shows a list of all available commands."
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help Menu",
            description="Welcome to the help menu! Please select a category from the dropdown below to see the available commands.",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="This menu will become inactive after 3 minutes.")

        view = HelpView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
