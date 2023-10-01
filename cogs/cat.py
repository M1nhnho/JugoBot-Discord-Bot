import discord
import aiohttp
from discord.ext import commands

class Cat(commands.Cog, name ='cat-', description ='cat'):
#Takes a cat pic from the listed API and displays it in an embed
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'cat')
    #Command that sends a cat pic in an embed
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r: #get a json file from the website
                    data = await r.json()
                    #display it in an embed
                    embed = discord.Embed(title="Random cat", colour = self.client.MAINCOLOUR)
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="Image obtained from: http://aws.random.cat/meow")

                    await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Cat(client))
