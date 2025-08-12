import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_CLEAR_ROLES = ["MOD", "FLEXX DEVELOPER", "OWNER", "SUPPORT", "DEV"]
LOG_CHANNEL_ID = 1336997478603423786
LOG_FILE = "logs.txt"


def has_clear_role(user):
    return any(role.name in ALLOWED_CLEAR_ROLES for role in user.roles)


@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Zsynchronizowano {len(synced)} komend.")
    except Exception as e:
        print(f"Błąd synchronizacji komend: {e}")


@bot.tree.command(name="clear",
                  description="Usuwa wiadomości lub czyści cały kanał")
@app_commands.describe(
    amount="Ilość wiadomości do usunięcia lub 'all' aby wyczyścić cały kanał")
async def clear(interaction: discord.Interaction, amount: str = "10"):
    if not has_clear_role(interaction.user):
        await interaction.response.send_message(
            "❌ You do not have permission to use this command!",
            ephemeral=True)
        return

    # Odroczenie odpowiedzi, aby uniknąć błędu Unknown interaction
    await interaction.response.defer(ephemeral=True)

    if amount.lower() == "all":
        await clear_all(interaction)
    elif amount.isdigit():
        amount_int = int(amount)
        if amount_int > 0:
            deleted_messages = await interaction.channel.purge(limit=amount_int
                                                               )
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

            await interaction.followup.send(
                f"✅ Deleted {len(deleted_messages)} messages!", ephemeral=True)
        else:
            await interaction.followup.send(
                "⚠️ Please provide a number greater than 0!", ephemeral=True)
    else:
        await interaction.followup.send(
            "⚠️ Usage: `/clear <number>` or `/clear all`", ephemeral=True)


async def clear_all(interaction: discord.Interaction):
    guild = interaction.guild
    old_channel = interaction.channel
    overwrites = old_channel.overwrites

    new_channel = await guild.create_text_channel(
        name=old_channel.name,
        category=old_channel.category,
        topic=old_channel.topic,
        overwrites=overwrites)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"\n[{old_channel.name}] Channel deleted by {interaction.user} at {interaction.created_at}\n"
        )

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel and os.path.exists(LOG_FILE):
        await log_channel.send(file=discord.File(LOG_FILE))
        os.remove(LOG_FILE)

    await new_channel.send(
        f"✅ Channel has been cleared by {interaction.user.mention}.")

    await old_channel.delete()


TOKEN = "ENTER_TOKEN_HERE"
bot.run(TOKEN)
