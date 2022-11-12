import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
from db_utils import donnees

class Scoreboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        s = "" if fmt < 2 else "s"
        await ctx.send(f"{len(fmt)} commande{s} synchronisée{s}.")
    
    @app_commands.command(name="scoreboard", description="Révèle le tableau des scores du serveur")
    async def scoreboard(self, interaction):
        scoreboard = []
        for row in donnees():
            id = row['id']
            total = row['total']
            correct = row['correct']
            survie = row['survie']
            aventure = row['aventure']
            precision = f"{100 * correct / total:.2f}%"
            score = (1 + correct) / (1 + total)
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
    await bot.add_cog(Scoreboard(bot), guilds = [guild])