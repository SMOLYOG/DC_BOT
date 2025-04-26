import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command(name="helpembed")
async def help_embed(ctx):
    embed = discord.Embed(
        title="📚 **Custom Embed Guide**",
        description=
        "This guide will help you understand how to use the `!customembed` command.",
        color=discord.Color.from_str("#1BBC9B")  
    )

    embed.add_field(
        name="**🔹 Command Usage:**",
        value=
        "`!customembed <title> <description> <color> <image_url> <thumbnail_url> <footer_text> <field>`\n\n"
        "Replace the parameters with the appropriate values to create a custom embed.",
        inline=False)

    embed.add_field(
        name="**🔹 Parameters:**",
        value="- `<title>`: The title of the embed (e.g., `My Embed Title`)\n"
        "- `<description>`: The main text of the embed (e.g., `This is the description`)\n"
        "- `<color>`: The color of the embed (HEX format like `#1BBC9B`)\n"
        "- `<image_url>` (optional): URL for the embed's image\n"
        "- `<thumbnail_url>` (optional): URL for the embed's thumbnail\n"
        "- `<footer_text>` (optional): Footer text at the bottom of the embed\n"
        "- `<field>` (optional): Add a custom field in `name|value` format (e.g., `Field Name|Field Value`)",
        inline=False)

    embed.add_field(
        name="**🔹 Example Command:**",
        value=
        "`!customembed \"My Title\" \"This is a description\" \"#1BBC9B\" \"https://imageurl.com\" "
        "\"https://thumbnailurl.com\" \"Footer text\" \"Field Name|Field Value\"`",
        inline=False)

    embed.add_field(
        name="**🔹 Available Roles:**",
        value=
        "Only users with the following roles can use the `!customembed` command:\n"
        "- **MOD**\n"
        "- **FLEXX DEVELOPER**\n"
        "- **OWNER**\n"
        "- **DEV**\n"
        "- **SUPPORT**",
        inline=False)

    embed.add_field(
        name="**🔹 Notes:**",
        value=
        "- All parameters are optional except `<title>` and `<description>`.\n"
        "- Color must be in HEX format (e.g., `#1BBC9B`).\n"
        "- The `field` parameter must be in the format `name|value`.",
        inline=False)

    embed.set_footer(
        text="Use the command carefully! Have fun creating custom embeds! 🎨")
    await ctx.send(embed=embed)


@bot.command(name="customembed")
async def custom_embed(
        ctx,
        title: str,
        description: str,
        color: str = "#1BBC9B",  
        image_url: str = None,
        thumbnail_url: str = None,
        footer_text: str = None,
        field: str = None):
    allowed_roles = ["MOD", "FLEXX DEVELOPER", "OWNER", "SUPPORT", "DEV"]

    has_permission = any(role.name in allowed_roles
                         for role in ctx.author.roles)

    if not has_permission:
        await ctx.send(
            "❌ You do not have the required role to use this command.")
        return

    try:
        embed_color = discord.Color.from_str(color)  
        embed = discord.Embed(title=title,
                              description=description,
                              color=embed_color)

        if field:
            field_name, field_value = field.split("|", 1)
            embed.add_field(name=field_name, value=field_value, inline=False)

        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if footer_text:
            embed.set_footer(text=footer_text)

        await ctx.send(embed=embed)

    except ValueError:
        await ctx.send("❌ Invalid color format! Use HEX format like `#1BBC9B`."
                       )
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


TOKEN = "enter your token here"
bot.run(TOKEN)
