import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_CLEAR_ROLES = ["MOD", "FLEXX DEVELOPER", "OWNER", "SUPPORT", "DEV"]
LOG_CHANNEL_ID = 1336997478603423786
LOG_FILE = "logs.txt"


def has_clear_role(ctx):
    return any(role.name in ALLOWED_CLEAR_ROLES for role in ctx.author.roles)


@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: str | None = "10"):
    if not has_clear_role(ctx):
        await ctx.send("❌ You do not have permission to use this command!",
                       delete_after=3)
        return

    if amount is None:
        await ctx.send("⚠️ Usage: `!clear <number>` or `!clear all`",
                       delete_after=3)
        return

    if amount.lower() == "all":
        await clear_all(ctx)
    elif amount.isdigit():
        amount = int(amount)
        if amount > 0:
            deleted_messages = await ctx.channel.purge(limit=amount + 1)
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                for msg in deleted_messages:
                    if msg.author != bot.user:
                        f.write(
                            f"[{msg.created_at}] {msg.author}: {msg.content}\n"
                        )

            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel and os.path.exists(LOG_FILE):
                await log_channel.send(file=discord.File(LOG_FILE))
                os.remove(LOG_FILE)

            await ctx.send(f"✅ Deleted {len(deleted_messages)-1} messages!",
                           delete_after=3)
        else:
            await ctx.send("⚠️ Please provide a number greater than 0!",
                           delete_after=3)
    else:
        await ctx.send("⚠️ Usage: `!clear <number>` or `!clear all`",
                       delete_after=3)


async def clear_all(ctx):
    guild = ctx.guild
    old_channel = ctx.channel
    overwrites = old_channel.overwrites

    new_channel = await guild.create_text_channel(
        name=old_channel.name,
        category=old_channel.category,
        topic=old_channel.topic,
        overwrites=overwrites)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"\n[{old_channel.name}] Channel deleted by {ctx.author} at {ctx.message.created_at}\n"
        )

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel and os.path.exists(LOG_FILE):
        await log_channel.send(file=discord.File(LOG_FILE))
        os.remove(LOG_FILE)

    await ctx.send("⚠️ Deleting channel...")
    await old_channel.delete()
    await new_channel.send(
        f"✅ Channel has been cleared by {ctx.author.mention}.")


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to delete messages!",
                       delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Usage: `!clear <number>` or `!clear all`",
                       delete_after=3)



TOKEN = "enter your token here"
bot.run(TOKEN)
