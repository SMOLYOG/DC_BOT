import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

ticket_owners = {}


async def create_ticket(user):
    guild = user.guild
    category = discord.utils.get(guild.categories, name="Tickets")
    if category is None:
        category = await guild.create_category("Tickets")

    ticket_channel = await guild.create_text_channel(f"ticket-{user.name}",
                                                     category=category)

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
    embed.set_thumbnail(url=user.avatar.url)

    message = await ticket_channel.send(embed=embed)

    await message.add_reaction("❌")

    ticket_owners[ticket_channel.id] = user.id


@bot.command(name="ticket")
async def ticket(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="Open a Ticket",
            description="Click the 🎟️ reaction to open a ticket!",
            color=discord.Color(int("1BBC9B", 16)))  
        embed.set_footer(text="Ticket System - Discord Bot")

        message = await channel.send(embed=embed)
        await message.add_reaction("🎟️")
    else:
        await ctx.send("Channel with the provided ID not found!")


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.emoji == "🎟️":
        await create_ticket(user)
        print(f"User {user.name} created a ticket!")

    if reaction.emoji == "❌":
        if reaction.message.channel.name.startswith("ticket-"):
            user_channel = reaction.message.channel
            ticket_owner_id = ticket_owners.get(user_channel.id)

            if ticket_owner_id == user.id or any(role.name in ["Owner", "Mod"]
                                                 for role in user.roles):
                await user_channel.delete()
                print(f"Ticket {user_channel.name} was closed by {user.name}")
            else:
                await reaction.remove(user)
                print(
                    f"{user.name} does not have permission to close this ticket."
                )


bot.run(
    'enter your token here')
