# Credits: faint#1337

import discord
from discord.ext import commands
from datetime import datetime

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()
async def on_message(self, message):
    if str(message.channel.type) == "private":
        if message.author == self.bot.user:
            return
    else:
        guild = self.bot.get_guild(961765341451665498)
        channels = guild.fetch_channels()
        channel = discord.utils.get(channels, name=str(message.author.id))

        if channel is None:
            category = discord.utils.get(guild.catgeotries, name="Tickets")
            channel = guild.create_text_channel((message.author.id), category=category)

            await message.author.send("Ticket has been created!")
            em = discord.Embed(
                title=f"{message.author.name}#{message.author.discriminator} created a ticket",
                description={message.content},
                timestamp=datetime.utcnow(),
                color=discord.Color.blurple()
            )
            await channel.send(embed=em)

        else:
            em = discord.Embed(
                title=f"{message.author.name}#{message.author.discriminator}",
                description={message.content},
                timestamp=datetime.utcnow(),
                color=discord.Color.blurple()
            )
            await channel.send(embed=em)

def setup(bot):
    bot.add_cog(command(bot))