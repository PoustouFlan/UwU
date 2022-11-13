import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
from db_utils import donnees_capitales

class ScoreboardCapitale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="scoreboard-capitale", description="Révèle le tableau des scores des capitales du serveur")
    async def scoreboard_capitale(self, interaction):
        scoreboard = []
        for row in donnees_capitales():
            id = row['id']
            total = row['total']
            if total == 0:
                continue
            correct = row['correct']
            survie = row['survie']
            aventure = row['aventure']
            precision = f"{100 * correct / total:.2f}%"
            score = (1 + correct) / (2 + total)
            scoreboard.append(
                (score, f"<@!{id}>", precision, str(total), f":fire:{survie}", f":fire:{aventure}"))
        scoreboard.sort(reverse = True)

        embed = discord.Embed()
        embed.add_field(
            name = "Utilisateur",
            value = "\n".join(map(lambda row: row[1], scoreboard))
        )
        embed.add_field(
            name = "Précision",
            value = "\n".join(map(lambda row: row[2], scoreboard))
        )
        embed.add_field(
            name = "Total",
            value = "\n".join(map(lambda row: row[3], scoreboard))
        )

        embed.add_field(
            name = "Utilisateur",
            value = "\n".join(map(lambda row: row[1], scoreboard))
        )
        embed.add_field(
            name = "Survie",
            value = "\n".join(map(lambda row: row[4], scoreboard))
        )
        embed.add_field(
            name = "Aventure",
            value = "\n".join(map(lambda row: row[5], scoreboard))
        )
        await interaction.response.send_message(
            "Scoreboard :",
            embed = embed,
            ephemeral = True,
        )

async def setup(bot):
    await bot.add_cog(ScoreboardCapitale(bot), guilds = [guild])