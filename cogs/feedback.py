import discord
from discord.ext import commands

class Feedback(commands.Cog, name ='feedback+', description ='feedback'):
#Sends a link to a questionnaire for users to give their feedback on
    def __init__(self, client):
        self.client = client

    @commands.command()
    #Command that sends an embed with a link to the questionnaire
    async def feedback(self, ctx):
        embed = discord.Embed(
            colour  = self.client.MAINCOLOUR
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/481225228630884363/825097904090906684/icon.png')
        embed.add_field(name='Tell us what you think!', value='Please complete this short questionnaire based on your experience using the bot https://tinyurl.com/Jugobot', inline = True)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Feedback(client))
