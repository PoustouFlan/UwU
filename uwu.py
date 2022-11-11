import discord
from discord.ext import commands
from bot_utils import TOKEN, GUILD_ID
from drapeau import *

import logging
from discord.client import _ColourFormatter
from discord.ext import commands
from discord.utils import get
from discord import app_commands
from time import sleep

guild = discord.Object(id=GUILD_ID)

log = logging.getLogger("UwU")
log.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setFormatter(_ColourFormatter())
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
    drapeau, pays = drapeau_aleatoire()
    await interaction.channel.send(drapeau)

bot.run(TOKEN)