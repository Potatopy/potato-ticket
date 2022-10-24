from nextcord.ext import commands
import nextcord
import asyncio
from config.json import TOKEN

bot = commands.Bot(command_prefix='-', intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    print('bot is ready!')

bot.run(TOKEN)