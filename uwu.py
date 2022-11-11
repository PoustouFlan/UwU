import discord
from discord.ui import Select, View
from discord import SelectOption
from discord.ext import commands
from bot_utils import TOKEN, GUILD_ID
from drapeau import *

import logging
from random import choice
#from discord.client import _ColourFormatter
from time import sleep

guild = discord.Object(id=GUILD_ID)

log = logging.getLogger("UwU")
log.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
#stream.setFormatter(_ColourFormatter())
log.addHandler(stream)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix = "UwU ",
    help_command = None,
    intents = intents
)

@bot.event
async def on_ready():
    log.info(f"Connecté en tant que {bot.user}")
    await bot.tree.sync(guild=guild)


@bot.tree.command(name="drapeau", description="Fais deviner un unique drapeau", guild = guild)
async def drapeau(interaction):
    choix = drapeaux_aleatoires(2)
    correct = choice(choix)
    select = Select(
        options = [
            SelectOption(label=pays) 
            for drapeau, pays in choix
        ],
        placeholder = "Sélectionne le pays correspondant au drapeau",
    )
    view = View()
    view.add_item(select)
    message = correct[0]
    await interaction.response.send_message(message, view = view)

bot.run(TOKEN)