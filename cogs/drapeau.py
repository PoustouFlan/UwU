import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
import json
from random import choice, sample

from time import sleep

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
    def __init__(self, interaction, choix, correct):
        self.correct = correct
        self.interaction = interaction
        pays = sorted(element[1] for element in choix)
        options = [
            discord.SelectOption(label=nom) for nom in pays
        ]
        placeholder = "Sélectionne le pays correspondant au drapeau"
        super().__init__(
            placeholder = placeholder,
            max_values = 1,
            min_values = 1,
            options = options
        )
    
    async def callback(self, interaction):
        user = interaction.user
        response = await self.interaction.original_response()
        message = f"{user.mention} a répondu {self.values[0]}:\n"
        if self.values[0] == self.correct[1]:
            message += ":white_check_mark: Bonne réponse !"
        else:
            message += f":x: Mauvaise réponse ! Il s'agissait de {self.correct[1]}."
        await response.edit(content = message, view = None)


class SelectView(discord.ui.View):
    def __init__(self, interaction, choix, correct):
        super().__init__()
        self.add_item(Select(interaction, choix, correct))

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
        view = SelectView(interaction, choix, correct)
        await interaction.response.send_message(
            "Préparez vous, drapeau dans 3 secondes !",
        )
        response = await interaction.original_response()
        sleep(3)
        await response.edit(
            content = "Quel est le pays correspondant à ce drapeau ?",
            attachments = [file],
            view = view,
        )

async def setup(bot):
    await bot.add_cog(Drapeau(bot), guilds = [guild])