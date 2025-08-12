import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!',
                   intents=intents)  # prefix jest już niepotrzebny do slash

ticket_owners = {}


async def create_ticket(user: discord.Member):
    guild = user.guild
    category = discord.utils.get(guild.categories, name="Tickets")
    if category is None:
        category = await guild.create_category("Tickets")

    ticket_channel = await guild.create_text_channel(f"ticket-{user.name}",
                                                     category=category)

    # Permissions: user + staff roles
    await ticket_channel.set_permissions(user,
                                         read_messages=True,
                                         send_messages=True)

    for role in guild.roles:
        if "Owner" in role.name or "Mod" in role.name:
            await ticket_channel.set_permissions(role,
                                                 read_messages=True,
                                                 send_messages=True)

    await ticket_channel.set_permissions(guild.default_role,
                                         read_messages=False)

    embed = discord.Embed(
        title=f"Ticket for {user.name}",
        description=
        "Please wait for assistance. Our moderators will contact you soon.",
        color=discord.Color(int("1BBC9B", 16)))
    embed.set_footer(text="Ticket System - Discord Bot")
    embed.set_thumbnail(
        url=user.avatar.url if user.avatar else discord.Embed.Empty)

    message = await ticket_channel.send(embed=embed)
    await message.add_reaction("❌")

    ticket_owners[ticket_channel.id] = user.id


# Slash command to post the ticket opening message
@bot.tree.command(name="ticket",
                  description="Send a message to open tickets in a channel")
@app_commands.describe(channel="The channel to send the ticket message in")
async def ticket(interaction: discord.Interaction,
                 channel: discord.TextChannel):
    embed = discord.Embed(title="Open a Ticket",
                          description="React with 🎟️ to open a ticket!",
                          color=discord.Color(int("1BBC9B", 16)))
    embed.set_footer(text="Ticket System - Discord Bot")

    message = await channel.send(embed=embed)
    await message.add_reaction("🎟️")

    await interaction.response.send_message(
        f"Ticket message sent in {channel.mention}.", ephemeral=True)


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.emoji == "🎟️":
        await create_ticket(user)
        print(f"User {user.name} created a ticket!")

    elif reaction.emoji == "❌":
        channel = reaction.message.channel
        if channel.name.startswith("ticket-"):
            ticket_owner_id = ticket_owners.get(channel.id)

            if ticket_owner_id == user.id or any(role.name in ["Owner", "Mod"]
                                                 for role in user.roles):
                await channel.delete()
                print(f"Ticket {channel.name} was closed by {user.name}")
            else:
                await reaction.remove(user)
                print(
                    f"{user.name} does not have permission to close this ticket."
                )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready! Logged in as {bot.user}.")


TOKEN = 'ENTER TOKEN HERE'
bot.run(TOKEN)
