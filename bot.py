# Credits zach.#0001

import nextcord
from nextcord.ext import commands
import os
import asyncio
import aiosqlite
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

class AddUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Add user to ticket",
            timeout=300,
        )
        self.channel = channel

        self.user = nextcord.ui.TextInput(
            label="User ID",
            min_length=2,
            max_length=35,
            required=True,
            placeholder="User ID (Must be INT)"
        )
        self.add_item(self.user)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send(f"This user does not exist, please make sure this ID is correct and/or in this guild!")
        overwrite = nextcord.PermissionOverwrite()
        overwrite.read_messages = True
        await self.channel.set_permissions(user, overwrite=overwrite)
        await interaction.send(f"{user.mention} has been added to the ticket!")

class RemoveUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Remove user to ticket",
            timeout=300,
        )
        self.channel = channel

        self.user = nextcord.ui.TextInput(
            label="User ID",
            min_length=2,
            max_length=35,
            required=True,
            placeholder="User ID (Must be INT)"
        )
        self.add_item(self.user)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send(f"This user does not exist, please make sure this ID is correct and/or in this guild!")
        overwrite = nextcord.PermissionOverwrite()
        overwrite.read_messages = False
        await self.channel.set_permissions(user, overwrite=overwrite)
        await interaction.send(f"{user.mention} has been removed from the ticket!")


class CreateTicket(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(
        label = "Create Ticket", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket:blurple"
    )
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.response.send_message("A ticket is being made for you :wink:", ephemeral=True)

        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT role FROM role WHERE guild = ?", (interaction.guild.id))
            role = await cursor.fetchone()
            if role:
                overwrites = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, view_channel=False),
                    interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                    interaction.user: nextcord.PermissionOverwrite(read_messages = True, view_channel = True),
                    interaction.guild.get_role(role[0]): nextcord.PermissionOverwrite(read_messages=True)
                }
            else:
                overwrites = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, view_channel=False),
                    interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                    interaction.user: nextcord.PermissionOverwrite(read_messages = True, view_channel = True),
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
        label = "Add User", style=nextcord.ButtonStyle.green, custom_id="ticket_settings:green"
    )
    async def add_user(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(AddUser(interaction.channel))

    @nextcord.ui.button(
        label = "Remove User", style=nextcord.ButtonStyle.gray, custom_id="ticket_settings:gray"
    )
    async def remove_user(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RemoveUser(interaction.channel))
        
    @nextcord.ui.button(
        label = "Close Ticket", style=nextcord.ButtonStyle.red, custom_id="ticket_settings:red"
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        messages = await interaction.channel.history(limit=None, oldest_first=True).flatten()
        contents = [message.content for message in messages]
        final = ""
        for msg in contents:
            msg = msg + "\n"
            final = final + msg
        with open('transcript.txt', 'w') as f:
            f.write(final)
        await interaction.response.send_message("Your Ticket is being closed1.", ephemeral=True)
        await interaction.channel.delete()
        await interaction.user.send(f"Ticket closed by {interaction.channel.mention}", file=nextcord.File(r'transcript.txt'))
        os.remove("transcript.txt")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(CreateTicket(self))
            self.add_view(TicketSettings())
            self.persistent_views_added = True
            print("Persistent views added")
            self.db = await aiosqlite.connect("tickets.db")
            async with self.db.cursor() as cursor:
                await cursor.execute(f"CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild INTEGER)")
            print("Database Ready!")

            print(f"Logged in as {self.user}")


bot = Bot(command_prefix='-', intents=nextcord.Intents.all())

@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup_tickets(ctx: commands.Context):
    embed = nextcord.Embed(title="Need Support?", description="For Support Click the `Create Ticket` Button for support! And we'll respond within less than 24 hours.")
    await ctx.send(embed=embed, view=CreateTicket(bot))

@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup_role(ctx: commands.Context, role: nextcord.Role):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT role FROM roles WHERE guild = ?", (ctx.guild.id,))
        role2 = await cursor.fetchone()
        if role2:
            await cursor.execute("UPDATE roles SET role = ? WHERE guild = ?", (role.id, ctx.guild.id,))
            await ctx.send(f"Bot Auto-Assigned role updated!")
        else:
            await cursor.execute("INSERT INTO roles VALUES (?, ?)", (role.id, ctx.guild.id))
            await ctx.send(f"Bot Auto-Assigned role added!")
    await bot.db.commit()

bot.run(TOKEN)