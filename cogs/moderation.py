import asyncio
from datetime import datetime, timezone

import discord
from discord import Member, app_commands
from discord.ext import commands

from utils import checks, database, logger
from utils.decorators import admin_only


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- KICK COMMAND (ANONYMOUS) ---
    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @app_commands.describe(member="The member to kick", reason="The reason for kicking")
    @admin_only()
    async def kick(self, interaction: discord.Interaction, member: Member, reason: str):
        await interaction.response.defer(ephemeral=True)
        if error := checks.is_target_valid(interaction, member):
            return await interaction.edit_original_response(content=error)

        reason = reason or "No reason provided."
        try:
            logger.log_action(str(interaction.user.id), "kick", str(member.id), reason)
            await member.kick(reason=reason)

            embed = discord.Embed(
                title="Member Kicked",
                description=f"**{member.mention} has been kicked.**",
                color=discord.Color.orange(),
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            await interaction.channel.send(embed=embed)

            await interaction.edit_original_response(
                content=f"✅ Successfully kicked {member.display_name}."
            )
            await asyncio.sleep(5)
            await interaction.delete_original_response()
        except Exception as e:
            await interaction.edit_original_response(
                content=f"❌ An error occurred: {e}"
            )

    # --- BAN COMMAND (ANONYMOUS) ---
    @app_commands.command(name="ban", description="Bans a member from the server.")
    @app_commands.describe(member="The member to ban", reason="The reason for banning")
    @admin_only()
    async def ban(self, interaction: discord.Interaction, member: Member, reason: str):
        await interaction.response.defer(ephemeral=True)
        if error := checks.is_target_valid(interaction, member):
            return await interaction.edit_original_response(content=error)

        reason = reason or "No reason provided."
        try:
            logger.log_action(str(interaction.user.id), "ban", str(member.id), reason)
            await member.ban(reason=reason)

            embed = discord.Embed(
                title="Member Banned",
                description=f"**{member.mention} has been banned.**",
                color=discord.Color.red(),
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            await interaction.channel.send(embed=embed)

            await interaction.edit_original_response(
                content=f"✅ Successfully banned {member.display_name}."
            )
            await asyncio.sleep(5)
            await interaction.delete_original_response()
        except Exception as e:
            await interaction.edit_original_response(
                content=f"❌ An error occurred: {e}"
            )

    # --- UNBAN COMMAND (ANONYMOUS) ---
    @app_commands.command(
        name="unban", description="Revokes a user's ban from the server."
    )
    @app_commands.describe(
        user_id="The ID of the user to unban", reason="The reason for unbanning"
    )
    @admin_only()
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str):
        await interaction.response.defer(ephemeral=True)
        reason = reason or "No reason provided."
        try:
            user = await self.bot.fetch_user(int(user_id))
            logger.log_action(str(interaction.user.id), "unban", str(user.id), reason)
            await interaction.guild.unban(user, reason=reason)

            embed = discord.Embed(
                title="User Unbanned",
                description=f"**{user.mention} (`{user.name}`) has been unbanned.**",
                color=discord.Color.green(),
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            await interaction.channel.send(embed=embed)

            await interaction.edit_original_response(
                content=f"✅ Successfully unbanned {user.name}."
            )
            await asyncio.sleep(5)
            await interaction.delete_original_response()
        except (ValueError, discord.NotFound):
            await interaction.edit_original_response(
                content=f"User with ID `{user_id}` not found or is not banned."
            )
        except Exception as e:
            await interaction.edit_original_response(
                content=f"❌ An error occurred: {e}"
            )

    # --- WARN COMMAND (ANONYMOUS) ---
    @app_commands.command(
        name="warn", description="Warns a member and logs it to the database."
    )
    @app_commands.describe(
        member="The member to warn", reason="The reason for the warning"
    )
    @admin_only()
    async def warn(self, interaction: discord.Interaction, member: Member, reason: str):
        await interaction.response.defer(ephemeral=True)
        if member.id == interaction.user.id:
            return await interaction.edit_original_response(
                content="❌ You cannot warn yourself."
            )

        database.add_warning(
            interaction.guild.id, member.id, interaction.user.id, reason
        )
        logger.log_action(str(interaction.user.id), "warn", str(member.id), reason)

        embed = discord.Embed(
            title="Member Warned",
            description=f"**{member.mention} has been warned.**",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        try:
            await interaction.channel.send(embed=embed)
        except discord.Forbidden:
            return await interaction.edit_original_response(
                content="❌ I do not have permission to send messages in this channel."
            )
        except Exception as e:
            print(f"Error sending warn embed: {e}")
            return await interaction.edit_original_response(
                content="❌ An unexpected error occurred while posting the public warning."
            )

        await interaction.edit_original_response(
            content=f"✅ Successfully warned {member.display_name}."
        )
        await asyncio.sleep(5)
        await interaction.delete_original_response()

    # --- PRIVATE WARNINGS COMMAND (UNCHANGED) ---
    @app_commands.command(
        name="warnings", description="Check a member's warning history privately."
    )
    @app_commands.describe(member="The member whose warnings you want to see")
    @admin_only()
    async def warnings(self, interaction: discord.Interaction, member: Member):
        user_warnings = database.get_warnings(interaction.guild.id, member.id)
        embed = discord.Embed(
            title=f"Warning History for {member.display_name}",
            description=f"**Total Warnings: {len(user_warnings)}**",
            color=discord.Color.orange(),
        )
        if not user_warnings:
            embed.description += "\n\nThis user has a clean record."
        else:
            for i, warning in enumerate(user_warnings[:10]):
                try:
                    moderator = interaction.guild.get_member(warning["moderator_id"])
                    mod_display = (
                        moderator.display_name if moderator else "Unknown Moderator"
                    )
                    naive_dt = datetime.strptime(
                        warning["timestamp"], "%Y-%m-%d %H:%M:%S"
                    )
                    aware_dt = naive_dt.replace(tzinfo=timezone.utc)
                    timestamp_str = f"<t:{int(aware_dt.timestamp())}:R>"
                    embed.add_field(
                        name=f"Warning #{i+1} (by {mod_display})",
                        value=f"**Reason:** `{warning['reason']}`\n**When:** {timestamp_str}",
                        inline=False,
                    )
                except Exception as e:
                    print(f"Could not parse warning #{i+1} for user {member.id}: {e}")
                    continue
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # --- CLEARWARNINGS COMMAND (ANONYMOUS) ---
    @app_commands.command(
        name="clearwarnings", description="Clears all warnings for a member."
    )
    @app_commands.describe(member="The member whose warnings will be cleared")
    @admin_only()
    async def clearwarnings(self, interaction: discord.Interaction, member: Member):
        await interaction.response.defer(ephemeral=True)
        cleared_count = database.clear_warnings(interaction.guild.id, member.id)
        if cleared_count == 0:
            await interaction.edit_original_response(
                content=f"ℹ️ {member.mention} had no warnings to clear."
            )
            await asyncio.sleep(5)
            return await interaction.delete_original_response()

        logger.log_action(
            str(interaction.user.id),
            "clearwarnings",
            str(member.id),
            f"Cleared {cleared_count} warnings.",
        )
        embed = discord.Embed(
            title="Warnings Cleared",
            description=f"✅ All **{cleared_count}** warnings for {member.mention} have been cleared.",
            color=discord.Color.blue(),
        )
        await interaction.channel.send(embed=embed)

        await interaction.edit_original_response(
            content=f"✅ Successfully cleared warnings for {member.display_name}."
        )
        await asyncio.sleep(5)
        await interaction.delete_original_response()


async def setup(bot):
    await bot.add_cog(Moderation(bot))
