import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def assign_role(user, role_name):
    guild = user.guild
    role = discord.utils.get(guild.roles, name=role_name)

    if role:
        await user.add_roles(role)
        print(f"Assigned {role_name} to {user.name}")
    else:
        print(f"Role {role_name} not found!")


@bot.command(name="verify")
async def verify(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="Click to Verify",
            description=
            "Click on the green check mark (✅) to verify yourself and gain access.",
            color=discord.Color(int("1BBC9B", 16))  # Zmiana koloru na #1BBC9B
        )
        embed.set_footer(text="Verification System - Discord Bot")

        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
    else:
        await ctx.send("Channel with the provided ID not found!")


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.emoji == "✅":
        await assign_role(user, "MEMBER")


bot.run(
    'enter your token here')
