import discord
import praw #pip install praw in cmd prompt
import random
from discord.ext import commands

class Meme(commands.Cog, name ='meme-', description ='meme'):
#Takes a random meme from the memes subreddit hot section and displays it in an embed
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'meme')
    async def meme(self, ctx):
    #client ID, secret and user agent obtained from reddit developer app
        reddit = praw.Reddit(client_id='uZMy5GOw4PhNfA', client_secret='AwIZBAqk65iqDqqc5eLBLgQnfZpJ0A', check_for_async=False,
                            user_agent='meme bot cog')
        #content obtained from memes subreddit in the hot section
        memes_submissions = reddit.subreddit('memes').hot()
        #randomise the selection and send an embed with the image
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)


        embed = discord.Embed(title="Random reddit meme", colour  = self.client.MAINCOLOUR)
        embed.set_image(url=submission.url)
        embed.set_footer(text="Image obtained from: https://www.reddit.com/r/memes/")

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Meme(client))
