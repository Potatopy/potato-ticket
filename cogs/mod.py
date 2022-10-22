# Credits: faint#1337

import discord
from discord.ext import commands
from datetime import datetime

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()
async def on_message(self, message):
    if "-close" in message.content:
        pass
    else:
        if str(message.channel.type) == "private":
            if message.author == self.bot.user:
                return
        else:
            user = message.guild.fetch_member(int(message.channel.name))
            emb = discord.Embed(
                title="Message from mods",
                description={message.content},
                timestamp=datetime.utcnow(),
                color=discord.Color.random()
            )
            await user.send(embed=emb)

        @commands.command()
        async def close(self, ctx):
            user=ctx.guild.fetch_member(int(ctx.channel.name))
            await ctx.send("Ticket has been closed by mods")
            await ctx.channel.delete()