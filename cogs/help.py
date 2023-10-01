import discord
import json
import os
from discord.ext import commands

class Help(commands.Cog, name='Help_', description='Help menu'):
    #access our client within our cog
    def __init__(self, client):
        self.client = client


#add command to cogs
    @commands.Cog.listener()
    async def on_ready(self):
        pass




####################################Help command
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="**__Commands__**", description=f'Enter `{ctx.prefix}help <command>` to get more information of the command \n(e.g `{ctx.prefix}help clear`)\n\u200b', colour=self.client.MAINCOLOUR)
        embed.set_thumbnail(url="")

        #store all different cogs in their own little list
        coglistUtility = []
        coglistGames = []
        coglistFun = []
        coglistUtility.append('`prefix`')
        for name in self.client.cogs:
            if (name.endswith('_')): #Unreachable cogs
                pass
            elif (name.endswith('+')): #Utilities
                coglistUtility.append('`' + name[:-1] + '`')

            elif (name.endswith('-')): #Fun
                coglistFun.append('`' + name[:-1] + '`')

            elif (name.endswith('#')): #games
                coglistGames.append('`' + name[:-1] + '`')

            else:
                pass

        #sort the cogs
        sorted_list_ut1 = sorted(coglistUtility)
        #join the cogs a ' , ' seperating them (itll also remove the '' and [])
        ut1 = ', '.join(sorted_list_ut1)
        gm1 = ', '.join(coglistGames)
        fn1 = ', '.join(coglistFun)


        ## add those cogs into different fields
        embed.add_field(name=f'🔧 **Utilities**', value=f'{ut1}',inline=False)
        embed.add_field(name=f'🎲 **Games**', value=f'{gm1}',inline=False)
        embed.add_field(name=f'🖼 **Fun**', value=f'{fn1}\n',inline=False)


        await ctx.send(embed=embed)


#########Help feedback
    @help.command()
    async def feedback(self, ctx):
        embed = discord.Embed(title='**Feedback**', description='A short questionnaire in which you can give your opinion on the bot.',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}feedback')
        embed.add_field(name='Example', value=f'{ctx.prefix}feedback')
        await ctx.send(embed=embed)
#########Help prefix
    @help.command()
    async def prefix(self, ctx):
        embed = discord.Embed(title='**Change prefix**', description='Change server prefix before every command',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}prefix <prefix>')
        embed.add_field(name='Example', value=f'{ctx.prefix}prefix !')
        await ctx.send(embed=embed)
#########Help cogs
    @help.command()
    async def cogs(self, ctx):
        embed = discord.Embed(title='**Cogs**', description='Load, Unload, Reload, ReloadAll cogs',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}load <cog name>\n{ctx.prefix}unload <cog name>\n{ctx.prefix}reload <cog name>\n{ctx.prefix}reloadAll')
        #xxx
        await ctx.send(embed=embed)
#########Help clear
    @help.command()
    async def clear(self, ctx):
        embed = discord.Embed(title='**Clear**', description='Purges the previous <amount> of messages.',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}clear <amount>')
        embed.add_field(name='Example', value=f'{ctx.prefix}clear 5')
        await ctx.send(embed=embed)
#########Help dice
    @help.command()
    async def dice(self, ctx):
        embed = discord.Embed(title='**Dice**', description='2 Player dice game that generates random number for each player, and the player with biggest rolled number wins. ',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}dice <min> <max>')
        embed.add_field(name='Example', value=f'{ctx.prefix}dice 1 10')
        await ctx.send(embed=embed)
#########Help headsup
    @help.command()
    async def charades(self, ctx):
        embed = discord.Embed(title='**Charades**', description='Charades game, a private message would be sent to the user after executing the command and players then would have to guess the word in chat. After 2 minutes, the game would end if no one guessed right.',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}charades')
        embed.add_field(name='Example', value=f'{ctx.prefix}charades')
        await ctx.send(embed=embed)
#########Help cat
    @help.command()
    async def cat(self, ctx):
        embed = discord.Embed(title='**Cat**', description='Display random cat images from the web!  ',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}cat')
        embed.add_field(name='Example', value=f'{ctx.prefix}cat')
        await ctx.send(embed=embed)
#########Help poll
    @help.command()
    async def poll(self, ctx):
        embed = discord.Embed(title='**Poll**', description='Make a poll for people in chat to react to. Has maximum 10 options and provides a summary after a set time ',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}poll <time in seconds> <"question"> <option1> <option2>... ',inline=False)
        embed.add_field(name='Example', value=f'{ctx.prefix}poll 2 "Do you like apples?" Yes No Maybe...',inline=False)
        await ctx.send(embed=embed)
#########Help meme
    @help.command()
    async def meme(self, ctx):
        embed = discord.Embed(title='**Meme**', description='Random images of memes from reddit!',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}meme')
        embed.add_field(name='Example', value=f'{ctx.prefix}meme')
        await ctx.send(embed=embed)
#########Help feedback
    @help.command()
    async def timezone(self, ctx):
        embed = discord.Embed(title='**Timezone**', description='Convert any time mentioned in chat to your own timezone (user must setup their region of timezone first)',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}timezone <region>')
        embed.add_field(name='Example', value=f'{ctx.prefix}timezone Europe/London')
        await ctx.send(embed=embed)
#########Help rps
    @help.command()
    async def rps(self, ctx):
        embed = discord.Embed(title='**Rock Paper Scissors**', description=f'Rock Paper Scissors vs {self.client.user}',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}rps')
        embed.add_field(name='Example', value=f'{ctx.prefix}rps')
        await ctx.send(embed=embed)
#########Help trivia
    @help.command()
    async def trivia(self, ctx):
        embed = discord.Embed(title='**Trivia**', description='Play your own custom trivia lists!',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}tri / {ctx.prefix}trivia')
        embed.add_field(name='Example', value=f'{ctx.prefix}tri')
        await ctx.send(embed=embed)
#########Help leaderboard
    @help.command()
    async def leaderboard(self, ctx):
        embed = discord.Embed(title='**Leaderboard**', description='Leaderboard for games and overall points.',colour=self.client.MAINCOLOUR)
        embed.add_field(name='Command Syntax', value=f'{ctx.prefix}lb / {ctx.prefix}leaderboard')
        embed.add_field(name='Example', value=f'{ctx.prefix}lb')
        await ctx.send(embed=embed)


####################################End of Help command

async def setup(client):
    await client.add_cog(Help(client))
