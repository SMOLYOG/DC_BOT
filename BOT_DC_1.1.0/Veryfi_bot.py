import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!',
                   intents=intents)  # prefix nie jest używany dla slash


async def assign_role(user: discord.Member, role_name: str):
    guild = user.guild
    role = discord.utils.get(guild.roles, name=role_name)

    if role:
        await user.add_roles(role)
        print(f"Assigned {role_name} to {user.name}")
    else:
        print(f"Role {role_name} not found!")


@bot.tree.command(
    name="verify",
    description="Send verification message in a specified channel")
@app_commands.describe(
    channel="The channel where verification message will be sent")
async def verify(interaction: discord.Interaction,
                 channel: discord.TextChannel):
    embed = discord.Embed(
        title="Click to Verify",
        description=
        "Click on the green check mark (✅) to verify yourself and gain access.",
        color=discord.Color(int("1BBC9B", 16)))
    embed.set_footer(text="Verification System - Discord Bot")

    message = await channel.send(embed=embed)
    await message.add_reaction("✅")

    await interaction.response.send_message(
        f"Verification message sent in {channel.mention}.", ephemeral=True)


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.emoji == "✅":
        await assign_role(user, "MEMBER")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready! Logged in as {bot.user}.")


bot.run(
    'ENTER TOKEN HERE')
