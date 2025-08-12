import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_ROLES = ["MOD", "FLEXX DEVELOPER", "OWNER", "SUPPORT", "DEV"]


@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(
    name="helpembed",
    description="Shows a guide on how to use the customembed command")
async def helpembed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 **Custom Embed Guide**",
        description=
        "This guide will help you understand how to use the `/customembed` command.",
        color=discord.Color.from_str("#1BBC9B"))

    embed.add_field(
        name="**🔹 Command Usage:**",
        value=
        ("`/customembed title description color image_url thumbnail_url footer_text field`\n\n"
         "Replace the parameters with the appropriate values to create a custom embed."
         ),
        inline=False)

    embed.add_field(
        name="**🔹 Parameters:**",
        value=
        ("- `title`: The embed title (e.g., `My Embed Title`)\n"
         "- `description`: The main embed text\n"
         "- `color`: The embed color in HEX (e.g., `#1BBC9B`)\n"
         "- `image_url` (optional): URL for the embed's image\n"
         "- `thumbnail_url` (optional): URL for the embed's thumbnail\n"
         "- `footer_text` (optional): Footer text at the bottom\n"
         "- `field` (optional): Custom field in the format `name|value` (e.g., `Field Name|Field Value`)"
         ),
        inline=False)

    embed.add_field(
        name="**🔹 Example Command:**",
        value=
        ("`/customembed title:\"My Title\" description:\"This is a description\" color:\"#1BBC9B\" "
         "image_url:\"https://imageurl.com\" thumbnail_url:\"https://thumbnailurl.com\" "
         "footer_text:\"Footer text\" field:\"Field Name|Field Value\"`"),
        inline=False)

    embed.add_field(
        name="**🔹 Allowed Roles:**",
        value=
        ("Only users with the following roles can use this command:\n"
         "- **MOD**\n- **FLEXX DEVELOPER**\n- **OWNER**\n- **DEV**\n- **SUPPORT**"
         ),
        inline=False)

    embed.add_field(
        name="**🔹 Notes:**",
        value=(
            "- All parameters except `title` and `description` are optional.\n"
            "- Color must be in HEX format (e.g., `#1BBC9B`).\n"
            "- The `field` parameter must be in the `name|value` format."),
        inline=False)

    embed.set_footer(
        text="Use the command carefully! Have fun creating custom embeds! 🎨")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(
    name="customembed",
    description="Creates a custom embed with the given parameters")
@app_commands.describe(title="Embed title",
                       description="Embed description",
                       color="Embed color in HEX, e.g., #1BBC9B",
                       image_url="Image URL (optional)",
                       thumbnail_url="Thumbnail URL (optional)",
                       footer_text="Footer text (optional)",
                       field="Field in the format name|value (optional)")
async def customembed(interaction: discord.Interaction,
                      title: str,
                      description: str,
                      color: str = "#1BBC9B",
                      image_url: str = None,
                      thumbnail_url: str = None,
                      footer_text: str = None,
                      field: str = None):
    if not any(role.name in ALLOWED_ROLES for role in interaction.user.roles):
        await interaction.response.send_message(
            "❌ You do not have the required role to use this command.",
            ephemeral=True)
        return

    try:
        embed_color = discord.Color.from_str(color)
    except ValueError:
        await interaction.response.send_message(
            "❌ Invalid color format! Use HEX format like `#1BBC9B`.",
            ephemeral=True)
        return

    embed = discord.Embed(title=title,
                          description=description,
                          color=embed_color)

    if field:
        try:
            field_name, field_value = field.split("|", 1)
            embed.add_field(name=field_name, value=field_value, inline=False)
        except Exception:
            await interaction.response.send_message(
                "❌ Field parameter format invalid! Use `name|value`.",
                ephemeral=True)
            return

    if image_url:
        embed.set_image(url=image_url)
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    if footer_text:
        embed.set_footer(text=footer_text)

    await interaction.response.send_message(embed=embed)


TOKEN = "ENTER TOKEN HERE"
bot.run(TOKEN)
