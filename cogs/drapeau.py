import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
from db_utils import increment_correct, increment_total
import json
from random import choice, sample

from time import sleep
import asyncio

with open("pays.json", "r") as file:
    pays = json.load(file)

CODE = {}
for cd, py in pays.items():
    CODE[py] = cd
    
def pays_aleatoires(n: int):
    """
    Retourne une liste de n pays aléatoires
    """
    return sample(list(pays.items()), n)

def drapeau(code: str):
    """
    Retourne l'image d'un drapeau sous la forme d'un object `File`
    """
    filename = f"drapeaux/{code.lower()}.png"
    file = open(filename, 'rb')
    return discord.File(file, filename="drapeau.png")

class Select(discord.ui.Select):
    def __init__(self, choix):
        self.answers = {}
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
        self.answers[user] = self.values[0]
        await interaction.response.defer()

class SelectView(discord.ui.View):
    def __init__(self, choix):
        super().__init__()
        self.add_item(Select(choix))

class Drapeau(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="drapeau", description="Fais deviner un unique drapeau")
    async def drapeau(self, interaction):
        choix = pays_aleatoires(15)
        correct = choice(choix)
        file = drapeau(correct[0])
        view = SelectView(choix)
        await interaction.response.send_message(
            ":thinking: Quel est le pays correspondant à ce drapeau ?",
            file = file,
            view = view,
        )

        response = await interaction.original_response()
        await asyncio.sleep(15)
        answers = view.children[0].answers
        message = ""

        for user, answer in answers.items():
            increment_total(user.id)
            if answer == correct[1]:
                message += ":white_check_mark: | "
                increment_correct(user.id)
            else:
                message += ":x: | "
            emote = f":flag_{CODE[answer].lower()}:"
            message += f"{user.mention} a répondu : {emote} {answer}\n"

        message += f":information_source: | La bonne réponse était {correct[1]}!"
        await response.edit(
            content = message,
            view = None,
        )

async def setup(bot):
    await bot.add_cog(Drapeau(bot), guilds = [guild])