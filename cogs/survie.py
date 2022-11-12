import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
from db_utils import increment_correct, increment_total, increment_streak, decrement_vies, donnee, set_donnee
from cogs.drapeau import pays_aleatoires, drapeau
import json
from random import choice, sample

from time import sleep
import asyncio

class Select(discord.ui.Select):
    def __init__(self, choix, correct, interaction):
        self.interaction = interaction
        self.correct = correct
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
        response = await self.interaction.original_response()
        id = interaction.user.id
        increment_total(id)

        if self.values[0] == self.correct[1]:
            increment_correct(id)
            increment_streak(id)
            message = ":white_check_mark: Correct !\n"

        else:
            message = f":x: Incorrect, la bonne réponse était {self.correct[1]} !\n"
            decrement_vies(id)

        vies = donnee(id, "VIES")
        streak = donnee(id, "STREAK")

        if vies <= 0:
            message += ":pensive: Vous êtes à court de vies !\n"
            x = "" if streak < 2 else "x"
            message += f":fire: Vous avez correctement trouvé {streak} drapeau{x} !\n"
            await response.edit(content = message, view = None)

        else:
            await response.edit(content = message, view = None)

            choix = pays_aleatoires(25)
            correct = choice(choix)
            file = drapeau(correct[0])
            view = SelectView(choix, correct, interaction)
            await interaction.response.send_message(
                f":thinking: Quel est le pays correspondant à ce drapeau ?\n" +
                f":fire: Streak : {streak}\n" +
                ":heart:" * vies,
                file = file,
                view = view,
                ephemeral = True,
            )

class SelectView(discord.ui.View):
    def __init__(self, choix, correct, interaction):
        super().__init__()
        self.add_item(Select(choix, correct, interaction))

class Survie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="survie", description="Fais deviner des drapeaux tant qu'il vous reste des vies")
    async def survie(self, interaction, vies:int=1):
        if vies > 10:
            await interaction.response.send_message(
                ":pensive: Le nombre de vies est limité à 10 au maximum !",
                ephemeral = True
            )
            return

        id = interaction.user.id

        set_donnee(id, "START", vies)
        set_donnee(id, "VIES", vies)
        set_donnee(id, "STREAK", 0)

        choix = pays_aleatoires(25)
        correct = choice(choix)
        file = drapeau(correct[0])
        view = SelectView(choix, correct, interaction)
        await interaction.response.send_message(
            ":thinking: Quel est le pays correspondant à ce drapeau ?",
            file = file,
            view = view,
            ephemeral = True,
        )

    @app_commands.command(name="continuer", description="Reprend une survie en cours de route")
    async def continuer(self, interaction):

        choix = pays_aleatoires(25)
        correct = choice(choix)
        file = drapeau(correct[0])
        view = SelectView(choix, correct, interaction)
        await interaction.response.send_message(
            ":thinking: Quel est le pays correspondant à ce drapeau ?",
            file = file,
            view = view,
            ephemeral = True,
        )

async def setup(bot):
    await bot.add_cog(Survie(bot), guilds = [guild])