import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
import json
from random import choice, sample

with open("pays.json", "r") as file:
    pays = json.load(file)
    
def pays_aleatoires(n: int):
    """
    Retourne une liste de n pays aléatoires
    """
    return sample(list(pays.items()), n)

def drapeau(code: str):
    filename = f"drapeaux/{code.lower()}.png"
    file = open(filename, 'rb')
    return discord.File(file, filename="drapeau.png")

class Select(discord.ui.Select):
    def __init__(self, choix):
        pays = sorted(element[1] for element in choix)
        options = [
            discord.SelectOption(label=nom) for nom in pays
        ]
        placeholder = "Sélectionne le pays correspondant au drapeau"
        super().__init__(
            placeholder=placeholder,
            options=options
        )
    
    async def callback(self, interaction):
        pass

class SelectView(discord.ui.View):
    def __init__(self, choix):
        super().__init__()
        self.add_item(Select(choix))

class Drapeau(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        s = "" if fmt < 2 else "s"
        await ctx.send(f"{len(fmt)} commande{s} synchronisée{s}.")
    
    @app_commands.command(name="drapeau", description="Fais deviner un unique drapeau")
    async def drapeau(self, interaction):
        choix = pays_aleatoires(15)
        correct = choice(choix)
        file = drapeau(correct[0])
        await interaction.response.send_message("", file = file, view = SelectView(choix))

async def setup(bot):
    await bot.add_cog(Drapeau(bot), guilds = [guild])
# @bot.tree.command(name="drapeau", description="Fais deviner un unique drapeau", guild = guild)
# async def drapeau(interaction):
#     choix = drapeaux_aleatoires(2)
#     correct = choice(choix)
#     select = Select(
#     )
#     view = View()
#     view.add_item(select)
#     message = correct[0]
#     await interaction.response.send_message(message, view = view)
