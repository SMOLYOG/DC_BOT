import discord
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

global_channel_id = None


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Zsynchronizowano {len(synced)} komend.")
    except Exception as e:
        print(f"Błąd synchronizacji: {e}")
    print(f'Bot is ready! Logged in as {bot.user}')


@bot.tree.command(
    name="commandlist",
    description="Wyświetla listę komend lub ustawia kanał globalny")
@app_commands.describe(
    channel_id="ID kanału, do którego bot ma wysyłać wiadomości")
async def commandlist(interaction: discord.Interaction,
                      channel_id: int = None):
    global global_channel_id

    if channel_id:
        global_channel_id = channel_id
        await interaction.response.send_message(
            f"Channel ID set to {global_channel_id}. Bot will now send messages to this channel."
        )

        channel = bot.get_channel(global_channel_id)
        if channel:
            await channel.send("Bot has started and is running!")
        else:
            await interaction.followup.send(
                f"Could not find channel with ID {global_channel_id}. Please check if the ID is correct."
            )
    else:
        embed = discord.Embed(
            title="🤖 **Available Commands**",
            description=
            ("💡 **/helpembed**\n→ Guide for using customembed command\n\n"
             "✨ **/customembed**\n→ Creates a custom embed message\n\n"
             "🗑️ **/clear <number>**\n→ Removes specified number of messages\n\n"
             "♻️ **/clear all**\n→ Removes all messages from the channel\n\n"
             "🎟️ **/ticket <channel_id>**\n→ Sends a message in the specified channel allowing users to open a ticket\n\n"
             "🔐 **/verify <channel_id>**\n→ Sends a verification message in the specified channel allowing users to verify themselves"
             ),
            color=discord.Color.blue())
        embed.set_footer(text="Use slash commands starting with /")
        await interaction.response.send_message(embed=embed)

TOKEN = "ENTER TOKEN HERE"
bot.run(TOKEN)
