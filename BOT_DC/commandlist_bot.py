import discord
from discord.ext import commands

TOKEN = 'enter your token here'

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

global_channel_id = None

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')

@bot.command()
async def commandlist(ctx, channel_id: int = None):
    if channel_id:
        global global_channel_id
        global_channel_id = channel_id
        await ctx.send(f"Channel ID set to {global_channel_id}. Bot will now send messages to this channel.")

        channel = bot.get_channel(global_channel_id)
        if channel:
            await channel.send("Bot has started and is running!")
        else:
            await ctx.send(f"Could not find channel with ID {global_channel_id}. Please check if the ID is correct.")
    else:
        embed = discord.Embed(
            title="🤖 **Available Commands**",
            description=(
                "💡 **!helpembed**\n→ Guide for using customembed command\n\n"
                "✨ **!customembed**\n→ Creates a custom embed message\n\n"
                "🗑️ **!clear <number>**\n→ Removes specified number of messages\n\n"
                "♻️ **!clear all**\n→ Removes all messages from the channel\n\n"
                "🎟️ **!ticket <channel_id>**\n→ Sends a message in the specified channel allowing users to open a ticket\n\n"
                "🔐 **!verify <channel_id>**\n→ Sends a verification message in the specified channel allowing users to verify themselves"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Use commands with ! prefix")
        await ctx.send(embed=embed)

bot.run(TOKEN)
