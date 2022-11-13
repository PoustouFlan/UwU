import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
from cogs.drapeau import drapeau, pays
from db_utils import increment_correct, increment_total
import json
from random import choice, sample

from time import sleep
import asyncio

with open("donnees/capitales.json", "r") as file:
    capitales = json.load(file)
    
def capitales_aleatoires(n: int):
    """
    Retourne une liste de n pays aléatoires
    """
    return sample(list(capitales.items()), n)

class Select(discord.ui.Select):
    def __init__(self, choix):
        self.answers = {}
        capitales = sorted(element[1] for element in choix)
        options = [
            discord.SelectOption(label=nom) for nom in capitales
        ]
        placeholder = "Sélectionne la capitale correspondant au pays"
        super().__init__(
            placeholder = placeholder,
            max_values = 1,
            min_values = 1,
            options = options
        )
    
    async def callback(self, interaction):
        user = interaction.user
        self.answers[user] = self.values[0]
        await interaction.response.defer()

class SelectView(discord.ui.View):
    def __init__(self, choix):
        super().__init__()
        self.add_item(Select(choix))

class Capitale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="capitale", description="Fais deviner une unique capitale")
    async def capitale(self, interaction):
        choix = capitales_aleatoires(15)
        correct = choice(choix)
        pays_correct = pays[correct[0]]
        file = drapeau(correct[0])
        view = SelectView(choix)
        await interaction.response.send_message(
            f":thinking: Quel est la capitale de ce pays ? ({pays_correct})",
            file = file,
            view = view,
        )

        response = await interaction.original_response()
        await asyncio.sleep(15)
        answers = view.children[0].answers
        message = ""

        for user, answer in answers.items():
            increment_total(user.id, "CAPITALES")
            if answer == correct[1]:
                message += ":white_check_mark: | "
                increment_correct(user.id, "CAPITALES")
            else:
                message += ":x: | "
            message += f"{user.mention} a répondu : {answer}\n"

        message += f":information_source: | La bonne réponse était {correct[1]}!"
        await response.edit(
            content = message,
            view = None,
        )

async def setup(bot):
    await bot.add_cog(Capitale(bot), guilds = [guild])