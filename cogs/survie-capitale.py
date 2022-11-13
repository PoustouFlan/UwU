import discord
from discord.ext import commands
from discord import app_commands

from bot_utils import guild
from db_utils import increment_correct, increment_total, increment_streak, decrement_vies, donnee, set_donnee
from cogs.drapeau import drapeau, pays
from cogs.capitale import capitales_aleatoires
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
        placeholder = "Sélectionne la capitale correspondant au pays"
        super().__init__(
            placeholder = placeholder,
            max_values = 1,
            min_values = 1,
            options = options
        )
    
    async def callback(self, interaction):
        response = await self.interaction.original_response()
        id = interaction.user.id
        increment_total(id, "CAPITALES")

        if self.values[0] == self.correct[1]:
            increment_correct(id, "CAPITALES")
            increment_streak(id, "CAPITALES")
            message = ":white_check_mark: Correct !\n"

        else:
            message = f":x: Incorrect, la bonne réponse était {self.correct[1]} !\n"
            decrement_vies(id, "CAPITALES")

        vies = donnee(id, "CAPITALES", "VIES")
        streak = donnee(id, "CAPITALES", "STREAK")

        if vies <= 0:
            message += ":pensive: Vous êtes à court de vies !\n"
            s = "" if streak < 2 else "s"
            message += f":fire: Vous avez correctement trouvé {streak} capitale{s} !\n"
            await response.edit(content = message, view = None)

        else:
            await response.edit(content = message, view = None)

            choix = capitales_aleatoires(25)
            correct = choice(choix)
            pays_correct = pays[correct[0]]
            file = drapeau(correct[0])
            view = SelectView(choix, correct, interaction)
            await interaction.response.send_message(
                f":thinking: Quel est la capitale de ce pays ? ({pays_correct})\n" +
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

class SurvieCapitale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="survie-capitale", description="Fais deviner des capitales tant qu'il vous reste des vies")
    async def survie_capitale(self, interaction, vies:int=1):
        if vies > 10:
            await interaction.response.send_message(
                ":pensive: Le nombre de vies est limité à 10 au maximum !",
                ephemeral = True
            )
            return

        try:
            id = interaction.user.id

            set_donnee(id, "CAPITALES", "START", vies)
            set_donnee(id, "CAPITALES", "VIES", vies)
            set_donnee(id, "CAPITALES", "STREAK", 0)

            choix = capitales_aleatoires(25)
            correct = choice(choix)
            pays_correct = pays[correct[0]]
            file = drapeau(correct[0])
            view = SelectView(choix, correct, interaction)
            await interaction.response.send_message(
                f":thinking: Quel est la capitale de ce pays ? ({pays_correct})",
                file = file,
                view = view,
                ephemeral = True,
            )
        except Exception as e:
            print(e)

    @app_commands.command(name="continuer-capitale", description="Reprend une survie-capitale en cours de route")
    async def continuer_capitale(self, interaction):
        id = interaction.user.id
        vies = donnee(id, "CAPITALES", "VIES", None, 1)
        if vies <= 0:
            await interaction.response.send_message(
                ":x: Vous n'avez pas de survie-capitale en cours !",
                ephemeral = True
            )
            return

        choix = capitales_aleatoires(25)
        correct = choice(choix)
        pays_correct = pays[correct[0]]
        file = drapeau(correct[0])
        view = SelectView(choix, correct, interaction)
        await interaction.response.send_message(
            f":thinking: Quel est la capitale de ce pays ? ({pays_correct})",
            file = file,
            view = view,
            ephemeral = True,
        )

async def setup(bot):
    await bot.add_cog(SurvieCapitale(bot), guilds = [guild])