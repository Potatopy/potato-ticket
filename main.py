# Credits faint#1337

import nextcord
from nextcord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label = "Create Ticket", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket:blurple"
    )
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.response.send_message("A ticket is being made for you :wink:", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, view_channel=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            interaction.user: nextcord.PermissionOverwrite(read_messages = True, view_channel = True),
            interaction.guild.get_role(1034215386960380005): nextcord.PermissionOverwrite(read_messages=True) # In this line replace the numbers with the id with mod perms (a.k.a manage server perm)
        }
        channel = await interaction.guild.create_text_channel(f"{interaction.user.name}-ticket",
        overwrites=overwrites)
        await msg.edit(f"Your ticket has been made! {channel.mention}")
        embed = nextcord.Embed(title=f"Ticket Created", description=f"{interaction.user.mention} created a ticket! If you want to change something, click one of the buttons to change them.")
        await channel.send(embed=embed, view=TicketSettings())

class TicketSettings(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @nextcord.ui.button(
        label = "Close Ticket", style=nextcord.ButtonStyle.red, custom_id="ticket_settings:red"
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Your Ticket is being closed1.", ephemeral=True)
        await interaction.channel.delete()
        await interaction.user.send(f"Ticket closed by {interaction.channel.mention}")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(CreateTicket())
            self.add_view(TicketSettings())
            self.persistent_views_added = True
            print("Persistent views added")
            print(f"Logged in as {self.user}")


bot = Bot(command_prefix='-', intents=nextcord.Intents.all())

@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup_tickets(ctx: commands.Context):
    embed = nextcord.Embed(title="Need Support?", description="For Support Click the `Create Ticket` Button for support! And we'll respond within less than 24 hours.")
    await ctx.send(embed=embed, view=CreateTicket())

bot.run(TOKEN)
