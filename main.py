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
        await interaction.response.send_message("A ticket is being made for you :wink:", ephemeral=True)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(CreateTicket())
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
