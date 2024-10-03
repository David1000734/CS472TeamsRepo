import discord
from discord.ext import commands
import re
from discord import FFmpegPCMAudio
import asyncio

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    # *************** Non-command/event Functions ***************
    async def check_emoji(self, msg):
        # Build the string for the bot to print it
        tempContent = msg.content

        # Iterate through all emojis available on the server
        for emoji in msg.guild.emojis:
            
            # Keep a copy of the message content before making replacements.
            # We will use this copy to make changes without affecting the original temporarily.
            currStr = tempContent
            
            # Proceed only if the current emoji is animated
            if emoji.animated:
                
                # Construct a regular expression pattern to search for the emoji name in the message.
                # The pattern looks for the emoji name surrounded by colons like :emoji_name:
                # For example, if the emoji's name is 'happy', it will search for ':happy:' in the message.
                emoji_pattern = rf":({emoji.name}):"
                
                # Replace any occurrence of the emoji's text form (like ":happy:") with its actual emoji character.
                # re.sub() function does this replacement:
                # - First argument is the pattern we are searching for (emoji_pattern),
                # - Second argument is the actual emoji object converted to string (str(emoji)),
                # - Third argument is the string we are working on (currStr), which holds the current state of the message content.
                tempContent = re.sub(emoji_pattern, str(emoji), currStr)

        if len(msg.content) < len(tempContent):
            await msg.delete()

            # Grab author's name
            nickName = msg.author.display_name

            # Create a webhook to send a message
            webhook = await msg.channel.create_webhook(name = nickName)

            # Use webhook to send message as the author
            await webhook.send(
                str(tempContent), username = nickName, avatar_url = msg.author.avatar
            )

            # Remove webhook after done using them
            webhooks = await msg.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
            # emoji is in the server list

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title = "Goooooooooogle", url = "https://google.com",\
                            description = "Heres google", color = 0x5A2F26)
        embed.set_author(name = ctx.author.display_name, url = "https://bing.com", icon_url = ctx.author.avatar)
        embed.set_thumbnail(url = "https://w0.peakpx.com/wallpaper/208/932/HD-wallpaper-mountin-calm-lake-simple.jpg")
        embed.add_field(name = "Labradore", value = "Cute Dog", inline = True)
        embed.add_field(name = "Chihuahua", value = "Little Devil", inline = True)
        embed.set_footer(text = "Thanks for reading :)")

        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Get the user that sent this message
        author = msg.guild.get_member(msg.author.id)

        # Check to see if they have premium. Only run if false
        # Ignore all messages from a bot
        if (not msg.author.bot and author.premium_since is None):
            await self.check_emoji(msg)
        # if premium or bot, END

async def setup(client):
    await client.add_cog(Miscellaneous(client))