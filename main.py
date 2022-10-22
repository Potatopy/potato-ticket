# Credits: faint#1337

import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('bot is on')

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        extension = file[:-3]

bot.run("Token")