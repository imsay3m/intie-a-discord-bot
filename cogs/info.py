import json

import discord
from discord import app_commands
from discord.ext import commands


# --- FAQ Loading ---
def load_faqs():
    try:
        with open("faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ WARNING: faq.json not found. The Info cog will not have questions.")
        return []
    except json.JSONDecodeError:
        print(
            "⚠️ WARNING: faq.json is not formatted correctly. The Info cog will not have questions."
        )
        return []


# The Info cog, providing information via a slash command.
class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.faqs = load_faqs()
        self.faq_questions = [item["question"] for item in self.faqs]
        self.faq_lookup = {
            item["question"].lower(): item["answer"] for item in self.faqs
        }
        print(f"✅ Loaded {len(self.faq_lookup)} info entries.")

    async def question_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=question, value=question)
            for question in self.faq_questions
            if current.lower() in question.lower()
        ][:25]

    @app_commands.command(
        name="info", description="Get information about frequently asked questions."
    )
    @app_commands.autocomplete(question=question_autocomplete)
    @app_commands.describe(question="Select a question from the list to get an answer.")
    async def info(self, interaction: discord.Interaction, question: str):
        answer_text = self.faq_lookup.get(question.lower())

        if answer_text:
            embed = discord.Embed(
                title=f"❓ {question}",
                description=answer_text,
                color=discord.Color.blue(),
            )

            # Respond publicly by default so others can see the answer.
            # Change ephemeral to True if you want it to be private.
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            await interaction.response.send_message(
                "I couldn't find an answer for that specific question. Please select one from the list.",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(Info(bot))
